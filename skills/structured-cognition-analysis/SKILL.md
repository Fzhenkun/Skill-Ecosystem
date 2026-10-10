---
name: structured-cognition-analysis
description: "MUST USE to analyze a non-trivial subject (technology, method, product, theory, policy, organization, decision, project, concept) by its essence with an 8-dimension scaffold (hidden assumptions, rationale, goal, principal contradiction, content, means, boundaries & costs, evolution & verification) and deliver an HTML report. Use when asked to understand, evaluate, dissect, compare or critique something, or 'what is X really / why does X work / when does X fail / is X worth it'. Keywords: structured analysis, first principles, hidden assumptions, deep dive, analysis report. 必须使用:结构化分析、本质分析、基石假设、主要矛盾、边界与代价、深度拆解、分析报告、HTML报告、批判性分析。Do NOT use for trivial facts, simple lookups or ordinary coding. 不用于琐碎事实、简单查询、普通编码。"
---

# Structured Cognition Analysis / 结构化认知分析

A thinking scaffold, not a questionnaire: ask about **assumptions, contradictions, boundaries, verification**. `SKILL.md` is routing only; read the file you need from the table below.

## Trigger Scenarios / 触发场景

| Scenario / 场景 | Typical request / 典型请求 | Trigger keywords / 触发关键词 |
| --- | --- | --- |
| Understand something new / 了解新事物 | "What is X really?" / "X 的本质是什么？" | essence, first principles, 本质分析 |
| Evaluate worth or risk / 评估取舍 | "Is X worth it? When does it fail?" / "X 值不值得？何时失效？" | boundaries and costs, 边界与代价, 批判性分析 |
| Dissect a method or decision / 拆解方法决策 | "Dissect X: assumptions, costs" / "拆解 X 的假设与代价" | hidden assumptions, 基石假设, 主要矛盾 |
| Full report / 完整报告 | "Give me a structured analysis report" / "给我完整分析报告" | structured analysis, deep dive, HTML报告, 分析报告 |

## Route Before Reading / 按需读取

| Need | Read |
| --- | --- |
| Capability list, the 8 dimensions, boundaries | `references/manifest.md` |
| Step-by-step analysis and report-rendering flow | `references/workflow.md` |
| Probing questions per dimension | `references/framework.md` |
| JSON schema for the report | `references/report-schema.md` |
| Any error, missing tool, or thin evidence | `references/fallback.md` |
| Trigger / non-trigger samples | `examples/positive.md`, `examples/negative.md` |

## ⚠️ Hard Rules / 硬性规则

1. **Fact vs inference / 区分事实与推断**: label every claim `fact` / `inference` / `speculation` and every assumption or conclusion with confidence (high/medium/low). Never fabricate sources.
2. **No filler / 禁止硬凑**: a dimension with no real insight is marked "not applicable" with a reason. Do not force all 8.
3. **User text first / 用户原文优先**: keep user-provided names, quotes, numbers and paths verbatim; never rewrite, abbreviate or translate them. Wrong: user says "OKR 3.0 方案", report titled "OKR methodology". Right: "OKR 3.0 方案".
4. **Trivial subject / 琐碎对象**: answer directly and skip the report.
5. **Circuit breaker / 错误熔断**: on any script or command failure, stop and read `references/fallback.md` first. Do not edit the render script to force success, swap tools, or install guessed dependencies.

## Single-Command Render

```powershell
python scripts/render_report.py --input <analysis.json> --output <report.html>
```

Write the analysis JSON per `references/report-schema.md` first, then render. Reply with a brief summary and the report path, in the user's language.
