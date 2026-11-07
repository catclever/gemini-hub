---
id: dynamic_tool_masking_and_swe_bench_workflow_003
title: 实现前端工具动态过滤与 SWE-bench 三阶段破案状态机
status: in_review
priority: high
tags:
- architecture
- swe-bench
- tool-masking
- workflow
session: conversation://703ec9db-6056-4813-8b39-e3ffa597e92f
---

# 实现前端工具动态过滤与 SWE-bench 三阶段破案状态机

## 任务目标与背景
1. 解耦 `Dalembert::Agent#initialize` 中写死的 5 个 OSINT 工具，支持 `tools:`、`cloud_tools:`（白名单，支持传 `[]` 全屏蔽）、`disabled_tools:`（黑名单，支持工具别名如 `search_code_examples`、`survey_architecture`）以及 `mode:` 参数。
2. 当 `mode: "swe_bench"`（或 `"bug_hunter"`）时，默认屏蔽 `github_repo_survey` 与 `github_code_search` 防止 SWE-bench 时间穿越泄漏。
3. 新增 `Dalembert::Workflows::SweBenchWorkflow`（`lib/dalembert/workflows/swe_bench_workflow.rb`），实现三阶段受控状态机（Stage 1 `:locate` 只读漏斗定位 -> Stage 2 `:reproduce` 最小复现红灯校验 -> Stage 3 `:patch_and_verify` 手术修复与回归验证）及按阶段动态工具掩码（Phase-based Tool Masking）。
4. 更新 `bin/dalembert-server` 支持转发 `mode`、`cloud_tools`、`disabled_tools`，并补齐 RSpec 单元测试。
5. 参考知识库文档：`kb/swe_bench_and_tool_masking_architecture.md`。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
