# Workflow

## Creation Loop

1. Read the user's source material, existing skill, or target workflow.
2. Identify repeated actions, reference-heavy content, and likely trigger phrases.
3. Decide the folder structure and only add directories that earn their keep.
4. Draft `SKILL.md` with strong frontmatter and routing rules.
5. Write support files in `references/`, `scripts/`, `examples/`, and `assets/` as needed.
6. Validate and correct naming, metadata, and missing files.

## Optimization Loop

Use this loop when a skill exists but performs poorly.

1. Inspect whether the description actually covers the user requests that should trigger it.
2. Check whether `SKILL.md` contains detailed material that belongs in `references/`.
3. Find repeated manual steps that should become scripts.
4. Add positive and negative examples for ambiguous trigger cases.
5. Re-run validation and compare the revised structure against the original problem.

## Continuous Maintenance Loop

Use this loop after real usage.

1. Record where the skill failed:
   - false trigger
   - missed trigger
   - incomplete capability
   - unclear execution
   - poor error recovery
2. Update the narrowest artifact that fixes the problem:
   - change `SKILL.md` for routing rules
   - change `references/*.md` for deeper guidance
   - change `scripts/` for deterministic execution
   - change `examples/` for invocation teaching
3. Validate again.
4. Keep the fix local and surgical. Do not rewrite the whole skill without cause.

## Execution Convergence Rule

When a workflow repeatedly requires multiple fragile steps, converge it into one documented command or one small script entry point. This reduces drift, token waste, and recovery chaos.

## User-Original-Text Rule

Preserve user-provided text verbatim when passing:

- file paths
- URLs
- SQL or code snippets
- table names
- identifiers
- literal prompts

Do not "clean up" or translate these values unless the user asks for rewriting.
