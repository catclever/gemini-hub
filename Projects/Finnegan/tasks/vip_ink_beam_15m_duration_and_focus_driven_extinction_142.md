---
id: vip_ink_beam_15m_duration_and_focus_driven_extinction_142
title: 新卡片水墨飞白15分钟时效调整与窗口聚焦驱动熄灭机制
status: completed
priority: high
tags:
- water-ink
- vip-card
- window-focus
- lifecycle
- optics
session: 58c97e35-a614-4542-ad8d-16f08d35616c
---

# 新卡片水墨飞白15分钟时效调整与窗口聚焦驱动熄灭机制

## 变更概述
将新卡片独享水墨飞白光弧的生命周期与窗口聚焦刷新机制彻底打通：
1. 时长收敛调整：将水墨飞白光晕的持续时间从 30 分钟收敛调整为 15 分钟（VIP_INK_BEAM_DURATION_MS = 15 * 60 * 1000）；
2. 窗口获得焦点驱动刷新（Window Focus Extinction）：
   - 在 handleWindowFocus 中遍历所有卡片，若卡片拥有 isVIP 且诞生时间超过 15 分钟，立即清除 isVIP 标志（isVIP: false），并清空 latestManualCardId；
   - 即使卡片正处于聚焦模式下，切回窗口时亦会静默消除其 VIP 身份，确保用户退出聚焦回到散落态后飞白不会再次亮起；
3. 响应式与时钟驱动（Triple Guard）：
   - UICard.svelte 绑定 $stageTime 响应式依赖，窗口获焦调用 refreshStageTime() 时全量卡片响应式重算；
   - App.svelte 45s 代谢时钟（metabolicInterval）同步执行超时 VIP 检查，确保无人干预下亦能温和自然淡退；
4. 单元测试与构建验证：在 tempCardsCollect.test.ts 补充 3 组针对 VIP 飞白时效清除的单元测试并通过，全量 193 组单元测试通过，wails build 验证通过。

## 验证结论
- [x] 核心逻辑已实现并通过验证
