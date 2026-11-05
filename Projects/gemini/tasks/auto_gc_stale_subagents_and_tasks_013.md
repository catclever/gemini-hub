---
id: auto_gc_stale_subagents_and_tasks_013
title: 确立子代理与后台任务的两节点机会式静默清理机制 (Opportunistic Silent GC)
status: completed
priority: medium
tags:
- system-config
- gc
- subagents
session: conversation://fa84592e-d75a-41f4-b469-a5fad64eb31e
---

# 确立子代理与后台任务的两节点机会式静默清理机制 (Opportunistic Silent GC)

## 变更概述
根据公主的指导方案，在 GEMINI.md 和 dev-manager SOP 中正式确立【派发前检查】与【验收闭环时】两节点机会式静默清理规则，并在 clean_subagents.py 中增加 --quiet 静默支持。

## 验证结论
- [x] 核心逻辑已实现并通过验证
