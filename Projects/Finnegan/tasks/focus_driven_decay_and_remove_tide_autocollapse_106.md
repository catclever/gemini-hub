---
id: focus_driven_decay_and_remove_tide_autocollapse_106
title: 切屏聚焦驱动临时卡片后退消融与废除45秒视口强行回滚
status: completed
priority: high
tags:
- ui
- cards
- viewport
- lifecycle
session: 9000d23e-2804-454f-9c2d-6d28930fee7d
---

# 切屏聚焦驱动临时卡片后退消融与废除45秒视口强行回滚

## 任务目标与背景
废除 45 秒视口自动强行弹回第一屏的逻辑，保持用户滚动画布位置稳定；在 window 获得焦点 (focus) 时，按半衰期驱动临时卡片进行两阶段退行（中近景卡片向深空后退一步，深空卡片消融淡出），并彻底移除前台使用期间卡片凭空蒸发的心跳逻辑。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
