# Unified Workflow / 统一工作流

The workflow is fixed; only investigation scale changes. Do not create separate templates for "complex" and "simple" subjects.

## 1. Scope the subject / 界定对象

State the object in one sentence, the user's decision or learning need, and the evidence boundary. Preserve the user's original names and paths. If the request is genuinely trivial, answer directly; do not manufacture a report.

Estimate scale:

- **Complex**: multiple components or actors, interactions, lifecycle, dependencies, history, or competing objectives.
- **Simple**: one concept, API, mechanism, short comparison, or bounded usage question.

This estimate controls map size and depth only. It does not change the workflow.

## 2. Build the global/context map / 建立全局或上下文地图

For a complex subject, map the system before deep reading:

- scope and non-goals;
- components, actors, ownership, and responsibilities;
- inputs, outputs, data/control flow, and dependencies;
- lifecycle, state transitions, external constraints, and failure surface;
- timeline or versions when history may explain current behavior.

For a simple subject, build the smallest useful context map: definition, neighboring concepts, caller/user, inputs/outputs, and where it sits in a real workflow. A map can be a short list; it does not need to be a diagram.

## 3. Identify key mechanisms / 识别关键机制

Explain the causal chain: **condition/input → mechanism → state change or decision → output/effect**. Select critical parts using impact, uncertainty, coupling, user consequence, or failure likelihood. In complex work, deep dive into selected parts only after the map; in simple work, this is usually the main body.

Use the eight questions as lenses, not mandatory headings:

1. What assumptions make it work?
2. What first principles or mechanisms explain it?
3. What goal and success measure does it serve?
4. What principal contradiction does it resolve?
5. What are its concrete components and terms?
6. How is it implemented or used?
7. What boundaries, costs, alternatives, and failure modes exist?
8. How did it evolve, and how can claims be verified?

## 4. Trace anomalous points / 追溯反常点

Flag choices that look irrational, overcomplicated, inconsistent, or obviously broken. For each:

1. describe the observation and why it is anomalous;
2. check current code, documentation, tests, version history, compatibility constraints, ownership boundaries, and prior incidents when available;
3. distinguish confirmed historical cause from plausible hypothesis;
4. state whether the old constraint still exists.

If no anomaly is found, say so briefly. Do not invent a historical narrative.

## 5. Analyze boundaries and costs / 分析边界与代价

Describe where the mechanism works, where it fails, and what it costs: performance, memory, complexity, operability, migration, safety, lock-in, or opportunity cost. Name viable alternatives and the condition under which each wins.

## 6. Verify with practice / 用实践验证

Choose the smallest useful check for each important claim:

- minimal runnable example or reproduction;
- source/code and configuration inspection;
- scenario walkthrough or counterexample;
- benchmark, measurement, log, or test;
- observable prediction that could falsify the claim.

Record the check, expected observation, result, and limits. A conceptual explanation alone is not verification.

## 7. Synthesize and output Markdown / 综合并输出 Markdown

End with:

- one-sentence essence;
- confirmed findings versus inferences;
- recommended stance or next action;
- key risks and boundary conditions;
- open questions and verification gaps;
- sources and artifacts inspected.

Write the final artifact as readable Markdown. JSON may be used as an intermediate input to `scripts/render_report.py`, but HTML is not the required deliverable.

## Evidence Discipline / 证据纪律

Label every substantive point as `fact`, `inference`, or `speculation`, with `high`, `medium`, or `low` confidence. If evidence is thin, lower confidence and list the missing evidence rather than filling the gap with confident prose.

## Maintenance Loop / 维护循环

After use, record the narrowest failure: wrong trigger, incomplete map, shallow mechanism, missed historical cause, weak verification, padded sections, or bad Markdown output. Fix the relevant reference, example, or script and rerun the skill audit.
