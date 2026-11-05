---
id: implement_three_tier_gc_trigger_matrix_016
title: 确立三层梯次清理触发矩阵 (自动24h+、手动1h+、历史面板全域1h+)
status: completed
priority: medium
tags:
- gc
- subagents
- matrix
session: conversation://fa84592e-d75a-41f4-b469-a5fad64eb31e
---

# 确立三层梯次清理触发矩阵 (自动24h+、手动1h+、历史面板全域1h+)

## 变更概述
根据公主指令确立三层精准清理矩阵：1. 任何自动触发只清当前会话24h以上且静默；2. 当前会话手动注入cmd清当前会话1h以上；3. 历史会话面板触发清理所有会话1h以上。完成脚本参数支持与KB、GEMINI.md同步。

## 验证结论
- [x] 核心逻辑已实现并通过验证
