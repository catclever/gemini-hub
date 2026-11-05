---
id: fix_mention_badge_low_contrast_adaptive_colors_059
title: 优化 Mention 面板暗色主题下项目指示灯与胶囊徽标的自适应亮度对比度
status: completed
priority: medium
tags:
- ui
- contrast
- mention
- theme
session: 051fa041-ce31-48b5-9568-442511c143a1
---

# 优化 Mention 面板暗色主题下项目指示灯与胶囊徽标的自适应亮度对比度

## 任务目标与背景
修复 Mention 面板中部分深色项目主题色（如 HollyShit #121a21、EnginEdge #1a2b4c）在暗黑背景下文字与指示灯隐形的问题。引入 HSL 自适应亮度保底算法，保留原色相并智能将明度提升至高对比可见区间。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
