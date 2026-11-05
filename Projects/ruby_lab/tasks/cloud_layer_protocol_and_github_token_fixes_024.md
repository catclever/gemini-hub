---
id: cloud_layer_protocol_and_github_token_fixes_024
title: 修复 descartes-produit 工具参数兼容性并补齐 Dalembert GITHUB_TOKEN
status: completed
priority: high
tags:
- descartes-produit
- dalembert
- github-api
- railway
session: 72c41d87-5423-42bb-9e33-136cae2ea3f3
---

# 修复 descartes-produit 工具参数兼容性并补齐 Dalembert GITHUB_TOKEN

## 任务目标与背景
1. descartes-produit session.rb 兼容 parameters/inputSchema/input_schema 工具参数字段；2. Dalembert github_repo_survey.rb 与 github_code_search.rb 补齐 GITHUB_TOKEN Authorization Header；3. Dalembert bundle update descartes-produit 锁定最新 commit 并 push 触发 Railway 自动部署。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
