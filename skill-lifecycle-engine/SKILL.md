---
name: skill-lifecycle-engine
description: Create, complete, optimize, and continuously maintain skills. Use when needs to create a new skill from scratch, repair an incomplete skill folder, improve SKILL.md triggering accuracy, split large instructions into progressive-disclosure references, add scripts/assets/examples, strengthen validation and fallback rules, or establish an iteration workflow for long-term skill maintenance. Trigger immediately for requests about skill creation, skill packaging, skill architecture, SKILL.md design, skill description tuning, trigger optimization, references routing, examples curation, maintenance workflow, or updating an existing skill to production quality. Do not use for ordinary app coding unless the main task is building or maintaining a skill itself.
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

## Trigger Design Rules

Use a structured trigger table instead of prose whenever the target skill supports multiple scenarios.

| Scenario | Typical user request | Trigger keywords |
| --- | --- | --- |
| Create a new skill | "Create a skill for X" | create skill, build skill, new skill |
| Repair an incomplete skill | "Complete this skill structure" | complete skill, missing SKILL.md, fix skill |
| Optimize triggering | "Make this skill trigger more accurately" | trigger, description, frontmatter, invocation |
| Split large instructions | "Refactor this huge skill into references" | progressive disclosure, references, split docs |
| Add maintenance loop | "Help me keep this skill updated" | maintain skill, optimize skill, improve skill |

Prefer explicit, high-signal nouns and verbs. Include Chinese and English trigger words when the users operate bilingually.

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
