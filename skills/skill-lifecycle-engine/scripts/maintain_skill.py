#!/usr/bin/env python3
"""Audit a skill folder: structure, frontmatter limits, and reference routing.

Single entry point, no third-party dependencies, ASCII-only output.
Exit code 1 means at least one FAIL; warnings do not fail the audit.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DESC_HARD_MAX = 1024  # VS Code Agent Skills limit
DESC_SOFT_MIN = 300
DESC_SOFT_MAX = 800
NAME_MAX = 64
BODY_SOFT_MAX_LINES = 500
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REF_RE = re.compile(r"(?:references|examples|scripts|assets)/[A-Za-z0-9_./-]+")

REQUIRED_FILES = ["SKILL.md"]
RECOMMENDED_PATHS = [
    "references/manifest.md",
    "references/workflow.md",
    "references/fallback.md",
    "examples/positive.md",
    "examples/negative.md",
]
OPTIONAL_PATHS = ["agents/openai.yaml", "scripts", "assets"]


def parse_frontmatter(text: str) -> dict[str, str] | None:
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None

    data: dict[str, str] = {}
    i = 1
    while i < end:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
        if not match:
            i += 1
            continue
        key, value = match.group(1), match.group(2).strip()
        i += 1
        if value[:1] in ("|", ">"):
            block = []
            while i < end and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            joiner = "\n" if value[0] == "|" else " "
            value = joiner.join(block).strip()
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        data[key] = value
    return data


def audit(skill_dir: Path) -> int:
    fails: list[str] = []
    warns: list[str] = []

    def ok(msg: str) -> None:
        print(f"[OK]   {msg}")

    def warn(msg: str) -> None:
        warns.append(msg)
        print(f"[WARN] {msg}")

    def fail(msg: str) -> None:
        fails.append(msg)
        print(f"[FAIL] {msg}")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail("required: SKILL.md is missing")
        return finish(fails, warns)

    text = skill_md.read_text(encoding="utf-8-sig")
    meta = parse_frontmatter(text)
    if meta is None:
        fail("SKILL.md has no valid YAML frontmatter delimited by ---")
        return finish(fails, warns)

    name = meta.get("name", "")
    if not name:
        fail("frontmatter: name is missing")
    elif not NAME_RE.match(name) or len(name) > NAME_MAX:
        fail(f"frontmatter: name '{name}' must be lowercase hyphen-case, max {NAME_MAX} chars")
    elif name != skill_dir.name:
        fail(f"frontmatter: name '{name}' must match folder name '{skill_dir.name}'")
    else:
        ok(f"name '{name}' is valid and matches the folder")

    desc = meta.get("description", "")
    length = len(desc)
    if not desc:
        fail("frontmatter: description is missing")
    elif length > DESC_HARD_MAX:
        fail(f"description is {length} chars; hard limit is {DESC_HARD_MAX} (VS Code). Shorten it")
    elif length > DESC_SOFT_MAX:
        warn(f"description is {length} chars; target {DESC_SOFT_MIN}-{DESC_SOFT_MAX}, hard max {DESC_HARD_MAX}")
    elif length < DESC_SOFT_MIN:
        warn(f"description is {length} chars; under {DESC_SOFT_MIN} usually triggers poorly")
    else:
        ok(f"description length {length} chars (target {DESC_SOFT_MIN}-{DESC_SOFT_MAX}, hard max {DESC_HARD_MAX})")

    line_count = len(text.splitlines())
    if line_count > BODY_SOFT_MAX_LINES:
        warn(f"SKILL.md has {line_count} lines; move detail into references/")
    else:
        ok(f"SKILL.md has {line_count} lines")

    body = text.lstrip("\ufeff").split("---", 2)[2]
    for rel in sorted(set(m.rstrip(".") for m in REF_RE.findall(body))):
        if not (skill_dir / rel).exists():
            fail(f"SKILL.md references missing path: {rel}")
    for rel in RECOMMENDED_PATHS:
        (ok if (skill_dir / rel).exists() else warn)(f"recommended: {rel}")
    for rel in OPTIONAL_PATHS:
        print(f"[INFO] optional: {rel} {'present' if (skill_dir / rel).exists() else 'absent'}")

    return finish(fails, warns)


def finish(fails: list[str], warns: list[str]) -> int:
    if fails:
        print(f"[FAIL] {len(fails)} blocking problem(s); fix them, then re-run.")
        return 1
    if warns:
        print(f"[WARN] usable, {len(warns)} warning(s).")
        return 0
    print("[PASS] skill is complete.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", required=True, help="Path to the target skill directory")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.is_dir():
        print(f"[FAIL] skill directory not found: {skill_dir}")
        return 1
    print(f"[INFO] auditing: {skill_dir}")
    return audit(skill_dir)


if __name__ == "__main__":
    sys.exit(main())
