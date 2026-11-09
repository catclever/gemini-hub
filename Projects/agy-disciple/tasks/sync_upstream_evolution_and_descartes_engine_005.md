---
id: sync_upstream_evolution_and_descartes_engine_005
title: 全面同步上游演进架构、双MCP治理与Descartes高阶引擎
status: completed
priority: high
tags:
- sync
- upstream
- remote-agent
- descartes
- mcp
session: conversation://f27ccc3d-b20c-4931-bdf7-cede06f87258
---

# 全面同步上游演进架构、双MCP治理与Descartes高阶引擎

## 任务目标与背景
全面将本地私有上游 dev-team 与 scripts 的最新架构演进脱敏同步到 agy-disciple 开源仓库中：
1. 下线 Jules：移除 agents/jules-dev.yaml，使用 scripts/watchdogs/remote_watchdog.sh 替换 jules_watchdog.sh；
2. 同步看门狗与自动化工具：引入 remote_watchdog.sh、升级版 pve_watchdog.sh、pve_test_sync.sh、clean_subagents.py，并收录 descartes_watchdog.sh 作为高阶架构推荐；
3. 双 MCP 引擎：升级 mcp/kanban-task-manager/server.py（支持自动序列编号与脚手架），新增 mcp/knowledge-manager/server.py；
4. 技能库与双模升级：升级 dev-manager、project-manager、night-shift、pve-dispatch、extract-knowledge；将 test-environment 迁移重构为 dev-server；新增 descartes-dispatch、pure-remote-init、local-to-remote-migration；
5. 配置器与文档：升级 configure.py（更新 VARIANTS 并支持新技能映射），更新中英文双语 README，运行 python configure.py --doctor 确保 100% 通过。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
