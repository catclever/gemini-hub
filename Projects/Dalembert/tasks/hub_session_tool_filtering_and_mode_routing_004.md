---
id: hub_session_tool_filtering_and_mode_routing_004
title: 改造 descartes-produit Session 支持前端工具动态过滤与 SWE-bench 状态机路由
status: in_review
priority: high
tags:
- descartes-produit
- hub-session
- swe-bench
- tool-masking
session: conversation://703ec9db-6056-4813-8b39-e3ffa597e92f
---

# 改造 descartes-produit Session 支持前端工具动态过滤与 SWE-bench 状态机路由

## 任务目标与背景
1. 改造 `/Users/kael/workbench/ruby_lab/descartes-produit/lib/descartes/hub/session.rb` 中的 `handle_init`（原第 109~121 行无条件注入 5 个 Dalembert 工具），改为支持 `payload[:cloud_tools]`（白名单，传 `[]` 则不注入任何云端工具）、`payload[:disabled_tools]`（黑名单，支持工具名与别名如 `search_code_examples`、`survey_architecture`）以及 `payload[:mode]`（当 `mode == "swe_bench"` 时默认屏蔽 `github_repo_survey` 与 `github_code_search`）。
2. 在 `handle_execute_tool` 中同样校验 `disabled_tools` / 模式限制，防止被屏蔽的云端工具通过直接 RPC 调用绕过。
3. 在 `handle_init` 中接入模式路由：当 `payload[:mode]` 为 `"swe_bench"`（或 `"bug_hunter"`）且 `Dalembert::Workflows::SweBenchWorkflow` 可用时，启动三阶段受控状态机（`:locate` -> `:reproduce` -> `:patch_and_verify`），并将各阶段的 `thought`、`tool_call_start`、`tool_call_end` 流式事件通过 WebSocket 实时推送给前端。
4. 补齐 `descartes-produit/spec/` 下的 RSpec 单元测试并验证全量通过。
5. 参考知识库文档：`~/.gemini/Projects/Dalembert/kb/swe_bench_and_tool_masking_architecture.md`。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
