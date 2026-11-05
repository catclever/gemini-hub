---
id: kanban_markdown_scaffold_and_content_api_012
title: Support task markdown description, smart scaffolding, and content update tool
  for Qled preview
status: completed
priority: high
tags:
- mcp
- kanban
- qled
- markdown
- ux
session: conversation://1165d06b-68aa-45a9-bfac-5abc5703d5f6
---

# Support task markdown description, smart scaffolding, and content update tool for Qled preview

## 变更概述
在 kanban_mcp_server 中新增 description 参数支持与状态自适应 Markdown 骨架生成，新增 update_task_content 工具支持正文追加/替换；同时升级自愈巡检引擎，一键治愈全量历史 239 个空正文任务，并同步更新 project-manager SOP。

## 验证结论
- [x] 核心逻辑已实现并通过验证
