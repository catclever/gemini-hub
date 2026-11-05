---
id: fix_agy_sheet_browser_hole_background_transparency_061
title: 修复新版 Antigravity agy-sheet 与 browser-hole 导致右侧背景实色遮挡失效问题
status: completed
priority: high
tags:
- ui
- bugfix
- background
session: 9121fe6d-93bf-4b57-83c0-aa3e25a6da14
---

# 修复新版 Antigravity agy-sheet 与 browser-hole 导致右侧背景实色遮挡失效问题

## 变更概述
Antigravity 官方在最新架构升级中引入了 .agy-sheet 与 browser-hole-ancestor 容器，其自带实色背景 rgb(7, 7, 9) 挡住了底层壁纸与毛玻璃。通过在反套娃机制中加入对 .agy-sheet、.browser-hole-opaque 及相关容器的穿透透明化规则，彻底恢复右侧主舞台（Home Greeting 及对话页面）的背景注入与磨砂质感。

## 验证结论
- [x] 核心逻辑已实现并通过验证
