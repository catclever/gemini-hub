---
id: sort_completed_tasks_by_completion_time_desc_045
title: 已完成任务按完成时间倒序排列并展示时间戳徽标
status: completed
priority: medium
tags:
- ui
- kanban
- sorting
- feature
session: 4282f618-0b6a-49c7-a16e-c9884bc4f2c4
---

# 已完成任务按完成时间倒序排列并展示时间戳徽标

## 变更概述
在后端 pm_dashboard_api 中解析 completed_at 字段与文件 mtimeMs 修改时间戳，在前端看板对 Completed 栏位已完成任务执行时间倒序排序（最近完成置顶），并在已完成卡片底部增加轻量化完成时间徽标与悬停精准时间提示。

## 验证结论
- [x] 核心逻辑已实现并通过验证
