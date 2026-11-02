#!/usr/bin/env python3
"""Dependency-free heuristic checker for common Google C++ style issues."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXTENSIONS = {".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx", ".ipp"}
SKIP_DIRS = {".git", ".svn", "build", "out", "dist", "third_party", "vendor"}


def files_for(path: Path):
    if path.is_file():
        return [path] if path.suffix.lower() in EXTENSIONS else []
    if not path.is_dir():
        raise FileNotFoundError(path)
    return sorted(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in EXTENSIONS and not any(part in SKIP_DIRS or part.startswith(".") for part in p.parts))


def finding(path, line, rule, message, severity="medium", fixable=False):
    return {"file": str(path), "line": line, "severity": severity, "rule": rule, "message": message, "fixable": fixable}


def check_file(path: Path, max_len: int):
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    findings = []
    is_header = path.suffix.lower() in {".h", ".hh", ".hpp", ".hxx", ".ipp"}
    guard_seen = False
    include_lines = []
    include_tokens = []
    for number, raw in enumerate(lines, 1):
        line = raw.rstrip("\r\n")
        if "\t" in line:
            findings.append(finding(path, number, "indentation", "使用 2 个空格缩进，不要使用 tab。", fixable=True))
        if line.rstrip() != line:
            findings.append(finding(path, number, "whitespace", "行尾存在空白。", severity="low", fixable=True))
        if len(line) > max_len and not line.lstrip().startswith(("#include", "//", "*")):
            findings.append(finding(path, number, "line-length", f"行长为 {len(line)}，默认上限为 {max_len} 列；长字符串等例外需说明。", severity="low"))
        if re.search(r"\busing\s+namespace\s+", line):
            findings.append(finding(path, number, "namespace", "避免 using namespace，尤其不要放在头文件中。", severity="high"))
        if re.search(r"\b(NULL)\b", line):
            findings.append(finding(path, number, "modern-cpp", "使用 nullptr 替代 NULL。", severity="medium", fixable=True))
        if re.search(r"\([A-Za-z_][\w:<>,\s*&]*\)\s*[A-Za-z_0-9(]", line) and not line.lstrip().startswith("#"):
            findings.append(finding(path, number, "casts", "可能存在 C 风格转换；请确认后改用 static_cast、const_cast 等命名转换。", severity="high"))
        if line.lstrip().startswith("#include"):
            include_lines.append((number, line))
            match = re.match(r"\s*#include\s*([<\"])([^>\"]+)[>\"]", line)
            if match:
                include_tokens.append((number, match.group(1), match.group(2)))
        if re.match(r"\s*#\s*ifndef\s+\w+_H_\s*$", line) or re.match(r"\s*#\s*define\s+\w+_H_\s*$", line):
            guard_seen = True
    if is_header and not guard_seen and "#pragma once" not in text:
        findings.append(finding(path, 1, "header-guard", "头文件缺少 include guard 或 #pragma once。", severity="medium"))
    if include_tokens:
        seen = set()
        previous_group = -1
        previous_name = ""
        for number, delimiter, name in include_tokens:
            if name in seen:
                findings.append(finding(path, number, "includes", f"重复 include：{name}。", severity="medium"))
            seen.add(name)
            if delimiter == '"':
                group = 0 if is_header or name.startswith(path.stem) else 3
            elif name.endswith(".h"):
                group = 1
            elif name in {"algorithm", "array", "cassert", "cstddef", "cstdint", "functional", "memory", "optional", "string", "string_view", "tuple", "type_traits", "utility", "vector"}:
                group = 2
            else:
                group = 3
            if group < previous_group:
                findings.append(finding(path, number, "include-order", "include 分组顺序可能不符合：项目头、C 系统头、C++ 标准库、第三方库。请按项目规则确认。", severity="medium"))
            if group == previous_group and name < previous_name:
                findings.append(finding(path, number, "include-order", "同一 include 分组应保持稳定的字典序。", severity="low"))
            previous_group, previous_name = group, name
    if re.search(r"\b(class|struct)\s+\w+\s*\{", text) and re.search(r"\b[A-Za-z_]\w*\s*\([^;{}]*\)\s*\{", text) and not re.search(r"\bexplicit\s+[A-Za-z_]\w*\s*\(", text):
        findings.append(finding(path, 1, "constructors", "类中可能存在单参数构造函数，请确认是否需要 explicit。", severity="medium"))
    if re.search(r"\b(int|long|float|double|char|bool)\s*\*\s*\w+", text) and re.search(r"\bdelete\b", text) is None:
        findings.append(finding(path, 1, "ownership", "发现裸指针；请确认所有权并优先使用 RAII 或智能指针。", severity="medium"))
    return findings, text


def apply_fixes(path: Path, text: str):
    fixed = text.replace("\t", "  ")
    fixed = re.sub(r"\bNULL\b", "nullptr", fixed)
    fixed = "\n".join(line.rstrip() for line in fixed.splitlines())
    if text.endswith(("\n", "\r")):
        fixed += "\n"
    if fixed != text:
        path.write_text(fixed, encoding="utf-8", newline="")
    return fixed != text


def main():
    parser = argparse.ArgumentParser(description="Check common C++ style rules")
    parser.add_argument("path")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--max-line-length", type=int, default=80)
    parser.add_argument("--fix", action="store_true", help="apply only mechanical fixes")
    args = parser.parse_args()
    try:
        paths = files_for(Path(args.path))
        if not paths:
            raise ValueError("no supported C++ files found")
        all_findings = []
        changed = []
        for path in paths:
            findings, text = check_file(path, args.max_line_length)
            if args.fix and apply_fixes(path, text):
                changed.append(str(path))
            all_findings.extend(findings)
        result = {"files": [str(p) for p in paths], "findings": all_findings, "changed": changed}
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Checked {len(paths)} C++ file(s); findings: {len(all_findings)}")
            for item in all_findings:
                print(f"[{item['severity'].upper()}] {item['file']}:{item['line']} {item['rule']}: {item['message']}")
            if changed:
                print("Changed: " + ", ".join(changed))
        return 0
    except (OSError, UnicodeError, ValueError, FileNotFoundError) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
