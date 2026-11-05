---
id: gravity_fallback_elevated_cards_112
title: 常态卡片通用全局引力归位兜底机制（10分钟保护期+切屏聚焦沉降+只往后不往前）
status: completed
priority: high
tags:
- ui
- cards
- physics
- lifecycle
- gravity
session: 9000d23e-2804-454f-9c2d-6d28930fee7d
---

# 常态卡片通用全局引力归位兜底机制（10分钟保护期+切屏聚焦沉降+只往后不往前）

## 任务目标与背景
实现常态卡片通用全局引力归位兜底机制：为所有被文本搜索、标签召回、命令挑选拉升至前台的常态卡片定义统一提升契约 (elevatedAt) 与 10 分钟保护期。在切屏切回 Finnegan (handleWindowFocus) 时，针对保护期已满的卡片，按创建时间计算其自然固有深度 (calculateIntrinsicTargetZ)，严格执行「只往后不往前 (targetZ > z + 5)」法则平滑沉降回深空，光芒与视觉线索独立保留。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
