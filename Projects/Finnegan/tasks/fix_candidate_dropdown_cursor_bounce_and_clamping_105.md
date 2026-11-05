---
id: fix_candidate_dropdown_cursor_bounce_and_clamping_105
title: 修复候选卡片下拉菜单键盘移动时光标被静止鼠标弹回与端点回绕问题
status: completed
priority: high
tags:
- frontend
- omnibar
- dropdown
- bugfix
session: 97aa8c6a-1720-45f1-a751-8213e8d557f9
---

# 修复候选卡片下拉菜单键盘移动时光标被静止鼠标弹回与端点回绕问题

## 变更概述
修复用户使用键盘上下键移动候选卡片高亮时被意外弹回的问题：1. 将 mouseenter 改为物理位移检验的 mousemove，防止列表在静止鼠标下方滚动时误触发高亮重置；2. scrollIntoView 改用 instant/auto 视口居中，消除 smooth 动画过程中的多重悬浮触发；3. 键盘上下移动限制在端点范围 [0, len-1]，防止翻到首尾时意外循环回绕跳跃。

## 验证结论
- [x] 核心逻辑已实现并通过验证
