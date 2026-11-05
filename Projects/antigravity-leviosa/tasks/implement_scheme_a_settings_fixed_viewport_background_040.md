---
id: implement_scheme_a_settings_fixed_viewport_background_040
title: 实现方案A：设置面板最外层卡片原生Fixed视口直通壁纸
status: completed
priority: high
tags: []
session: fba8eb14-e6fb-4b79-a186-9eb1a0f0fda6
---

# 实现方案A：设置面板最外层卡片原生Fixed视口直通壁纸

## 变更概述
落实方案A：彻底移除设置面板内层独立的缩略图注入节点，通过将原生固定视口背景 (background-attachment: fixed) 绑定在设置弹窗最外层卡片容器上，实现1:1全景连续同轴截取与零JS坐标振颤，并精确隔离侧边栏边框规则避免次级面板黑屏。

## 验证结论
- [x] 核心逻辑已实现并通过验证
