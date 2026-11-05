---
id: calendar_day_time_formatting_and_qiantian_123
title: 卡片时间重构为自然日历日判定并引入前天格式（解决前天显示为昨天）
status: completed
priority: high
tags:
- frontend
- time
- bugfix
session: 9000d23e-2804-454f-9c2d-6d28930fee7d
---

# 卡片时间重构为自然日历日判定并引入前天格式（解决前天显示为昨天）

## 任务目标与背景
将卡片时间格式化引擎从滚动的 24h/48h 毫秒时差重构为自然日历日（今天/昨天/前天/N天前）判定，彻底解决前天下午/晚上撰写的卡片因未满 48 小时被误算为'昨天'，以及缺乏'前天'展示格式的问题。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## 问题根因分析
1. **滑动毫秒差误判**:
   原 `formatPointTime` 采用纯物理毫秒时差 `diffMs < 48 * 3600 * 1000` 判定“昨天”。若当前为下午（如 12:36），前天（27日）下午（如 15:00）或晚上撰写的卡片，距现在仅 45.6 小时，小于 48 小时，从而被错误归类为“昨天”。
2. **缺乏“前天”语义层级**:
   原代码在 48 小时之后直接退化为 `{days} 天前 {period}`（即显示为“2 天前 上午”），代码库中完全没有“前天”这一自然语言格式。

## 修复方案
1. **自然日历日判定（Calendar Day Difference）**:
   利用 `targetMidnight` 与 `nowMidnight` 计算绝对日历日差 `dayDiff`：
   - `dayDiff === 0`: 今天（< 5分钟为“刚刚”，否则为“今天 HH:mm”）
   - `dayDiff === 1`: 昨天（“昨天 HH:mm”）
   - `dayDiff === 2`: 前天（“前天 HH:mm”）
   - `dayDiff >= 3 && dayDiff < 30`: N 天前（“{dayDiff} 天前 {period}”）
2. **全面测试验证**:
   `frontend/src/lib/time.test.ts` 完整覆盖日历日“今天/昨天/前天/N天前”全部边界用例，158 个测试全部通过。
3. **前端生产构建验证**:
   `npm run build` 0 报错通过。
