---
id: extract_subagent_gc_global_kb_014
title: 提取子代理垃圾回收规范为全局知识库与指令 (subagent-gc)
status: completed
priority: medium
tags:
- kb
- commands
- gc
session: conversation://fa84592e-d75a-41f4-b469-a5fad64eb31e
---

# 提取子代理垃圾回收规范为全局知识库与指令 (subagent-gc)

## 变更概述
将机会式静默清理规范独立沉淀为全局 KB 文件 ~/.gemini/kb/subagent-gc.md（支持 cmdg/快捷键注入与 /subagent-gc 触发），并在 GEMINI.md 中保留两节点自动触发机制与引用链接。

## 验证结论
- [x] 核心逻辑已实现并通过验证
