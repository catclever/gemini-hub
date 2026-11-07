---
title: DOM 注入兜底选择器泛匹配导致穿透至会话折叠框
description: 登录界面注入脚本因包含超宽正则 `/continue with google|google/i`，导致 Agent 执行带 google
  关键词的工具调用时被误判并注入账号选择按钮。
date: '2026-11-06'
---

# Post-Mortem: DOM 注入兜底选择器泛匹配导致穿透至会话折叠框

## 问题现象
在聊天会话中，当 Agent 执行带有 Google 关键词的搜索或分析工具时（例如 `Searched antigravity.google for...`），工具组折叠头部组件 `<button data-testid="tool-group-collapsible">` 与下方详情列表之间，被强行插入了两个账号管理按钮（`#leviosa-account-buttons-container`：选择已有账号、通过 Refresh Token 获取账号）。

## 根本原因
1. **兜底正则过于宽泛**：`account_login_inject.js` 中的 `tryInjectEntranceButtons` 在未找到 `.entrance-auth-panel` 时，使用兜底逻辑寻找 Google 登录按钮，但正则写成了 `/continue with google|google/i`。后面的 `|google` 分支导致任何 `textContent` 或 `title` 包含子串 `google` 的按钮都被判定为登录按钮；
2. **缺乏页面上下文作用域检查**：全局 `MutationObserver` 持续运行，在未确认当前处于未登录欢迎页的情况下，在已登录的工作区和会话界面中盲目执行注入；
3. **父容器降级假定脆弱**：匹配到折叠按钮后直接取其 `parentElement`（折叠组件的外层卡片 `<div class="relative">`）作为挂载目标，并在第一个按钮后插入容器，破坏了原有 Accordion 头部与内容区的紧凑结构。

## 防御措施与规范
1. **严禁在登录注入脚本中使用无边界的关键词泛匹配**：匹配第三方按钮必须采用严格锚定（如 `/^continue with google$/i`），严禁使用简单 `includes` 或包含 `|keyword` 的子串匹配；
2. **进入注入逻辑前必须先执行状态守卫（State Guard）**：如果是专属特定视图（如登录面板、欢迎屏）的注入，必须首先校验当前是否存在已登录主界面/工作区特征元素（如 `[data-turn-content]`, `[role="article"]`, `[data-testid="user-input-step"]`），若存在则立即终止；
3. **主动清理误注入残留**：在每次执行注入尝试前，先查询并移除当前页面会话流或非目标容器中已存在的误注入元素，确保界面状态自愈；
4. **挂载前校验目标容器合法性**：插入前必须校验 `targetCard` 及其祖先元素，确保不属于任何包含 `[role="article"]` 或 `[data-testid*="tool"]` 的非目标区域。
