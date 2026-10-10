---
name: skill-lifecycle-engine
description: |
  **English**: Create, complete, optimize, and continuously maintain skills. Use when needs to create a new skill from scratch, repair an incomplete skill folder, improve SKILL.md triggering accuracy, split large instructions into progressive-disclosure references, add scripts/assets/examples, strengthen validation and fallback rules, or establish an iteration workflow for long-term skill maintenance. Trigger immediately for requests about skill creation, skill packaging, skill architecture, SKILL.md design, skill description tuning, trigger optimization, references routing, examples curation, maintenance workflow, or updating an existing skill to production quality. Do not use for ordinary app coding unless the main task is building or maintaining a skill itself.

  **中文**: 创建、完成、优化和持续维护技能。当需要从零开始创建新技能、修复不完整的技能文件夹、改进SKILL.md触发准确性、将大型指令拆分为渐进式参考文档、添加脚本/资产/示例、加强验证和回退规则，或建立长期技能维护工作流时，请使用此技能。对于关于技能创建、技能打包、技能架构、SKILL.md设计、技能描述优化、触发器优化、参考文档路由、示例管理、维护工作流或将现有技能更新到生产质量的请求，应立即触发此技能。不用于普通应用编码，除非主要任务是构建或维护技能本身。

  **Trigger Keywords** (EN): create skill, build skill, new skill, complete skill, missing SKILL.md, fix skill, optimize skill, trigger accuracy, skill packaging, skill architecture, SKILL.md design, description tuning, trigger optimization, references routing, examples curation, maintenance workflow, skill structure
  
  **触发关键词** (ZH): 创建技能, 构建技能, 新技能, 完成技能, 修复技能, 优化技能, 触发器, 技能打包, 技能架构, SKILL.md设计, 描述优化, 参考文档, 示例管理, 维护工作流, 技能结构
---

# Skill Lifecycle Engine

## Overview

Build and maintain skills with a stable, reusable structure instead of one-off `SKILL.md` files. Keep the main file focused on routing and operating rules, then push detail into `references/`, executable helpers into `scripts/`, and usage patterns into `examples/`.

## Use This Workflow

1. Inspect the target skill folder or the user's source material before writing anything.
2. Normalize the skill name to lowercase hyphen-case and keep it under 64 characters.
3. Ensure the folder has the minimum structure:
   - `SKILL.md`
   - `agents/openai.yaml`
   - `references/`
   - `scripts/` when deterministic or repeated actions are needed
   - `assets/` when templates or bundled files are needed
   - `examples/` when positive and negative invocation patterns improve reliability
4. Write a trigger-strong frontmatter description that states:
   - what the skill does
   - when it must be used
   - strong trigger phrases, synonyms, and bilingual keywords when relevant
   - explicit non-goals to avoid overlap with other skills
5. Keep `SKILL.md` short and operational. Route detailed reading to `references/`.
6. Add or update helper scripts so execution converges to a small number of commands.
7. Add examples that teach both correct invocation and failure modes.
8. Validate the skill structure and iterate after real usage.

## Route Before Reading

Read only the reference file needed for the current subtask:

| Need | Read |
| --- | --- |
| Understand the full capability inventory | `references/manifest.md` |
| Build or revise the execution/maintenance workflow | `references/workflow.md` |
| Handle errors, tool failures, or dependency gaps | `references/fallback.md` |
| Improve triggering, wording, or coverage | `references/description-patterns.md` |
| Check examples of good and bad invocations | `examples/positive.md` and `examples/negative.md` |

## Trigger Design Rules / 触发器设计规则

### English Version

Use a structured trigger table instead of prose whenever the target skill supports multiple scenarios.

| Scenario | Typical user request | Trigger keywords |
| --- | --- | --- |
| Create a new skill | "Create a skill for X" | create skill, build skill, new skill, scaffold skill |
| Repair an incomplete skill | "Complete this skill structure" | complete skill, missing SKILL.md, fix skill, repair skill |
| Optimize triggering | "Make this skill trigger more accurately" | trigger, description, frontmatter, invocation, improve accuracy |
| Split large instructions | "Refactor this huge skill into references" | progressive disclosure, references, split docs, refactor |
| Add maintenance loop | "Help me keep this skill updated" | maintain skill, optimize skill, improve skill, workflow |

Prefer explicit, high-signal nouns and verbs. Include Chinese and English trigger words when the users operate bilingually.

### 中文版本

在目标技能支持多个场景时，使用结构化的触发表而不是散文。

| 场景 | 典型用户请求 | 触发关键词 |
| --- | --- | --- |
| 创建新技能 | "为X创建一个技能" | 创建技能, 构建技能, 新技能, 搭建技能 |
| 修复不完整的技能 | "完成这个技能结构" | 完成技能, 缺少SKILL.md, 修复技能, 修复结构 |
| 优化触发器 | "使这个技能更准确地触发" | 触发器, 描述, 前置元数据, 调用, 提高精度 |
| 拆分大型指令 | "将这个巨大的技能重构为参考文档" | 渐进式披露, 参考文档, 拆分文档, 重构 |
| 添加维护循环 | "帮助我保持这个技能的更新" | 维护技能, 优化技能, 改进技能, 工作流 |

## Hard Rules

`Warning`: preserve user-provided names, paths, code snippets, URLs, schema names, and literal task text unless the user explicitly asks for rewriting.

`Warning`: when a script or command fails, read `references/fallback.md` before improvising. Do not silently swap tools, invent auth flows, or rewrite unrelated files as a recovery shortcut.

Keep execution entry points narrow. If the skill repeatedly performs the same transformation, add or update a script under `scripts/` and document a single invocation path.

## Deliverables Checklist

Before finishing a skill creation or maintenance task, ensure:

| Item | Required outcome |
| --- | --- |
| `SKILL.md` | concise routing instructions plus strong description |
| `agents/openai.yaml` | UI metadata consistent with the skill |
| `references/manifest.md` | capability inventory and boundaries |
| `references/workflow.md` | creation, optimization, and maintenance process |
| `references/fallback.md` | error interception and user-facing recovery rules |
| `references/description-patterns.md` | patterns for high-quality descriptions |
| `examples/` | positive and negative trigger examples |
| `scripts/maintain_skill.py` | maintenance helper for structure checks |

## Single-Command Maintenance

Use this command when the skill folder exists and needs a quick structural audit:

```powershell
python scripts/maintain_skill.py --skill-dir <path-to-skill>
```

If the user asks for a new skill from scratch, initialize or scaffold the folder first, then apply this skill's structure and references.
