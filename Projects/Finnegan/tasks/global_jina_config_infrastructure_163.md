---
id: global_jina_config_infrastructure_163
title: 全局 Jina 配置基础设施下沉与跨模块统一
status: completed
priority: medium
tags:
- backend
- config
- jina
session: null
---

# 全局 Jina 配置基础设施下沉与跨模块统一

## 任务目标与背景
Promote Jina configuration (api_key, base_url) to global config.Config (finnegan.yml). Update Config struct in core/config/config.go, migrate Bugu and keyword link fetcher to inherit this global Jina configuration, and ensure unit tests pass.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
