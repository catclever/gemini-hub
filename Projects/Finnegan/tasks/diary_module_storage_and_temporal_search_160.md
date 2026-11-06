---
id: diary_module_storage_and_temporal_search_160
title: 实现日记后端模块 (modules/diary)、卡片存储扩展与按小时/时间范围搜索
status: completed
priority: high
tags:
- diary
- search
- storage
- backend
session: conversation://c1672485-6e37-4151-b40f-453866902a63
---

# 实现日记后端模块 (modules/diary)、卡片存储扩展与按小时/时间范围搜索

## 任务目标与背景
实现日记后端模块 (modules/diary)、存储模型扩展与专属时间检索引擎：
1. 注册 diary 卡片类型：实现 modules/diary (Module, ManifestProvider, CommandProvider, ActionProvider)，声明 CardTypes: [{Type: "diary"}]。
2. 扩展卡片模型与 Frontmatter 解析 (cards.go, storage.go, app_capture.go)：新增 CardTypeDiary = "diary"，扩展 DiaryLocation 与 DiaryWeather 元数据读写；提供 CaptureDiary 捕获管道（当 geo 模块开启且授权 diary 模块时自动关联经纬度、位置命名与对应小时天气）。
3. 日记模块专属时间搜索技能 (modules/diary/temporal_search.go & app_search_cmd.go)：支持通过 /diary 命令或搜索框按精确到小时（如 2026-11-06 14、昨天 22:00）或时间范围（如 2026-11-01 ~ 2026-11-06、2026-11-06 08:00 ~ 18:00）以及叠加关键词检索日记卡片。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

- **Jules Cloud Session**: `sessions/8865300304482654504` (https://jules.google.com/session/8865300304482654504)
- **PVE Watchdog Log**: `/tmp/jules_diary_module_storage_and_temporal_search_160.log`
- **File Scope**: `modules/diary/*`, `cards.go`, `storage.go`, `app_capture.go`, `app_search_cmd.go`

- **PR Created**: https://github.com/catclever/Finnegan/pull/25 (`COMPLETED`)
