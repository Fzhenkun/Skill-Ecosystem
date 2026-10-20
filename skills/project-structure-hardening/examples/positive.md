# 正例

## 示例 1：已有项目补齐结构

用户：

```text
给 D:\projects\demo 补齐 AGENTS.md、openspec 和 agent-os 目录，已有文件不要覆盖。
```

应触发：明确要求已有项目补齐目录且保护已有内容。

## 示例 2：新项目初始化

用户：

```text
为新项目创建跨 Codex、Copilot、Claude Code 共用的 Agent 目录结构，skill 名称为 release-check。
```

应触发：新项目初始化，并明确提供了 `<name>`。

