# Manifest

## Purpose

Define what a skill can do, what it must include, and where its boundaries are. Read this file when deciding whether a skill is complete or when expanding an existing skill safely.

## Core Capabilities

1. Create a new skill from source requirements, raw notes, or an existing workflow.
2. Repair incomplete skill folders missing structure, metadata, references, or scripts.
3. Improve `SKILL.md` so triggering is sharper, less ambiguous, and easier for the agent to route, while enforcing the 1024-character description limit.
4. Refactor overloaded instructions into progressive-disclosure references.
5. Add execution helpers under `scripts/` for deterministic or repeated operations.
6. Add `examples/` with positive and negative cases to improve invocation quality.
7. Establish a maintenance loop for validation, iteration, and long-term updates.

## Required Structure

Minimum required:

- `SKILL.md` (frontmatter `name` equals folder name; `description` <= 1024 chars, target 300-800)

Recommended complete structure for this skill pattern:

- `references/manifest.md` (capability list)
- `references/workflow.md` (call/execution flow)
- `references/fallback.md` (error handling, two-layer Agent/User structure)
- `references/description-patterns.md`
- `scripts/` (single-command entry, e.g. `maintain_skill.py`)
- `examples/positive.md`, `examples/negative.md`

Optional: `assets/`, and `agents/openai.yaml` (Codex UI metadata only; not used by VS Code).

## Discovery Locations (VS Code / Copilot)

Project: `.github/skills/`, `.agents/skills/`, `.claude/skills/`. Personal: `~/.copilot/skills/`, `~/.agents/skills/`, `~/.claude/skills/`. Each skill is one folder containing `SKILL.md`. Use `/skills` in Copilot Chat to verify.

## Boundaries

This skill is for building and maintaining agent skills themselves.

Do use it for:

- skill architecture
- trigger design
- skill refactoring
- skill validation
- skill maintenance workflows

Do not use it for:

- ordinary application development unrelated to skills
- product docs that are not part of a skill package
- generic prompt writing unless it is specifically for skill triggering or skill operation

## Quality Bar

A production-quality skill should:

1. Trigger on the right problems and avoid false positives; description <= 1024 chars.
2. Keep `SKILL.md` concise enough to load comfortably into context.
3. Push detail into references instead of bloating the main file.
4. Expose narrow, repeatable execution paths for automation.
5. Fail safely with explicit recovery instructions.
6. Support future improvement without re-deriving the whole design.
