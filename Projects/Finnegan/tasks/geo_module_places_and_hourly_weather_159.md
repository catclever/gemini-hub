---
id: geo_module_places_and_hourly_weather_159
title: 实现地理位置与逐小时气象模块 (modules/geo) 及模块级地理权限中心
status: completed
priority: high
tags:
- geo
- weather
- module
- backend
session: conversation://c1672485-6e37-4151-b40f-453866902a63
---

# 实现地理位置与逐小时气象模块 (modules/geo) 及模块级地理权限中心

## 任务目标与背景
实现地理位置与历史/实况气象模块 (modules/geo)：
1. 模块级权限配置与守卫：在 finnegan.yml 的 geo 配置域支持 enabled、provider (auto/google/amap/osm)、google_api_key、amap_api_key、recommend_radius_m 以及 allowed_modules 模块白名单（如 ["diary"]），提供 IsModuleAllowed(moduleName) 与 check_permission Action。
2. 精确经纬度与地标 POI 抓取：内置 WGS-84 与 GCJ-02 自动纠偏，支持通过 Google Places / 高德 / OpenStreetMap 抓取周边地标元素辅助位置命名。
3. 本地位置记忆库 (<home>/.finnegan/places.yml)：基于 Haversine 球面距离自动推荐邻近已存位置；支持在极近距离或同坐标下创建多个不同名称的位置并自由选择；支持创建非当前范围内的远方位置。
4. 按小时气象查询与未来时间拦截：接入 Open-Meteo Forecast & Archive Hourly API，支持按指定时间（精确到小时）获取对应天气，且严格拦截未来时间（targetTime > now 返回错误）。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

- **Jules Cloud Session**: `sessions/10194634683386364511` (https://jules.google.com/session/10194634683386364511)
- **PVE Watchdog Log**: `/tmp/jules_geo_module_places_and_hourly_weather_159.log`
- **File Scope**: `modules/geo/*` (100% isolated from other parallel tasks)

- **PR Created**: https://github.com/catclever/Finnegan/pull/23 (`COMPLETED`)
