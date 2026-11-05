---
id: extract_descartes_hub_013
title: 独立出 descartes-hub 项目并更新 Dockge 配置
status: completed
priority: high
tags:
- pve
- refactor
- descartes
session: 72c41d87-5423-42bb-9e33-136cae2ea3f3
---

# 独立出 descartes-hub 项目并更新 Dockge 配置

## 任务目标与背景
将 descartes 中的 Hub 模块独立为独立的 descartes-hub 目录/服务：
1. 在 ruby_lab 下创建 descartes-hub 目录，迁移 lib/descartes/hub、bin/descartes-hub、Dockerfile 及 compose.yaml；
2. 保持 descartes 作为纯净 Agent SDK，更新各自 README.md；
3. 更新 Dockge 服务配置以引用新位置。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
