---
id: untrack_llm_yml_descartes_produit_018
title: 剥离 llm.yml 跟踪并提供标准 llm.example.yml 模板
status: completed
priority: medium
tags:
- security
- config
- git
- descartes-produit
session: 72c41d87-5423-42bb-9e33-136cae2ea3f3
---

# 剥离 llm.yml 跟踪并提供标准 llm.example.yml 模板

## 变更概述
在 descartes-produit 仓库中剥离 llm.yml 追踪，提供标准的 llm.example.yml 模板配置，并将 llm.yml 写入 .gitignore 彻底杜绝本地敏感配置泄漏。更新 Dockerfile 兜底从 example 自动拷贝。测试全绿并通过。

## 验证结论
- [x] 核心逻辑已实现并通过验证
