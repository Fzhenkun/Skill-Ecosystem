# Manifest / 能力清单

## Purpose

Full capability inventory and boundaries. Read this when deciding whether the skill fits a request or what a complete analysis contains.

## Core Capabilities

1. Scope a subject in one sentence and decide whether it deserves analysis.
2. Analyze it through the 8 dimensions, prioritizing 1, 4, 7, 8.
3. Separate fact, inference and speculation, and label confidence.
4. Synthesize: essence in one sentence, key risks, recommended stance, open questions.
5. Render a self-contained HTML report through `scripts/render_report.py`.

## The 8 Dimensions / 八个维度

| # | Dimension / 维度 | Core question / 核心追问 |
| --- | --- | --- |
| 1 | Foundational & hidden assumptions / 基石假设·隐性假设 | What premises does it stand on? |
| 2 | Rationale & first principles / 依据·基本原理 | Why does it hold? |
| 3 | Goal / 目标 | What does it aim to achieve? |
| 4 | Principal contradiction / 主要矛盾 | What problem does it resolve? |
| 5 | Main content / 主要内容 | What is it? |
| 6 | Means & implementation / 主要手段·实现 | How is it done? |
| 7 | Boundaries & costs / 边界与代价 | When does it fail? What does it cost? Alternatives? |
| 8 | Evolution & verification / 演化与验证 | Where did it come from? How to verify? Counterexamples? |

Probing questions per dimension: `framework.md`.

## Required Structure

- `SKILL.md` (routing only; description <= 1024 chars)
- `references/`: `manifest.md`, `workflow.md`, `framework.md`, `report-schema.md`, `fallback.md`
- `scripts/render_report.py` (single entry point)
- `examples/positive.md`, `examples/negative.md`

## Boundaries

Do use it for: understanding, evaluating, dissecting, comparing or critiquing a technology, method, product, theory, policy, organization, decision, project or concept.

Do not use it for: trivial facts, simple lookups, ordinary coding, translation, or trivial choices (the framework over-analyzes small things).

## Quality Bar

1. Every dimension is either substantive or explicitly "not applicable" with a reason.
2. Claims are labeled by type and confidence; no invented sources.
3. Hidden assumptions are stress-tested with "if this were false, what breaks?".
4. The HTML report renders from valid JSON in one command.

## Limits / 局限

High threshold: hidden assumptions are hard to excavate. Over-analysis risk on trivial subjects.
