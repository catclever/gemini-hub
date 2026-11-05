---
id: add_session_scope_to_clean_subagents_015
title: 为子代理清理脚本支持会话隔离与时间戳保护参数
status: completed
priority: medium
tags:
- scripts
- gc
- subagents
session: conversation://fa84592e-d75a-41f4-b469-a5fad64eb31e
---

# 为子代理清理脚本支持会话隔离与时间戳保护参数

## 变更概述
为 clean_subagents.py 脚本增加 --session 单会话隔离作用域与 --min-age-hours 全局活跃时间戳保护锁，未改动任何外部规则或运行触发逻辑。

## 验证结论
- [x] 核心逻辑已实现并通过验证
