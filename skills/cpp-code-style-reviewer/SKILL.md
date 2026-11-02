---
name: cpp-code-style-reviewer
description: "MUST USE when the user asks to review, lint, explain, suggest fixes for, or reformat C++ code according to Google C++ Style Guide or a similar team standard. Checks headers, includes, naming, formatting, namespaces, classes, constructors, const correctness, pointers/references, macros, modern C++ usage, and maintainability; gives file/line findings with severity and safer alternatives. If the user explicitly requests it, may apply only reviewed, low-risk mechanical fixes and show the diff. Supports .cc/.cpp/.cxx/.h/.hpp and pasted snippets. Do NOT use for compiling, debugging runtime behavior, designing architecture, or silently rewriting code without explicit fix permission. 触发词：C++ 规范、代码审查、Google C++ Style Guide、格式化、命名、头文件、include、修正代码。"
---

# C++ Code Style Reviewer

审查 C++ 代码是否符合图片所示的 Google C++ Style Guide 要点，并输出可执行的修改建议。用户明确要求“修正/自动修改/应用修复”时才改文件；默认只审查。

## 触发场景

| 场景 | 典型请求 | 触发关键词 |
| --- | --- | --- |
| 审查文件或目录 | “检查这个 C++ 项目的规范” | review, lint, C++, 代码规范 |
| 解释违规项 | “为什么这个 include 顺序不对？” | explain, 建议, Google C++ Style Guide |
| 生成补丁 | “按规范修正这些文件” | fix, reformat, 自动修正, 应用修改 |
| 审查片段 | “看看这段类定义是否符合规范” | snippet, class, naming, const |

## 工作方式

1. 保留用户给出的路径、代码和标准名称原文；先判断目标是文件、目录还是代码片段。
2. 读取 `references/workflow.md`，确定审查范围、标准优先级和输出格式。
3. 读取 `references/style-rules.md`，按严重性审查；项目已有 `.clang-format`、lint 配置或团队规则时优先遵循项目规则，并标出与 Google 风格的差异。
4. 对文件/目录可运行 `scripts/cpp_style_check.py` 获取机械检查结果。脚本结果只是证据，不能替代语义审查。
5. 默认只报告问题。只有用户明确要求修正时，才使用脚本的 `--fix`，并先说明将修改哪些低风险项目；涉及语义、API、宏逻辑、include 依赖或所有权的修改必须给补丁建议，不自动改。
6. 输出按严重性排序：阻断/高风险、规范问题、可维护性建议。每项包含文件:行号、规则、原因、建议代码或操作、是否可自动修正。

## 输出要求

- 先给摘要：检查范围、采用的标准、问题数量、是否执行了修正。
- 不把编译错误、运行时 bug 或个人偏好伪装成风格违规。
- 对无法可靠判断的规则标记为“需人工确认”，并说明需要的上下文。
- 若执行修正，报告修改文件、未修改的高风险项，并展示关键 diff；不要声称已验证编译，除非确实运行了构建命令。

## 支持文件

- `references/style-rules.md`: 从参考图片整理的规则、例外和严重性。
- `references/cpp-style-guide-summary.md`: 面向人的全局地图、关键规则详解、历史原因和调查清单。
- `references/workflow.md`: 审查、建议和可选修正流程。
- `references/fallback.md`: 脚本失败或规则冲突时的处理。
- `scripts/cpp_style_check.py`: 无第三方依赖的启发式检查器，支持 JSON 报告和低风险修正。
- `examples/positive.md`、`examples/negative.md`: 触发与不触发示例。

完整结构化分析结果见 `reports/cpp-style-guide-analysis.html`；需要机器读取时使用同目录的 JSON 文件。
