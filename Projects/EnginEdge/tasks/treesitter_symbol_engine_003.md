---
id: treesitter_symbol_engine_003
title: 'Milestone 2: 跨语言 Tree-sitter AST 符号引擎'
status: completed
priority: high
tags:
- milestone2
- rust
- treesitter
- ast
session: null
---

# Milestone 2: 跨语言 Tree-sitter AST 符号引擎

## 任务目标与背景
集成 Tree-sitter 核心与多语言语法库 (Rust, Go, TypeScript/JavaScript, Python, Ruby)，实现代码大纲提取 (get_outline)、符号精读 (read_symbol) 与符号原子替换 (replace_symbol)，彻底消除行号漂移。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

### Google Jules 调度信息 (Milestone 2)
- **Session ID**: `sessions/15340192566539380919`
- **Session URL**: https://jules.google.com/session/15340192566539380919
- **自动化模式**: `AUTO_CREATE_PR` (Autonomous Mode)
- **Watchdog 状态**: PVE 后台守护进程运行中 (PID: 29593)，正自动轮询执行状态

### 交付与验证报告 (Milestone 2)
- **PR 详情**: [#2 feat: implement Universal Tree-sitter AST Engine](https://github.com/catclever/EnginEdge/pull/2) (已自动化合并至 `main`)
- **多语言语法支持**:
  * Rust (`tree-sitter-rust`)
  * Go (`tree-sitter-go`)
  * TypeScript / JavaScript (`tree-sitter-typescript`, `tree-sitter-javascript`)
  * Python (`tree-sitter-python`)
  * Ruby (`tree-sitter-ruby`)
- **核心工具集成**:
  * `get_outline(file_path)`: 提取类/函数/方法/接口大纲与范围
  * `read_symbol(file_path, symbol_path)`: 符号级精准提取代码
  * `replace_symbol(file_path, symbol_path, new_code)`: 语法树原子替换 + 语法自检防破坏
- **自动化测试**: PVE 节点执行 `cargo test`，11 项单元测试全绿通过（100% Pass）。
- **代码同步**: 远端 `main` 分支已合入，Mutagen 已自动同步至本地 Mac 工作区。
