---
id: tune_card_scale_range_balanced_098
title: 平衡调整卡片透视缩放比例至 0.48~1.15 及 3D 深度位移
status: completed
priority: medium
tags:
- frontend
- optics
- scale
- ui
session: 242774c3-b4d5-489f-afb1-fcb6326d9fee
---

# 平衡调整卡片透视缩放比例至 0.48~1.15 及 3D 深度位移

## 变更概述
依据视觉反馈优化卡片缩放动态范围：近景最大 1.15x (230px)，远景最小 0.48x (96px)，translateZ 平衡调整为 [-120px, +120px]，兼顾强烈的景深对比与卡片辨识度。

## 验证结论
- [x] 核心逻辑已实现并通过验证
