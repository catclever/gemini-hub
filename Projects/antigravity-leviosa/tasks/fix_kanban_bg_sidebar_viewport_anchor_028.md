---
id: fix_kanban_bg_sidebar_viewport_anchor_028
title: 修复展开侧边栏时任务看板背景缩放偏移并实现视口绝对锚定
status: completed
priority: medium
tags:
- ui
- kanban
- background
- layout
session: 4282f618-0b6a-49c7-a16e-c9884bc4f2c4
---

# 修复展开侧边栏时任务看板背景缩放偏移并实现视口绝对锚定

## 变更概述
当右侧边栏展开导致看板宽度被压缩时，由于 CSS transform 形成了新的 containing block，直接在面板上使用 fixed 背景会导致背景以压缩后的宽度重新计算 cover 缩放与居中，从而产生形变与视差错位。通过剥离出视口级独立背景层 #leviosa-pm-bg，并在 updateLayout 中严格维持真实视口全屏宽高与反向偏移裁剪，彻底实现侧边栏无论开合背景均绝对对齐且无缝融合。

## 验证结论
- [x] 核心逻辑已实现并通过验证
