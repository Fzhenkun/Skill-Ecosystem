# Review Workflow

## 1. Establish scope

Identify the exact file, directory, or pasted snippet. Include only C++ source/header files unless the user asks for build configuration. Check for `.clang-format`, `clang-tidy`, `cpplint`, or repository guidance and record the precedence.

## 2. Run mechanical checks

```powershell
python scripts/cpp_style_check.py <path> --format text
python scripts/cpp_style_check.py <path> --format json
```

Use `--max-line-length N` only when the project specifies another limit. The script skips generated and hidden directories by default. Its include-order and ownership findings are heuristics and require human confirmation.

## 3. Perform semantic review

Review include self-sufficiency, ownership, casts, API changes, const correctness, macro hazards, and whether a suggested formatting change alters meaning. Distinguish observed violations from suggestions that need context.

## 4. Report

Use this shape:

```text
摘要：<范围>；标准：<标准和项目覆盖关系>；发现：<高/中/低数量>

[高] path:line - <规则>
原因：<具体风险>
建议：<最小修改或代码片段>
自动修正：否/是
```

## 5. Optional fix

Only after an explicit request, show the planned low-risk edits and run:

```powershell
python scripts/cpp_style_check.py <path> --fix --format text
```

Re-run without `--fix`, report the remaining findings, and advise the user to compile and run project tests. Do not claim semantic correctness from this script alone.
