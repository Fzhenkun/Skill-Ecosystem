---
name: smart-execution-guide-builder
description: "MUST USE when the user asks to turn one or more local Markdown notes, study materials, interview notes, or domain documents into a practical execution guide based on SMART. The skill inventories all requested .md files, synthesizes domain knowledge without changing source files, prioritizes content, creates time-boxed actions, templates, progress tracking, review questions, and measurable acceptance criteria. Trigger phrases include SMART方案、SMART计划、整理成指南、学习路线、刷题指南、执行计划、进度复盘表、文档汇总、笔记归纳、Markdown转可执行方案、study plan、action plan、execution guide. Do NOT use for ordinary summarization, direct translation, blog publishing, or editing the original notes unless the user explicitly requests those separately."
---

# SMART Execution Guide Builder

把分散的 Markdown 材料整理成“能执行、能记录、能复盘、能验收”的 SMART 指南。默认保留源文件不变，并根据材料所属领域补充必要的结构化知识。

## 触发与边界

| 场景 | 典型请求 | 触发关键词 |
|---|---|---|
| 新建执行指南 | 把一批笔记整理成有时间表的学习/准备指南 | SMART、整理成指南、学习路线、执行计划 |
| 领域专项方案 | 根据题库、面试资料、技术文档生成训练方案 | 刷题指南、面试准备、训练计划、专项复习 |
| 进度管理补充 | 给已有指南添加进度表、复盘表和验收标准 | 进度记录、复盘表、完成度、下一步重点 |
| 指南迭代 | 根据执行反馈调整优先级和计划 | 优化计划、错题复盘、调整重点、二轮复习 |

不要把它用于只要求摘要、翻译、改写原文、发布博客或普通应用开发的请求。若用户同时要求发布博客，先完成指南，再交给专门的博客发布技能处理。

## 工作方式

1. 读取用户明确指定的参考文档、输入目录和所有相关 Markdown；保留用户提供的路径、文件名和限定条件原文。输出先列“已读取文件 / 未找到文件”。
2. 先盘点材料：文件清单、主题、题目/章节、重复内容、缺口和已有模板。
3. 按领域知识重新组织内容，不做文件拼接。把“识别信号、核心方法、易错点、验证方式”提炼出来。
4. 生成 SMART 目标：
   - S：具体到主题、能力和产出；
   - M：用题数、时间、正确率、独立完成率、复盘次数等衡量；
   - A：拆成可在单次学习时段完成的动作；
   - R：说明与用户目标、面试或实际工作之间的关系；
   - T：给出首轮、复习轮和截止时间。
5. 按 P0/P1/P2 或同等优先级分层，优先覆盖高频、高收益、强依赖和高风险内容。
6. 为每个阶段提供：学习重点、具体任务、输出物、验收条件和下一步动作。
7. 必须加入执行进度记录表、单项复盘表、周期复盘表和“当前重点”判断规则。
8. 以新文件输出指南，不修改任何原始 Markdown；若用户没有指定输出路径，放在输入目录并使用清晰的中文文件名。
9. 交付前核对：所有源文件均被纳入索引或主题归纳，SMART 五维完整，计划可执行，表格可填写，原文未被改动。

### 失败处理与检查点

| 触发条件 | 必须执行 |
|---|---|
| 输入路径不存在或没有 `.md` 文件 | 停止生成，列出实际扫描路径，请用户补充文件；不得用虚构材料填充指南 |
| 文件编码无法读取 | 保留原路径，先尝试 UTF-8；仍失败则记录文件名和错误，继续处理可读文件并标注覆盖缺口 |
| 多份材料对同一事实或要求冲突 | 在“待确认事项”表中并列来源，不擅自裁决；计划只使用已确认内容 |
| 目标没有截止日期或可量化指标 | 生成最小可执行草案，但把缺少项列为阻塞条件，并要求用户补齐后再承诺完成日期 |
| 输出路径已存在 | 停止覆盖，展示目标路径并请求用户选择新文件名或明确覆盖 |

🔴 **CHECKPOINT：** 在写入最终指南前，展示“材料覆盖、SMART 五维、阶段任务、验收标准和未决问题”摘要；确认前只输出草稿，不写入最终文件。

## 反例与黑名单

- 不把摘要、翻译或原文改写伪装成执行指南。
- 不修改、覆盖或重命名用户的原始 Markdown。
- 不在输入缺失、来源冲突或目标不可量化时编造材料、日期或验收结果。
- 不把任务清单写成没有时间盒、输出物和验收条件的愿望清单。
- 不未经确认覆盖已有输出文件，也不把未决事项隐藏在最终结论中。

## 输出要求

默认使用 Markdown，建议包含：

- 标题和目标说明
- SMART 总目标
- 材料覆盖范围与优先级
- 领域知识/题型/主题框架
- 通用执行流程或方法模板
- 分阶段计划
- 每次任务的执行节奏
- 进度记录与复盘表
- 错误/问题记录模板
- 验收标准和面向截止日期的速记清单
- 原始资料索引

详细组织规则见 [references/workflow.md](references/workflow.md)，可直接套用的章节骨架见 [references/output-template.md](references/output-template.md)。遇到失败、编码异常、输入缺失或输出冲突时，先读 [references/fallback.md](references/fallback.md)。

