---
id: fix_settings_panel_fixed_viewport_background_loss_037
title: 修复设置面板丢失壁纸并实现固定视口锚定全景裁剪
status: completed
priority: high
tags: []
session: fba8eb14-e6fb-4b79-a186-9eb1a0f0fda6
---

# 修复设置面板丢失壁纸并实现固定视口锚定全景裁剪

## 变更概述
针对设置面板完全失去背景图的问题，通过为设置面板宿主容器、左侧 200px 导航以及右侧主内容区注入 background-attachment: fixed 全局视口绝对锚定壁纸，使背景图像素级锁定 Viewport 坐标系，彻底消灭二次缩放与错位，并杜绝 JS 动态坐标跳变。

## 验证结论
- [x] 核心逻辑已实现并通过验证
