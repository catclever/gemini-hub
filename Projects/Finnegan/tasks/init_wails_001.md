---
title: Initialize Wails Project
status: completed
priority: high
tags:
- setup
- wails
id: init_wails_001
---
# 初始化 Wails 项目

**目标**: 
在 `/root/Projects/Finnegan` (及 Mac 镜像端) 初始化标准的 Wails 项目骨架，并集成已有的 `bugu` 模块。

**验收结果**:
1. [x] 确定并初始化 Svelte + TypeScript 前端架构与 Wails v2 骨架。
2. [x] 成功安装 PVE Debian 13 底层依赖 (`pkg-config`, `libgtk-3-dev`, `libwebkit2gtk-4.1-dev`) 及 `wails v2.11.0` CLI。
3. [x] 结构深度整合：将 `bugu` (config, models, fetcher, llm, api) 作为内部包导入 Wails 后端，并在 `App` 结构体提供 `GetRadarTargets` 与 `RunRadar` 绑定，自动生成 TS 接口定义与前端运行时。
4. [x] 前后端完整编译跑通：`wails build -tags webkit2_41` 成功输出可执行二进制 `build/bin/Finnegan` (9.4MB)。
5. [x] Git 版本基线建立：完成 `git init` 与 `.gitignore` 过滤，并按夜间狂暴模式准则完成版本提交。
