---
id: gravity_fallback_extinction_first_then_cooldown_118
title: 常态卡片引力归位修正：先光效熄灭解锁、再冷静10分钟后切屏归位
status: completed
priority: high
tags:
- ui
- cards
- physics
- gravity
session: 9000d23e-2804-454f-9c2d-6d28930fee7d
---

# 常态卡片引力归位修正：先光效熄灭解锁、再冷静10分钟后切屏归位

## 变更概述
修正全局引力归位逻辑：光芒亮起期间卡片绝对锁定在前台；光效寿命结束熄灭瞬间进入解锁状态并记录时间戳；从熄灭瞬间起算 10 分钟冷静期；冷静期满后切屏聚焦 (handleWindowFocus) 时严格执行「只往后不往前」沉降回历史深空。搜索光赋予 15 分钟自然寿命，UICard 光阶平滑适配。

## 验证结论
- [x] 核心逻辑已实现并通过验证
