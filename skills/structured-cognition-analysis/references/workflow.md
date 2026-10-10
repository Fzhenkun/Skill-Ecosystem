# Workflow / 工作流

## Analysis Loop

1. **Scope / 界定对象**: restate the subject in one sentence. If it is trivial, answer directly and skip the report. If ambiguous, ask one clarifying question about the subject.
2. **Gather / 收集依据**: use user-provided material, workspace files, or available search tools. Mark every claim as `fact` / `inference` / `speculation`. Never fabricate sources.
3. **Analyze / 展开分析**: work through the 8 dimensions (see `framework.md`), prioritizing 1, 4, 7, 8. For hidden assumptions, list candidates, then test each with "if this were false, what breaks?".
4. **Synthesize / 综合**: write the conclusion: essence in one sentence, key risks, recommended stance, open questions.
5. **Report / 输出报告**: write the analysis JSON following `report-schema.md` (use the `reports/` folder or a path the user gives), then render:

```powershell
python scripts/render_report.py --input <analysis.json> --output <report.html>
```

6. **Verify / 验证**: confirm the script printed `Report written:` and the HTML file exists.
7. **Reply / 回复**: brief summary plus the report path, in the user's language (bilingual users: follow the language of the request).

## User-Original-Text Rule

Preserve user-provided names, quotes, numbers, paths and identifiers verbatim in the JSON and report. Do not clean up or translate them unless the user asks.

## Maintenance Loop

After real usage, record the failure type (false trigger, missed trigger, padded dimension, bad render, thin evidence) and fix the narrowest artifact: `SKILL.md` for routing, `framework.md` for questions, `scripts/` for rendering, `examples/` for invocation teaching. Re-run the audit:

```powershell
python <skill-lifecycle-engine>/scripts/maintain_skill.py --skill-dir <path-to-this-skill>
```
