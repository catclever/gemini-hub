---
id: fix_conversation_viewport_bottom_shadow_034
title: 消除对话视口底部黑色渐变遮罩与脏阴影边
status: completed
priority: medium
tags: []
session: fba8eb14-e6fb-4b79-a186-9eb1a0f0fda6
---

# 消除对话视口底部黑色渐变遮罩与脏阴影边

## 变更概述
在透明壁纸主题下，由于原生主题 --background 变量指向深黑，导致对话视口底部的滚动淡出渐变遮罩 (from-background) 与输入框上边沿阴影呈现出脏黑横条。通过在 background.js 中针对 conversation-view 与 autoscroll-viewport 增强渐变与阴影消杀规则，还原晶莹通透的视觉质感。

## 验证结论
- [x] 核心逻辑已实现并通过验证
