---
id: mcp_ripgrep_and_ast_import_manager_018
title: 落地内嵌 ripgrep 引擎与 AST 专属 Import 引用管理器两大核心升级
status: completed
priority: high
tags:
- ast
- ripgrep
- imports
- refactor
- enginedge
session: 8bc0e420-6a50-41a3-95a4-21f573d20bb0
---

# 落地内嵌 ripgrep 引擎与 AST 专属 Import 引用管理器两大核心升级

## 任务目标与背景
在 EnginEdge 端落地两大核心升级：1) 内嵌 Rust 官方 ignore/ripgrep 引擎，支持 .gitignore 自动解析、隐蔽与二进制文件过滤及海量代码毫秒级检索；2) 基于 Tree-sitter 语法树构建跨语言专用 manage_imports 引用管理器，实现引用的自动幂等合并、智能定位与无效死引用清理。同时顺手加固沙箱隔离（防止目录脏文件污染包名）。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
