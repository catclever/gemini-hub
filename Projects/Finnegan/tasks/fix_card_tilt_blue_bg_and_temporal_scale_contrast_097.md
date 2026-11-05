---
id: fix_card_tilt_blue_bg_and_temporal_scale_contrast_097
title: 修复鼠标倾角过大、常态卡片误染临时蓝底与今日及历史卡片景深对比度失效
status: completed
priority: high
tags:
- frontend
- bugfix
- optics
- tilt
- scale
session: 242774c3-b4d5-489f-afb1-fcb6326d9fee
---

# 修复鼠标倾角过大、常态卡片误染临时蓝底与今日及历史卡片景深对比度失效

## 任务目标与背景
1. 减小 globalTilt 倾角至 ±4.5° 并恢复 1000px 视角，收敛卡片 2D 散乱角度至 ±7°；2. 修复 isTemporary 判定条件，仅针对 bugu/radar 卡片，常态卡片恢复纯净白毛玻璃；3. 修复 stageCoords 中 macroExpiresAt 劫持所有卡片导致 z 统一等于 20 的重大缺陷，拉开今日卡片 (z 3~11, scale ~1.22x) 与 11天前卡片 (z 48~62, scale ~0.70x) 的显著尺寸对比。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
