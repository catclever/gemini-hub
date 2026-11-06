---
id: frontend_time_weather_emblem_and_omnibar_diary_bar_161
title: 实现「昼夜时辰×天气」联动天象徽章与 OmniBar 日记时空胶囊栏
status: completed
priority: high
tags:
- diary
- geo
- omnibar
- frontend
session: conversation://c1672485-6e37-4151-b40f-453866902a63
---

# 实现「昼夜时辰×天气」联动天象徽章与 OmniBar 日记时空胶囊栏

## 任务目标与背景
实现前端「昼夜时辰 × 天气」联动天象徽章与 OmniBar 日记时空胶囊栏：
1. 昼夜时辰 × 天气联动 SVG 徽章 (TimeWeatherEmblem.svelte & src/lib/diaryGeo.ts)：将 24 小时昼夜时辰（破晓、晨光、正午、夕照、初夜、深宵）与气象状态（晴、少云、阴、雨、雷、雪、雾）融合为双层动态矢量天象图标，拒绝呆板文字展示，支持散落态与聚焦态复用及悬停详情提示。
2. OmniBar 日记时空胶囊栏 (DiarySpatiotemporalBar.svelte & OmniBar.svelte)：当切换至 :diary 且模块拥有地理权限时，在输入框上方展示时空胶囊，支持自动推荐邻近位置、切换极近距离的不同位置命名、点选周边地图地标或新建自定义位置名，并支持回拨历史小时（严格禁选未来时间）实时刷新联动天象图标。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

- **Jules Cloud Session**: `sessions/4805280204560462281` (https://jules.google.com/session/4805280204560462281)
- **PVE Watchdog Log**: `/tmp/jules_frontend_time_weather_emblem_and_omnibar_diary_bar_161.log`
- **File Scope**: `frontend/src/types/card.ts`, `frontend/src/lib/cardType.ts`, `frontend/src/lib/diaryGeo.ts`, `frontend/src/components/cards/TimeWeatherEmblem.svelte`, `frontend/src/components/omnibar/DiarySpatiotemporalBar.svelte`, `frontend/src/components/OmniBar.svelte`

- **PR Created**: https://github.com/catclever/Finnegan/pull/24 (`COMPLETED`)
