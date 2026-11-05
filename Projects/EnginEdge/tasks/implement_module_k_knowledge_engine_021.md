---
id: implement_module_k_knowledge_engine_021
title: 实现 EnginEdge Module K 知识与治理引擎
status: completed
priority: high
tags:
- knowledge
- module_k
- rust
- mcp
session: 9c1db6b9-de32-4ef9-b7e6-c1b1c4fd2458
---

# 实现 EnginEdge Module K 知识与治理引擎

## 任务目标与背景
在 EnginEdge 中实现 Module K (Knowledge & Governance Engine):
1. Rust 原生项目元数据寻址 (定位 ~/.gemini/Projects/<project>/)；
2. 知识库查询 (kb_search)、读取 (kb_read)、落盘记录并自动更新索引 (kb_record)、踩坑红线校验 (kb_audit)；
3. 与 Policy Engine 和 Security 联动；
4. 运行模式策略：独立运行 (run/bench) 时自动加载，无知识库时零开销静默降级；MCP 模式下默认不暴露工具，支持 --enable-kb / --preset kb 按需开启。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## 架构设计与实现目标
在 EnginEdge 中落地 Module K (Knowledge & Governance Engine)，实现三大层级：
1. **原生项目元数据寻址 (`src/knowledge.rs`)**：
   - 自动推导工作区根目录与项目名，定位 `~/.gemini/Projects/<project_name>/`；
   - 支持环境变量 `ENGINEDGE_META_DIR` / `AGY_PROJECT_META_DIR` 覆盖；
   - 无元数据时零报错静默优雅降级。
2. **核心治理工具集 (`kb_search`, `kb_read`, `kb_record`, `kb_audit`)**：
   - 纯 Rust 检索与读取；
   - 原子落盘并自动同步更新 `knowledge.md` / `grave.md` 索引；
   - 方案前置审计扫描反模式红线。
3. **两套运行模式策略**：
   - **独立运行 (`run` / `bench`)**：默认启用，无知识库时优雅降级；
   - **MCP 模式 (`mcp`)**：默认预设（`light`/`ast`/标准`full`）不暴露 `kb_*` 工具，仅在 `--enable-kb` 或 `--preset kb` 时按需暴露。
4. **交付方式**：通过 Google Jules Watchdog (Gemini 3.1 Pro 云端 VM) 自动编译、自测并通过 GitHub Pull Request 交付。
