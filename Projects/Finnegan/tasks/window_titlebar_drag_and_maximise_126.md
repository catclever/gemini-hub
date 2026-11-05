---
id: window_titlebar_drag_and_maximise_126
title: 修复 macOS 窗口拖拽移动失效并支持双击最大化
status: completed
priority: high
tags:
- ui
- wails
- macos
- window
session: b5da6de9-a9a5-4cc4-98d1-b7e11ede2050
---

# 修复 macOS 窗口拖拽移动失效并支持双击最大化

## 变更概述
通过新增 WindowTitleBar 组件，声明 --wails-draggable: drag 与 -webkit-app-region: drag，预留左侧 76px 原生红绿灯避让区，并将层级提升至 z-index: 9999 避免被全屏遮罩遮挡，同时绑定双击窗口最大化/还原交互。

## 验证结论
- [x] 核心逻辑已实现并通过验证
