---
id: refactor_settings_panel_pure_fullscreen_transparency_036
title: 重构设置面板为纯净全景透底并移除冗余独立背景层
status: completed
priority: medium
tags: []
session: fba8eb14-e6fb-4b79-a186-9eb1a0f0fda6
---

# 重构设置面板为纯净全景透底并移除冗余独立背景层

## 变更概述
按方案 A 彻底废弃并移除设置面板内注入的独立背景层节点 (leviosa-settings-panel-bg 与 leviosa-settings-sidebar-bg)，解除 container-type: size 引起的局部包含块隔离与二次缩放错位；通过 CSS 让设置面板外层容器纯净透明，直接打通底层 #root 全景大壁纸，右侧采用标准 65% + blur(12px) 毛玻璃，左侧保留 75% + blur(2px) 侧边栏质感，实现 0 跳动、像素级全景透底。

## 验证结论
- [x] 核心逻辑已实现并通过验证
