---
name: skill-lifecycle-engine
description: "MUST USE immediately when the user asks to create, complete, repair, optimize, refactor, validate or maintain a skill: SKILL.md, frontmatter description, trigger accuracy, references/scripts/examples, fallback rules, maintenance workflow. Keywords: create skill, new skill, fix skill, optimize skill, skill packaging, skill architecture, description tuning, trigger optimization, references routing, progressive disclosure. 必须使用:创建技能、新技能、完善/修复技能、优化技能、技能打包、描述优化、触发优化、拆分references、维护工作流。Do NOT use for ordinary app coding, generic prompt writing, or analysis unrelated to skills. 不用于普通编码、通用提示词、与技能无关的分析。"
---

# Skill Lifecycle Engine

`SKILL.md` is routing only. Read the file you need from the table below; do not load everything.

## Trigger Scenarios / 触发场景

| Scenario / 场景 | Typical request / 典型请求 | Trigger keywords / 触发关键词 |
| --- | --- | --- |
| Create a new skill / 创建新技能 | "Create a skill for X" / "为X创建一个技能" | create skill, new skill, scaffold skill, 创建技能, 新技能 |
| Repair incomplete skill / 修复技能 | "Complete this skill structure" / "完成这个技能结构" | fix skill, missing SKILL.md, repair skill, 修复技能, 补全技能 |
| Tune triggering / 优化触发 | "Make it trigger more accurately" / "让它触发更准确" | description, frontmatter, trigger, 描述优化, 触发优化 |
| Split large skill / 拆分大技能 | "Move this into references" / "拆到references" | progressive disclosure, references, 渐进式披露, 拆分 |
| Maintain over time / 持续维护 | "Keep this skill updated" / "持续维护这个技能" | maintain skill, optimize skill, 维护技能, 优化技能 |

## Route Before Reading / 按需读取

| Need | Read |
| --- | --- |
| What the skill can do, required structure, install locations | `references/manifest.md` |
| Creation, optimization, maintenance steps | `references/workflow.md` |
| Any error, tool failure, or audit `[FAIL]` | `references/fallback.md` |
| Writing or tuning a description | `references/description-patterns.md` |
| Good and bad invocation samples | `examples/positive.md`, `examples/negative.md` |

## ⚠️ Hard Rules / 硬性规则

1. **Description ≤ 1024 characters** (VS Code limit; target 300–800), counted on the final text including Chinese. Never deliver a skill over the limit: shorten repeated synonyms and duplicated bilingual sentences, but keep the "when to use" and "do not use" parts. 描述超过 1024 字符禁止交付。
2. **User text first / 用户原文优先**: pass paths, URLs, code, names and literal prompts verbatim; never rewrite, abbreviate or translate them. Wrong: user gives `C:\Users\me\Desktop\skills工程\x.txt`, agent writes "the desktop notes file". Right: use the path exactly.
3. **Circuit breaker / 错误熔断**: on any command, script or audit failure, stop and read `references/fallback.md` first. Do not edit scripts to force success, swap tools, install guessed dependencies, or copy auth logic from other skills.
4. **Audit before delivery / 交付前审计**: run the command below, fix every `[FAIL]`, re-run, then tell the user the final description length. Re-check rule 1.

## Single-Command Audit

```powershell
python scripts/maintain_skill.py --skill-dir <path-to-skill>
```

Exit code 1 means blocked. For a new skill, create the folder and `SKILL.md` first, then run it.
