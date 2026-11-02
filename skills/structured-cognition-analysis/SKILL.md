---
name: structured-cognition-analysis
description: "MUST USE for non-trivial analysis of a technology, method, product, system, project, policy, theory, decision, or knowledge request about what it is, how it works, why it exists, when it fails, or whether it fits. Follow one scalable flow: scope, context map, key mechanisms, anomaly history, boundaries, practice verification, then Markdown. Complex subjects expand the map and deepen selected parts; simple subjects shrink the map and focus on use, mechanism, applicability, limitations, and likely problems. Separate fact, inference, and speculation. Keywords: structured analysis, first principles, system map, mechanism, root cause, historical reason, boundary, verification, Markdown, 结构化分析,全局梳理,关键机制,历史原因,适用边界,实践验证,Markdown文档. Do NOT use for trivial facts, translation, or ordinary coding."
---

# Structured Cognition Analysis / 结构化认知分析

Use one scalable cognition flow, not a fixed questionnaire:

**界定对象 → 建立全局/上下文地图 → 识别关键机制 → 追溯反常点 → 分析边界与代价 → 用实践验证 → 输出 Markdown**

The same flow applies to a complex system and a single concept. Complexity changes the breadth of the map and the depth of selected investigations; it does not create a second framework.

## Trigger Scenarios / 触发场景

| Scenario / 场景 | Typical request / 典型请求 | Trigger keywords / 触发关键词 |
| --- | --- | --- |
| Understand or explain / 理解解释 | "What is X really? How does it work?" / "X 的本质和机制是什么？" | essence, mechanism, first principles, 本质, 原理, 机制 |
| Evaluate or compare / 评估比较 | "When does X fail? Is it suitable?" / "X 的边界、代价和替代方案是什么？" | boundary, cost, trade-off, failure, 适用边界, 代价, 对比 |
| Investigate a system / 系统调查 | "Map this architecture and deep dive into risky parts." / "先梳理全局，再分析关键部分。" | system map, architecture, root cause, historical reason, 全局梳理, 深挖, 历史原因 |
| Produce a report / 输出报告 | "Give me a structured analysis in Markdown." / "输出分析文档。" | structured analysis, deep dive, Markdown report, 结构化分析, Markdown文档 |

## Route Before Reading / 按需读取

| Need / 需要 | Read / 读取 |
| --- | --- |
| Capability, scope, quality bar | `references/manifest.md` |
| Unified investigation loop and complexity scaling | `references/workflow.md` |
| Prompts for map, mechanism, anomalies, boundaries, verification | `references/framework.md` |
| JSON intermediate fields and Markdown output contract | `references/report-schema.md` |
| Any command, script, dependency, or evidence failure | `references/fallback.md` |
| Trigger teaching | `examples/positive.md`, `examples/negative.md` |

## Hard Rules / 硬规则

1. **One flow, scalable depth / 一个流程、深度伸缩**: always follow the seven-step flow above. A complex subject requires a system/context map and selected deep dives; a simple subject uses a small context map and concise mechanism analysis.
2. **Map before detail / 先地图后细节**: before explaining a complex system, identify scope, actors/components, inputs/outputs, control or data flow, dependencies, lifecycle, and failure surface. Do not claim a local part is important without showing its place in the whole.
3. **Anomaly backtracking / 反常点追溯**: when a design seems irrational, overly complex, inconsistent, or obviously broken, record the observation and investigate historical constraints, compatibility, migration, ownership, or prior incidents. Mark evidence versus hypothesis; never invent history.
4. **Practice as evidence / 实践作为抓手**: for each key mechanism or risk, provide a minimal experiment, code inspection, scenario walkthrough, measurement, or falsifiable check. State what the check proves and what it does not.
5. **Fact versus inference / 事实与推断分离**: label claims `fact`, `inference`, or `speculation`; attach confidence `high`, `medium`, or `low`. Never fabricate sources.
6. **No forced sections / 不硬凑章节**: omit or mark a section not applicable with a reason when evidence does not support it. Do not pad a simple question into eight artificial dimensions.
7. **User text first / 用户原文优先**: preserve user-provided names, quotes, numbers, paths, and identifiers verbatim.
8. **Markdown artifact / Markdown 产物**: the final report must be a readable `.md` document. JSON is only an optional intermediate representation.
9. **Circuit breaker / 错误熔断**: on any command, script, dependency, or thin-evidence failure, stop and read `references/fallback.md` before acting.

## Single-Command Render / 单命令生成

```powershell
python scripts/render_report.py --input <analysis.json> --output <report.md>
```

Write the intermediate JSON using `references/report-schema.md`, render the Markdown file, verify that the script printed `Report written:` and that the `.md` file exists, then reply with a concise summary and report path in the user's language.
