---
title: "Amber 2.0: Reactive Agentic State Machine & Execution Engine"
date: "2026-10-10"
author: "Antigravity Night Shift"
status: "tentative"
tags: [amber, dsl, state-machine, agent, sandbox, mcp]
---

# Amber 2.0 核心架构设计方案

## 1. 设计愿景与背景
在传统的规则引擎与状态机设计中，状态流转往往是静态、同步且线性的。然而现代 AI Agent 系统（如 `agentos`）要求：
1. **基于 Context 的动态驱动**：依据不断变化的事实上下文，自发唤醒与执行任务。
2. **并发与非阻塞反应式流转**：多个 Job 并行运算，无需等待全局 Job 归拢，只要关键 Job 产出满足条件，即刻触发状态跃迁。
3. **动态 Job 生成**：Job 不仅能预先硬编码，还能在运行时由人类动态注入或由 LLM Agent 动态追加。
4. **混合依赖判断**：兼备形式规则依赖（Deterministic Guard）与基于内容的主观语义判断（Semantic Guard via LLM）。
5. **多形态执行**：Job 可为 Deterministic Workflow、ReAct Agent、或由 AI 根据 Job 意图自愈生成的 Dynamic Agent。
6. **自动安全沙箱**：在 Ruby 生态中提供多层级的执行隔离。

---

## 2. 状态机与并发 Job 引擎架构

```
               ┌────────────────────────────────────────────────────────┐
               │                  Amber::Context (Facts)                │
               └───────────────────────┬────────────────────────────────┘
                                       │ (Reactive Updates)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ State: ActiveState                                                              │
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │ Job Pool (Concurrent Execution)                                         │   │
│   │                                                                         │   │
│   │  [Job A: Fetch Data]      -> Finished -> updates Context                │   │
│   │  [Job B: Risk Agent]      -> Finished -> updates Context                │   │
│   │  [Job C: Dynamic Agent]   -> Running (background)                       │   │
│   │  [Job D: Dynamically Appended at runtime]                               │   │
│   └──────────────────────────────────────┬──────────────────────────────────┘   │
│                                          │                                      │
│   ┌──────────────────────────────────────┴──────────────────────────────────┐   │
│   │ Transition Evaluator (Event-Driven)                                     │   │
│   │  If Condition Satisfied -> TRIGGER NEXT STATE IMMEDIATELY!              │   │
│   └──────────────────────────────────────┬──────────────────────────────────┘   │
└──────────────────────────────────────────┼──────────────────────────────────────┘
                                           ▼
                                    State: NextState
```

### 关键机制
1. **Event-Driven Transitions (非阻塞即时跃迁)**：
   每次 Context 写入（`ctx.set(...)`）或 Job 完成时，引擎自动对当前 State 的所有 `transition` 进行求值。一旦满足跳转条件，立刻推进到新状态，未完成的耗时 Job 可根据策略被静默取消或转入后台。
2. **Job Context Dependency Declarations**：
   - **形式依赖 (Formal Guard)**: `depends_on: [:order_id, :user_id]` 或 `depends_on: ->(ctx) { ctx[:amount] > 100 }`。
   - **语义依赖 (Semantic Guard)**: `semantic_guard: "上下文中的用户资料与订单信息已足够评估信用风险"`，通过内部轻量 LLM 快速判断是否具备执行条件。
3. **动态 Job 追加 (`context.spawn_job(...)`)**：
   在状态机运行生命周期内，任何 Agent 或外部事件可调用 `state.append_job(name, ...)` 动态注册新 Job。

---

## 3. 执行器分层：Workflow vs Agent vs Dynamic Agent

1. **Workflow (确定性工作流)**：
   - 确定性的 Ruby 逻辑，步骤串联或 DAG。
   - **Workflow 转换为 Tool**：提供 `.as_tool(name, description)`，允许将整条 Workflow 封装为 Agent 可调用的工具。
2. **Agent (LLM 驱动代理)**：
   - 支持 ReAct 循环（Thought -> Action -> Observation -> Final Answer）。
   - 兼容 `RubyLLM::LLMService` 和 `LLMJSON`。
   - 多模型 Prompt 模板适配（GLM, OpenAI, Gemini 等）。
3. **Dynamic Agent (动态自适应 Agent)**：
   - 当 Job **未定义** 具体执行体（无 Workflow 也无 Agent 声明）时，系统默认将其作为 Dynamic Agent。
   - 引擎根据 Job 名称、Context 现状及目标（Goal），利用 LLM 自动合成 System Prompt 与 Tool 绑定，自主完成任务。

---

## 4. 扩展生态：Claude Skill 与 MCP (Model Context Protocol)
- **Claude Skill 规范**：读取带有 `SKILL.md` 的目录规范，解析名称、描述、说明与执行脚本，自动转为 Ruby Tool。
- **MCP Client 适配器**：通过 stdio JSON-RPC 与 MCP Server（如 Filesystem, Brave Search, GitHub 等）通讯，自动发现工具定义并执行。

---

## 5. Ruby 生态沙箱机制的技术评估与落地方案

由于现代 Ruby（2.7+ / 3.x）废弃了历史上的 `$SAFE`，在 Ruby 生态实现沙箱有三种主要路径：

| 方案 | 原理 | 优点 | 缺点 / 挑战 | 适用场景 |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: In-Process BasicObject** | 基于 `BasicObject` 的 BlankSlate，限制方法调度与白名单常量 | 轻量、跨平台、极低开销 | 无法防御死循环、难以彻底防御全局类猴子补丁或复杂反射 | 轻量 DSL 规则计算、快速求值 |
| **Tier 2: Linux Process Fork + Rlimits** | 利用 Linux `Process.fork`，在子进程中配置 `setrlimit` (CPU、内存、进程数) 并切断多余 FD，通过 IPC Pipe 回传结果 | 纯原生 Ruby 支持、零外部依赖、彻底隔离内存崩溃与内存修改、防死循环与 OOM | 仅适用于 Unix/Linux（Mac/Linux 完全支持） | 动态 Ruby 代码执行、用户提交脚本 |
| **Tier 3: Bubblewrap / Bwrap** | 利用 Linux 内核 user namespace 与 seccomp 隔离文件系统与网络 | 最高安全级别（容器级隔离） | 需要系统安装 `bwrap` 依赖 | 高风险不可信代码 |

### 架构决策：
Amber 框架内置 **双层弹性沙箱架构 (`Amber::Sandbox`)**：
- 默认在 Linux/PVE 环境启用 **Tier 2 (Process.fork + Rlimits)**，提供进程级隔离、内存/CPU限额与硬超时安全终止；
- 同时保留 **Tier 1 (InProcess DSL Context)**，兼顾轻量级规则的高速评估。
