---
id: fix_secondary_sidebar_and_aux_pane_background_loss_038
title: 修复二级侧边栏与Subagent任务面板背景丢失变黑问题
status: completed
priority: high
tags: []
session: fba8eb14-e6fb-4b79-a186-9eb1a0f0fda6
---

# 修复二级侧边栏与Subagent任务面板背景丢失变黑问题

## 变更概述
排查并修复由于此前选择器过度限定为 :has(button[data-testid^="settings-nav-item-"]) 且被 border-sidebar-border 豁免规则误伤，导致 Subagents / Background Tasks / Artifacts 等二级侧边栏与导航面板失去壁纸变纯黑的问题。现已全面放开选择器至所有二级 .bg-sidebar 与 container-type: size 容器，使所有二级侧边栏与主工作区无缝继承 background-attachment: fixed 全景壁纸与毛玻璃质感。

## 验证结论
- [x] 核心逻辑已实现并通过验证
