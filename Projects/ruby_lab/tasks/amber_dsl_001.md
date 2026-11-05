---
title: Initialize PVE Ruby Environment (mise) and Amber DSL Implementation
status: completed
priority: high
tags:
- env
- ruby
- amber
- dsl
session: conversation://521401e5-10e3-4c95-8143-9e6c03a9caad
id: amber_dsl_001
---
# 任务目标 / Task Goals & 交付报告 / Delivery Report

1. **环境准备 (Env Setup)**: [COMPLETED]
   - 在 PVE 服务器 (`Antigravity`) 上通过 `mise` 成功配置 Ruby 3.3.0 与 Bundler 2.5.3。
   - 现有环境隔离保护：Python 3.13、Go 1.23、fnm、uv 环境完全保持原样，零干扰。
   - 配置 `~/.bashrc` 中的 mise shims 与自动激活。

2. **Amber 2.0 框架核心架构开发**: [COMPLETED]
   基于 `kael.md` 的全部设计诉求，搭建了完整的反应式状态机与自主 Agent 引擎：
   - **反应式状态机 (`Amber::StateMachine`, `Amber::State`)**: 基于事件监听的即时状态跃迁机制，只要满足跳变条件即刻触发下一状态，无需阻塞等待所有长任务。
   - **动态并发任务 (`Amber::Job`, `Amber::Context`)**:
     - 混合依赖声明：支持形式规则（Formal Guards）与基于内容主观判断的语义依赖（Semantic Guards via LLM）。
     - 支持运行期动态追加：支持通过 `ctx.spawn_job(...)` 在执行过程中追加任务并即刻纳入调度。
   - **执行器分层 (Workflow vs Agent vs Dynamic Agent)**:
     - `Amber::Workflow`: 确定性任务流水线，提供 `.as_tool` 转换为 Agent 工具接口。
     - `Amber::Agent`: 完整 ReAct 循环，支持 GLM 等多模型模板与自定义工具调用。
     - `Amber::DynamicAgent`: 当 Job 未定义具体执行体时，自动由 LLM 分析意图动态生成 Prompt 与绑定工具。
   - **生态扩展适配器**:
     - `Amber::Skill`: Claude Skill 目录规范解析器与脚本工具封装。
     - `Amber::MCP`: Model Context Protocol (stdio JSON-RPC) 客户端适配。
   - **Ruby 动态沙箱隔离 (`Amber::Sandbox`)**:
     - Tier 2 (Process.fork + setrlimit): 原生进程级隔离，实施 CPU 时间、内存限额（防 OOM/死循环）与硬超时强制回收机制。
     - Tier 1 (InProcess BasicObject): 轻量内存级白名单沙箱。

3. **测试与验证交付**: [COMPLETED]
   - 全套自动化测试套件 (`test/`): 覆盖 Context、Sandbox、Workflow、StateMachine，`rake test` 11 runs / 33 assertions 100% 通过。
   - 实战端到端案例 (`examples/agentic_order_flow.rb`): 演示电商全流程并发、动态追加、多模型 Agent 与即时流转。
   - 沙箱专项案例 (`examples/dynamic_sandbox_demo.rb`): 演示进程隔离、超时拦截、内存限制与 Crash 隔离。
   - 独立 Git 仓库管理: 遵循 multi-repo 规范，独立提交并推进入 master 分支。
