# Fallback Protocol

## Read This On First Failure

If any command, script, dependency lookup, or validation step fails, stop and read this file before trying alternative tools or edits.

## Agent Intervention

When a failure occurs, do not:

- rewrite unrelated scripts to force success
- copy authentication logic from another skill
- install random dependencies without evidence
- swap to a different unsafe workflow just to get an output
- silently degrade the task without telling the user

Correct behavior:

1. Identify the exact failing command, file, or dependency.
2. Determine whether the failure is structural, environmental, or content-related.
3. Apply the smallest safe fix.
4. If the fix requires user action or external state, present a direct recovery instruction.

## User-Facing Recovery Pattern

When user intervention is required, present:

1. The exact problem.
2. The exact command or action needed.
3. A request to reply after completion.

Example:

```text
The skill validation failed because SKILL.md is missing valid YAML frontmatter.
Please restore or update the frontmatter, then reply with: 已修复
```

## Common Failures

### Validation failure

Symptoms:

- missing `SKILL.md`
- invalid frontmatter
- invalid skill name
- missing description

Response:

1. Fix the specific file.
2. Re-run validation.

### Missing support files

Symptoms:

- references mentioned in `SKILL.md` do not exist
- `agents/openai.yaml` is stale or absent

Response:

1. Create the missing files.
2. Ensure file references match exact paths.

### Script failure

Symptoms:

- Python execution error
- bad path resolution
- encoding mismatch

Response:

1. Inspect the failing script.
2. Patch only the cause.
3. Re-run the exact command.

## Why This Matters

This protocol prevents wasteful improvisation loops. Good fallback behavior is part of the skill design, not an afterthought.
