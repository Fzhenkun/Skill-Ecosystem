#!/usr/bin/env python3
"""
Structural maintenance helper for Codex skills.

Checks for the presence of key files and directories used by a complete skill package.
"""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
]

RECOMMENDED_PATHS = [
    "references/manifest.md",
    "references/workflow.md",
    "references/fallback.md",
    "references/description-patterns.md",
    "examples/positive.md",
    "examples/negative.md",
]

OPTIONAL_DIRS = [
    "scripts",
    "references",
    "examples",
    "assets",
]


def check_path(skill_dir: Path, relative_path: str) -> bool:
    return (skill_dir / relative_path).exists()


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Codex skill structure.")
    parser.add_argument("--skill-dir", required=True, help="Path to the target skill directory")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.exists() or not skill_dir.is_dir():
        print(f"[ERROR] Skill directory not found: {skill_dir}")
        return 1

    print(f"[INFO] Auditing: {skill_dir}")

    missing_required = [path for path in REQUIRED_FILES if not check_path(skill_dir, path)]
    missing_recommended = [path for path in RECOMMENDED_PATHS if not check_path(skill_dir, path)]
    missing_optional_dirs = [path for path in OPTIONAL_DIRS if not check_path(skill_dir, path)]

    for path in REQUIRED_FILES:
        status = "OK" if path not in missing_required else "MISSING"
        print(f"[{status}] required: {path}")

    for path in RECOMMENDED_PATHS:
        status = "OK" if path not in missing_recommended else "MISSING"
        print(f"[{status}] recommended: {path}")

    for path in OPTIONAL_DIRS:
        status = "OK" if path not in missing_optional_dirs else "MISSING"
        print(f"[{status}] optional-dir: {path}")

    if missing_required:
        print("[FAIL] Required skill files are missing.")
        return 1

    if missing_recommended or missing_optional_dirs:
        print("[WARN] Skill is usable but not fully complete.")
        return 0

    print("[PASS] Skill structure is complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
