# Fallback Protocol / 故障处理协议

Two layers: the **Agent layer** controls the agent, the **User layer** is copy-ready text for the user. Read this file at the first failure of any script, command or dependency.

## Layer 1: Agent Intervention / Agent 拦截指令

`⚠️` Stop at the first failure. Then:

Forbidden:

- editing `render_report.py` just to make it pass
- swapping to another tool or an unsafe fallback
- installing guessed dependencies without evidence
- inventing sources or data to fill thin evidence
- silently degrading the task without telling the user

Required:

1. Identify the exact failing command, file or error text.
2. Classify it as structural, environmental or content-related.
3. Apply the smallest safe fix only when the cause is in the analysis JSON.
4. If user action or external state is needed, present the matching User Fix below verbatim and wait for the reply "已修复".

## Layer 2: Errors and User Fixes / 错误现象与用户修复

### E1 `ERROR: JSON must contain 'title' and a list of 'lenses' or 'dimensions'` or JSON decode error

Agent fix: correct the JSON against `report-schema.md` without altering analysis content. Re-run the exact command.

### E2 `python` is not available

Do not improvise. Tell the user, and offer a hand-authored Markdown report in the same section order, stating it was not script-rendered. Show:

```text
Detected: Python is not available, so the Markdown report cannot be rendered by script.
Please install Python 3 or add it to PATH, then reply: 已修复
```

### E3 Output path not writable

Report the error and propose an alternate path; do not silently write elsewhere. Show:

```text
Detected: the output path is not writable.
Please choose another folder or fix permissions, then reply: 已修复
```

### E4 Thin evidence or no search tool

Analyze from provided material and general knowledge; mark points `inference` / `speculation` with low confidence and list the gaps under open questions. No user action needed.

### E5 Subject is ambiguous

Ask one clarifying question about the subject before analyzing.

### E6 Skill installed but not found in Copilot Chat

```text
Detected: the skill is not listed in Copilot Chat.
Please check, in order:
1. The folder is under .github/skills/, .agents/skills/, .claude/skills/ (project) or ~/.copilot/skills/, ~/.agents/skills/, ~/.claude/skills/ (personal).
2. The description is <= 1024 characters.
3. Run Developer: Reload Window, then type /skills in chat.
Reply: 已修复
```

## Why This Matters

Without a circuit breaker the agent enters improvisation loops that inflate token cost and push the context toward truncation. Never invent sources, citations, or data.
