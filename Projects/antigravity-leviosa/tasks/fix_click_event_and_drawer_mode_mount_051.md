---
id: fix_click_event_and_drawer_mode_mount_051
title: 修复选中文档Edit点击无响应及强制抽屉模式挂载
status: completed
priority: high
tags:
- file_editor
- bugfix
- event_handling
- drawer_mode
session: 426dd4ce-86f0-44a3-83f1-811899047778
---

# 修复选中文档Edit点击无响应及强制抽屉模式挂载

## 任务目标与背景
修复 mousedown/mouseup 事件竞争导致 click 被浏览器取消的缺陷，通过在 mousedown 阶段即刻捕获执行并增加点击中防卸载保护；同时修复 openFileInEditor 错误匹配无关 DOM 导致抽屉未能弹出的问题，保证对话选中文档时 100% 优雅以 Drawer 模式滑出。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
