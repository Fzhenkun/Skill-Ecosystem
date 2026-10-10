# Positive Examples

## Example 1

User request:

```text
通过参考这份文档，帮我创建一个完整的 skill，包含 SKILL.md、references、scripts 和维护流程。
```

Why this skill should trigger:

- explicit request to create a skill
- asks for complete skill structure
- asks for maintenance workflow

## Example 2

User request:

```text
Optimize this existing skill so it triggers more accurately and move the long instructions into references.
```

Why this skill should trigger:

- focuses on skill optimization
- requests progressive disclosure refactor

## Example 4

User request:

```text
我的 skill 在 Copilot Chat 里找不到，帮我检查 description 和目录。
```

Why this skill should trigger:

- debugging skill discovery and frontmatter limits (description <= 1024 chars)

## Example 3

User request:

```text
给我补全这个 skill 的 fallback 文档和 examples，让它便于后续持续维护。
```

Why this skill should trigger:

- asks for skill completion
- asks for fallback and examples
- asks for continuous maintenance
