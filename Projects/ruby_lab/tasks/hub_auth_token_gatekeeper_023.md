---
id: hub_auth_token_gatekeeper_023
title: 在 descartes-produit 中加入可选的 HUB_AUTH_TOKEN 鉴权守卫
status: completed
priority: medium
tags:
- security
- hub
- descartes-produit
- auth
session: 72c41d87-5423-42bb-9e33-136cae2ea3f3
---

# 在 descartes-produit 中加入可选的 HUB_AUTH_TOKEN 鉴权守卫

## 任务目标与背景
Implement optional HUB_AUTH_TOKEN handshake gatekeeper in descartes-produit Hub Server (supporting Bearer header and query param ?token=) while keeping /healthz open for container probes.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
