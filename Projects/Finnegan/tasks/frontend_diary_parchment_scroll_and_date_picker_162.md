---
id: frontend_diary_parchment_scroll_and_date_picker_162
title: 实现日记卡片羊皮卷双态渲染（散落单卷/聚焦同日正序合卷）与左上角日期选择器
status: completed
priority: high
tags:
- diary
- parchment
- ui
- frontend
session: conversation://c1672485-6e37-4151-b40f-453866902a63
---

# 实现日记卡片羊皮卷双态渲染（散落单卷/聚焦同日正序合卷）与左上角日期选择器

## 任务目标与背景
实现前端日记卡片羊皮卷双态渲染组件与聚焦态左上角日期选择器：
1. 注册 diary 卡片组件 (cardRegistry.ts, DiaryCardBody.svelte, UICard.svelte)：散落态 (200x190) 单张展示为微缩复古羊皮卷，镶嵌「昼夜时辰×天气」联动天象图标与位置印记。
2. 聚焦态同日正序合卷 (src/lib/diaryScroll.ts & DiaryCardBody.svelte)：进入聚焦态时，自动聚合同一自然日的所有日记卡片，在一张舒展的羊皮卷轴上按时间正序（从清晨到深夜）依次排开，每篇带独立天象时辰图标、地点与正文配图，支持双击单篇独立打开外部编辑器。
3. 聚焦态左上角日期选择器 (DiaryDatePicker.svelte)：在聚焦态羊皮卷左上方展示古籍风日期选择器（标注有日记的日期墨点、禁选未来日期），支持前后日翻页或点选具体日期无缝切换查看对应日期的羊皮卷。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

- **Jules Cloud Session**: `sessions/11794671028204298200` (https://jules.google.com/session/11794671028204298200)
- **PVE Watchdog Log**: `/tmp/jules_frontend_diary_parchment_scroll_and_date_picker_162.log`
- **File Scope**: `frontend/src/lib/diaryScroll.ts`, `frontend/src/components/cards/DiaryDatePicker.svelte`, `frontend/src/components/cards/DiaryCardBody.svelte`, `frontend/src/components/cards/cardRegistry.ts`, `frontend/src/UICard.svelte`

- **PR Created**: https://github.com/catclever/Finnegan/pull/22 (`COMPLETED`)
