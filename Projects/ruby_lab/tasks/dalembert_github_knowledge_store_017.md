---
id: dalembert_github_knowledge_store_017
title: 为 Dalembert KnowledgeStore 接入 GitHub Contents API 持久化存储
status: completed
priority: high
tags:
- pve
- dalembert
- github
- night-shift
session: 72c41d87-5423-42bb-9e33-136cae2ea3f3
---

# 为 Dalembert KnowledgeStore 接入 GitHub Contents API 持久化存储

## 任务目标与背景
为 Dalembert 的 KnowledgeStore 模块增加基于 GitHub Contents API 的远端持久化支持：
1. 检查环境变量 GITHUB_TOKEN 与 KNOWLEDGE_REPO（支持格式 owner/repo，支持配置可选的 KNOWLEDGE_BRANCH，默认 main）；
2. 若存在以上配置，store/retrieve/list_topics 优先调用 GitHub REST API (https://api.github.com/repos/{repo}/contents/{path}) 进行知识读写与列举；
3. 若未配置则无缝回退到本地 ./knowledge_vault 目录；
4. 补充针对 GitHub 模式和本地模式的 RSpec 单元测试，确保 bundle exec rspec 全绿通过；
5. 提交代码并推送到 catclever/Dalembert 仓库。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
