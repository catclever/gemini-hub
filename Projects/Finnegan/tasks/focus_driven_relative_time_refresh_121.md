---
id: focus_driven_relative_time_refresh_121
title: 切屏聚焦时卡片相对时间格式刷新（今天/昨天/前天/刚刚）
status: completed
priority: medium
tags:
- frontend
- time
- focus
session: 9000d23e-2804-454f-9c2d-6d28930fee7d
---

# 切屏聚焦时卡片相对时间格式刷新（今天/昨天/前天/刚刚）

## 任务目标与背景
Finnegan 窗口获得焦点 (handleWindowFocus) 时，触发卡片展示时间格式重新计算，确保跨天或时间流逝后（今天/昨天/前天/刚刚等）相对时间显示能够自动刷新。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## 变更概述
1. **全局响应式 Stage 时间锚点**:
   - 在 `frontend/src/lib/time.ts` 中导出响应式 Svelte Store `stageTime: Writable<number>` 及主动刷新函数 `refreshStageTime(now?: number)`。
2. **聚焦驱动时间刷新机制**:
   - 在 `frontend/src/App.svelte` 的 `handleWindowFocus` 以及 `visibilitychange`（切屏重返 Finnegan）触发时调用 `refreshStageTime()`，确保窗口获得焦点瞬间所有卡片展示的相对时间自动重算。
   - 在 `metabolicInterval`（45s 周期）中同步调用 `refreshStageTime()`，保证即使常驻前台，跨越 5 分钟（刚刚 -> 今天）或午夜（今天 -> 昨天）时也能自然刷新。
3. **卡片层级全链路响应绑定**:
   - `UICard.svelte` 将展示时间计算绑定为 `$: displayTime = getCardDisplayTime(card, $stageTime)`。
   - `VirtualCardProxy.svelte` 将展示时间计算绑定为 `getTime(card, $stageTime)`。
   - `ThoughtCardBody.svelte`、`BabelCardBody.svelte`、`NoteCardBody.svelte`、`ChatLogCardBody.svelte` 的时间兜底与区间时间计算均接入 `$stageTime`。
4. **自动化单元测试与构建验证**:
   - `frontend/src/lib/time.test.ts` 新增对 `stageTime & refreshStageTime` 响应式及多时间跨度（刚刚 -> 今天 -> 昨天 -> 2天前 -> 1年前的今天）聚焦跳转的完整测试。
   - 151 个自动化单元测试全部通过，Vite 生产打包通过。
