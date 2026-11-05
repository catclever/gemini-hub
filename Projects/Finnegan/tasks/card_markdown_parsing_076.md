---
id: card_markdown_parsing_076
title: Support Markdown Syntax Parsing for Cards in Both Focus and Scattered Modes
status: completed
priority: high
tags:
- frontend
- svelte
- markdown
- typography
- jules
session: conversation://58c97e35-a614-4542-ad8d-16f08d35616c
---

## 需求描述
根据 `features/卡片支持md格式解析.md`：
- 支持 both 聚焦态 and 散落态的 Markdown 语法解析。
- 在前端封装或集成轻量 Markdown 解析组件（可使用轻量库如 marked 或同等稳定轻量方案），支持加粗、斜体、各级标题、列表、代码块、行内代码与引用。
- **散落态（200x190）**：紧凑排版适配，支持行内 Markdown 格式（粗体、行内代码、短列表等），标题自适应降级，超长文本行数截断（line-clamp），保持散落态卡片规整。
- **聚焦态（420x420）**：全量 Markdown 排版展示，优美的行距、内联样式与代码块配色。
- 适配范围涵盖 `ThoughtCardBody.svelte`、`NoteCardBody.svelte` 以及其它卡片正文。

## 验收标准
- [ ] 卡片在散落态和聚焦态均能正确解析 Markdown 语法。
- [ ] 散落态卡片不会因 Markdown 元素过大而破损溢出。
- [ ] 前端测试及编译通过。
