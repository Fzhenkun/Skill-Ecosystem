# Fallback Protocol / 故障处理协议

Two layers: the **Agent layer** controls the agent, the **User layer** is copy-ready text for the user. Read this file at the first failure of any command, script, dependency lookup or audit.

## Layer 1: Agent Intervention / Agent 拦截指令

`⚠️` Stop the task at the first failure. Then:

Forbidden:

- editing scripts or local tests just to make them pass
- swapping to a different tool or an unsafe fallback
- installing guessed dependencies without evidence
- copying authentication logic from another skill
- silently degrading or skipping the task without telling the user

Required:

1. Identify the exact failing command, file or text.
2. Classify it as structural, environmental or content-related.
3. Apply the smallest safe fix only when the cause is in the skill's own files.
4. If user action or external state is needed, present the matching User Fix below verbatim and wait for the reply "已修复".

## Layer 2: Errors and User Fixes / 错误现象与用户修复

### E1 `[FAIL] description is N chars; hard limit is 1024`

Cause: the description exceeds the VS Code limit; the skill may not load in Copilot Chat.

Agent fix: shorten it (merge duplicated bilingual sentences, cut repeated synonyms), keep "when to use" and "do not use", re-run the audit. No user action needed.

### E2 `[FAIL] SKILL.md has no valid YAML frontmatter` / `name ... must match folder name`

Agent fix: restore `---` delimiters; set `name` equal to the folder name in lowercase hyphen-case. Re-run the audit.

### E3 `[FAIL] SKILL.md references missing path: <path>`

Agent fix: create the missing file or correct the path. Re-run the audit.

### E4 Python or script execution error (path, encoding, missing interpreter)

Agent fix: inspect the failing script, patch only the cause, re-run the exact command. If `python` is unavailable, show:

```text
Detected: Python is not available, so the audit cannot run.
Please install Python 3 or add it to PATH, then reply: 已修复
```

### E5 Skill installed but not found in Copilot Chat

Show the user:

```text
Detected: the skill is not listed in Copilot Chat.
Please check, in order:
1. The folder is under .github/skills/, .agents/skills/, .claude/skills/ (project) or ~/.copilot/skills/, ~/.agents/skills/, ~/.claude/skills/ (personal).
2. The audit prints no [FAIL] (especially description <= 1024 chars).
3. Run Developer: Reload Window, then type /skills in chat.
Reply: 已修复
```

## Why This Matters

Without a circuit breaker the agent enters improvisation loops that inflate token cost and push the context toward truncation.
