"""Idempotently audit or create the shared agent-project directory layout."""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT_AGENTS = """# Agent 项目规则

本文件是项目 Agent 规则的唯一真相源。其他工具适配文件只引用本文件，不复制规则。

## 目录约定

- `.agents/skills/` 存放跨工具 Skill。
- `agent-os/standards/` 存放从代码库抽取的规范。
- `openspec/changes/` 存放变更提案，`openspec/specs/` 存放规格。
- `packages/*/AGENTS.md` 存放包目录专属规则，就近规则优先。

请在这里补充项目实际的构建、测试、风格和禁止操作规则。
"""
CLAUDE = "@AGENTS.md\n"
COPILOT = "See AGENTS.md at the repository root for all project instructions.\n"
PACKAGE_AGENTS = "# Package 规则\n\n本目录暂无专属规则；通用规则以项目根 AGENTS.md 为准。\n"


@dataclass
class Change:
    status: str
    path: Path
    detail: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--skill-name", required=True)
    parser.add_argument("--skill-source", type=Path)
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def ensure_name(name: str) -> None:
    if not name or name == "<name>" or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in name):
        raise ValueError("--skill-name 必须是非空的小写 hyphen-case 名称，不能使用 <name>")


def classify(path: Path) -> str:
    if path.is_dir():
        return "existing-dir"
    if path.is_file():
        return "existing-file"
    return "missing"


def add_parent_conflicts(root: Path, path: Path, conflicts: list[Path]) -> None:
    parent = path.parent
    while parent != root:
        if parent.is_file():
            conflicts.append(parent)
            return
        parent = parent.parent


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    ensure_name(args.skill_name)
    if not root.is_dir():
        print(f"[FAIL] 项目根目录不存在或不是目录: {root}")
        return 1

    source = (args.skill_source or Path(__file__).resolve().parents[1]).resolve() / "SKILL.md"
    targets = {
        root / "AGENTS.md": ("file", ROOT_AGENTS),
        root / "CLAUDE.md": ("file", CLAUDE),
        root / ".github" / "copilot-instructions.md": ("file", COPILOT),
        root / ".agents" / "skills" / args.skill_name / "SKILL.md": ("file", None),
        root / "agent-os" / "standards": ("dir", None),
        root / "openspec" / "changes": ("dir", None),
        root / "openspec" / "specs": ("dir", None),
        root / "packages": ("dir", None),
    }
    conflicts: list[Path] = []
    changes: list[Change] = []

    for path, (kind, content) in targets.items():
        add_parent_conflicts(root, path, conflicts)
        state = classify(path)
        if kind == "dir" and state == "existing-file":
            conflicts.append(path)
        elif kind == "file" and state == "existing-dir":
            conflicts.append(path)
        elif state == "missing":
            changes.append(Change("created", path))
        else:
            changes.append(Change("existing", path))

    packages = root / "packages"
    if packages.is_dir():
        for child in sorted(packages.iterdir()):
            if not child.is_dir():
                continue
            package_agents = child / "AGENTS.md"
            add_parent_conflicts(root, package_agents, conflicts)
            state = classify(package_agents)
            if state == "existing-dir":
                conflicts.append(package_agents)
            elif state == "missing":
                changes.append(Change("created", package_agents))
            else:
                changes.append(Change("existing", package_agents))

    if not source.is_file():
        conflicts.append(source)

    if conflicts:
        for path in conflicts:
            print(f"[CONFLICT] {path}")
        print("[FAIL] 预检发现路径类型冲突或 Skill 源文件缺失，未执行写入。")
        return 1

    if not args.apply:
        for change in changes:
            print(f"[{change.status}] {change.path}")
        print("[CHECK] 只读检查完成；使用 --apply 创建缺失项。")
        return 0

    for path, (kind, content) in targets.items():
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        if kind == "dir":
            path.mkdir()
        elif content is None:
            shutil.copyfile(source, path)
        else:
            path.write_text(content, encoding="utf-8", newline="\n")

    packages.mkdir(parents=True, exist_ok=True)
    for child in sorted(packages.iterdir()):
        if child.is_dir() and not (child / "AGENTS.md").exists():
            (child / "AGENTS.md").write_text(PACKAGE_AGENTS, encoding="utf-8", newline="\n")

    for change in changes:
        print(f"[{change.status}] {change.path}")
    print("[APPLY] 缺失项已幂等补齐；已有文件未覆盖。")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(f"[FAIL] {error}")
        raise SystemExit(1)

