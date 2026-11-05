---
id: fix_session_switcher_ctrl_tab_032
title: 修复 Ctrl+Tab 会话切换快捷键在 Antigravity 新版 DOM 下失效的问题
status: completed
priority: high
tags:
- bugfix
- session-switcher
- ui
- keyboard-shortcuts
session: a7074977-07c6-4fd1-b05e-03fefc179bb8
---

# 修复 Ctrl+Tab 会话切换快捷键在 Antigravity 新版 DOM 下失效的问题

## 任务目标与背景
由于 Antigravity 侧边栏 DOM 结构变更（移除 span[data-testid^='convo-pill-']，替换为 [data-testid='conversation-row-sidebar']），导致 Ctrl+Tab 无法捕获会话列表。升级选择器并引入 TanStack Router 原生 SPA 路由与 Fiber 点击兼容，同时支持快速连续切换状态防抖。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
