---
id: terminal_interactive_cli_launcher_tai_011
title: TaiChi 终端交互式 CLI 启动器 (tai) 实现与环境安装
status: completed
priority: medium
tags:
- cli
- launcher
- terminal
- fzf
session: conversation://1d0eccf4-3467-4f0c-b2c9-3d731d7b7844
---

# TaiChi 终端交互式 CLI 启动器 (tai) 实现与环境安装

## 任务目标与背景
实现方案 A 终端交互式启动器 tai，打通网关 API 并支持 fzf 模糊搜索、直接调用与导航下钻，安装到用户全局 PATH。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## 变更概述与验证结论

1. **终端交互式 CLI 启动器实现**：
   - 编写了 [`bin/tai`](file:///Users/kael/Projects/taichi_launcher/bin/tai) 命令行工具，原生对接 TaiChi 统一网关 HTTP API（默认端口 `9216`，支持 `TAICHI_PORT` 环境变量覆盖）。
   - **交互式选择与模块下钻**：完美集成终端模糊搜索工具 `fzf`，支持 ANSI 高亮、回车执行、模块卡片（如 `⚡️ Cyber 注入应用`）自动无缝下钻展开下一级列表。
   - **直达参数与单项穿透**：支持 `tai cyber [app]`、`tai service [action]`、`tai action <payload>`。当匹配到唯一操作项时自动执行，多个选项时自动进入 fzf 交互过滤。
   - **脚本化选项**：提供 `-l/--list`（文本列表模式）及 `-j/--json`（输出原始 Alfred 风格 JSON，方便与其他脚本配合）。
2. **环境注入与全局命令部署**：
   - 软链接安装至用户 PATH 目录：`/Users/kael/Library/XDG/bin/tai` -> `/Users/kael/Projects/taichi_launcher/bin/tai`。
   - 验证 `which tai` 成功定位，命令行直接调用 `tai -h`、`tai --list`、`tai cyber -l` 及动作执行均 100% 成功。
