---
name: structured-cognition-analysis
description: |
  **English**: Proactively analyze any non-trivial thing (a technology, method, product, theory, policy, organization, decision, project, concept) by its essence and characteristics using an 8-dimension cognitive scaffold (hidden assumptions, rationale, goal, principal contradiction, content, means, boundaries & costs, evolution & verification), then deliver an HTML report. Use when the user wants to understand, evaluate, dissect, compare, or critique something new or unfamiliar, asks "what is X really / why does X work / when does X fail / is X worth it", or wants a structured deep-dive report. Do not use for trivial facts, simple lookups, or ordinary coding tasks; do not force all 8 dimensions when some do not apply.

  **中文**: 基于“结构化认知”八维脚手架（基石假设、依据原理、目标、主要矛盾、主要内容、主要手段、边界与代价、演化与验证），根据事物的本质与特点主动展开结构化分析，并输出 HTML 报告。当用户想了解、评估、拆解、对比或批判某个新事物/陌生事物（技术、方法、产品、理论、政策、组织、决策、项目、概念），或询问“X 的本质是什么/为什么成立/何时失效/值不值得”，或需要结构化深度分析报告时使用。不用于琐碎事实、简单查询或普通编码；不适用的维度不要硬凑。

  **Trigger Keywords** (EN): structured analysis, cognitive analysis, first principles, hidden assumptions, essence, principal contradiction, boundaries and costs, deep dive, analysis report, HTML report, understand X, critique X

  **触发关键词** (ZH): 结构化分析, 认知分析, 本质分析, 隐性假设, 基石假设, 主要矛盾, 边界与代价, 深度拆解, 分析报告, HTML报告, 了解新事物, 批判性分析
---

# Structured Cognition Analysis / 结构化认知分析

## Overview / 概述

A thinking scaffold, not a questionnaire. The goal is the habit of asking about **assumptions, contradictions, boundaries, and verification** — not filling every cell. Adapt depth to the subject; skip or merge dimensions that do not apply and say why.

这是思维脚手架，而非标准问卷。重点是养成追问假设、矛盾、边界、验证的习惯，而不是填满所有维度。按对象调整深度，不适用的维度可跳过或合并，并说明原因。

## The 8 Dimensions / 八个维度

| # | Dimension / 维度 | Core question / 核心追问 |
| --- | --- | --- |
| 1 | Foundational & hidden assumptions / 基石假设·隐性假设 | What premises does it stand on? / 它建立在什么前提上？ |
| 2 | Rationale & first principles / 依据·基本原理 | Why does it hold? / 为什么成立？ |
| 3 | Goal / 目标 | What does it aim to achieve? / 要达成什么？ |
| 4 | Principal contradiction / 主要矛盾 | What problem does it resolve? / 解决什么问题？ |
| 5 | Main content / 主要内容 | What is it? / 是什么？ |
| 6 | Means & implementation / 主要手段·实现 | How is it done? / 怎么做？ |
| 7 | Boundaries & costs / 边界与代价 | When does it fail? What does it cost? Alternatives? / 何时失效？代价？替代方案？ |
| 8 | Evolution & verification / 演化与验证 | Where did it come from? How to verify? Counterexamples? / 从何而来？如何验证？有何反例？ |

Details and probing questions: `references/framework.md`.

## Workflow / 工作流

1. **Scope / 界定对象**: Restate the subject in one sentence. If it is trivial, answer directly and skip the report (the framework over-analyzes trivial things). 若对象琐碎，直接回答，不出报告。
2. **Gather / 收集依据**: Use user-provided material, workspace files, or available search tools. Mark every claim as *fact / inference / speculation* (事实/推断/推测). Never fabricate sources.
3. **Analyze / 展开分析**: Work through the 8 dimensions, prioritizing 1, 4, 7, 8 (assumptions, contradiction, boundaries, verification). Hidden assumptions are hard to dig out: list candidates, then test each by asking "if this were false, what breaks?".
4. **Synthesize / 综合**: Write a short conclusion: essence in one sentence, key risks, recommended stance, open questions.
5. **Report / 输出报告**: Write the analysis to a JSON file following `references/report-schema.md`, then render HTML:

```powershell
python scripts/render_report.py --input <analysis.json> --output <report.html>
```

6. Reply with a brief summary and the report path. Respond in the user's language (bilingual users: follow the language of the request).

## Hard Rules / 硬性规则

`Warning`: separate fact from inference; label confidence (high/medium/low) on assumptions and conclusions. 区分事实与推断，标注置信度。

`Warning`: do not pad dimensions with generic filler. A dimension with no real insight should be marked "not applicable" with a reason. 无实质内容的维度标注“不适用”并说明原因。

`Warning`: preserve user-provided names, quotes, and numbers verbatim. If the render script fails, read `references/fallback.md` before improvising.

## Route Before Reading / 按需读取

| Need | Read |
| --- | --- |
| Probing questions per dimension | `references/framework.md` |
| JSON schema for the report | `references/report-schema.md` |
| Failures, missing tools, thin evidence | `references/fallback.md` |
| Trigger / non-trigger samples | `examples/positive.md`, `examples/negative.md` |
