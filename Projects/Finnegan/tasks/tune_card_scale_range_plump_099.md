---
id: tune_card_scale_range_plump_099
title: 优化卡片丰满度：近景最大 1.25x 与远景最小 0.55x 缩放比例
status: completed
priority: medium
tags:
- frontend
- optics
- scale
- ui
session: 242774c3-b4d5-489f-afb1-fcb6326d9fee
---

# 优化卡片丰满度：近景最大 1.25x 与远景最小 0.55x 缩放比例

## 变更概述
根据公主审美偏好优化整体质感丰满度：将近景最大缩放设为 1.25x (250px)，远景收敛于 0.55x (110px)，公式 uniformScale = 0.55 + 0.70 * (1 - zNorm)^1.2，使全局卡片更饱满且层次分明。

## 验证结论
- [x] 核心逻辑已实现并通过验证
