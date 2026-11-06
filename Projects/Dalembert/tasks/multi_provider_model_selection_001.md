---
id: multi_provider_model_selection_001
title: 支持多Provider与动态模型参数选择 (方案B)
status: completed
priority: high
tags:
- architecture
- llm
- multi-provider
- dalembert
session: null
---

# 支持多Provider与动态模型参数选择 (方案B)

## 任务目标与背景
实现Provider与Model的正交解耦机制：
1. 支持在llm.yml配置多个Provider通道及各Provider默认模型；
2. 实现ProfileResolver，支持'provider/model'复合语法及显式model参数；
3. 解决ENV['LLM_BASE_URL']强行霸权导致的Profile失效问题；
4. 改造Dalembert::Agent与bin/dalembert CLI，支持--model参数；
5. 扩展WebSocket init报文解析，使客户端（EnginEdge）可无缝动态切换Provider与Model。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
