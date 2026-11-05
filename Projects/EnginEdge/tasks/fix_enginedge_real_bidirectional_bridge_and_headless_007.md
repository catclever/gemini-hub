---
id: fix_enginedge_real_bidirectional_bridge_and_headless_007
title: 'Phase 2: EnginEdge 真实双向桥接、4项本地工具补齐与无头 run 入口'
status: completed
priority: high
tags:
- phase2
- rust
- bridge
- tools
- headless
session: conversation://5fd801ac-d570-4893-8590-69c9e3a18b74
---

# Phase 2: EnginEdge 真实双向桥接、4项本地工具补齐与无头 run 入口

## 任务目标与背景
重构 src/bridge.rs，实现不丢弃 write 端的真实双向 WebSocket 消息收发与请求响应关联队列；在 src/tools.rs 补齐 list_files、grep_search、write_file、run_verification (白名单执行器)；在 src/main.rs 实现 enginedge run 无头自主编码 CLI 入口；替换掉所有硬编码假数据，通过真实 WebSocket 调用云端 Dalembert 情报工具。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
