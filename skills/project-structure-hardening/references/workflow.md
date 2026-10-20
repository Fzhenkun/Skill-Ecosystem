# 目录固化工作流

## 目标路径

脚本检查并按需创建：

- `AGENTS.md`
- `CLAUDE.md`
- `.github/copilot-instructions.md`
- `.agents/skills/<name>/SKILL.md`
- `agent-os/standards/`
- `openspec/changes/`
- `openspec/specs/`
- `packages/`
- 每个 `packages/<直接子目录>/AGENTS.md`

## 文件策略

- 缺失的 `AGENTS.md` 使用最小中文模板，声明它是全局规则唯一真相源，并记录目录约定；不猜测构建命令、代码风格或业务规则。
- 缺失的 `CLAUDE.md` 写入单行 `@AGENTS.md`。
- 缺失的 `.github/copilot-instructions.md` 写入指向根 `AGENTS.md` 的单行说明。
- 缺失的 package 规则文件只说明“暂无专属规则，通用规则以项目根 AGENTS.md 为准”，不复制根文件内容。
- 缺失的 Skill 文件从当前 Skill 自身复制；已有 Skill 文件跳过。

## 幂等和冲突

先完成全部路径类型预检，再开始写入。已存在的目录和文件返回 `existing`，缺失项返回 `created`，不重复追加文本。若目标路径已经是错误类型，返回 `conflict` 并且本次不写入任何目标。

## 验证

`--apply` 完成后再次不带 `--apply` 运行脚本。第二次运行应只报告 `existing`，且不修改文件。若发现 `packages/<name>` 是普通文件，不创建 `packages/<name>/AGENTS.md`，而是报告冲突。

