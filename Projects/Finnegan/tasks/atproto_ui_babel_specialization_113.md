---
id: atproto_ui_babel_specialization_113
title: Babel 卡片 Bluesky 蝴蝶图腾特化与转评交互区
status: completed
priority: high
tags:
- frontend
- svelte
- atproto
- babel
- jules
session: conversation://34fd952a-c2fe-491e-be53-488c3ec6081a
---

# Babel 卡片 Bluesky 蝴蝶图腾特化与转评交互区

## 任务目标与背景
在 frontend/src/components/cards/BabelCardBody.svelte 中实现 Bluesky 来源特化展示。
保持卡片类别为 babel (card.type === 'babel')，当识别到 card.origin === 'atproto' 或 card.sourceUrl 包含 bsky.app 时：
1. 顶栏将通用地球图标替换为天蓝色蝴蝶图标 🦋 与 @Handle 链接；
2. 420x420 聚焦态底栏展示专属转评赞微型交互区（💬 评论数、🔁 引用数、♥ 赞数），并支持点击 💬 抛出拉取回复事件。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## Jules 会话跟踪
- **Jules Session**: `sessions/9284366123349025568`
- **Jules Web Console**: [https://jules.google.com/session/9284366123349025568](https://jules.google.com/session/9284366123349025568)
- **Watchdog Signal**: `/tmp/atproto_ui_babel_specialization_113.signal`

## 验证结论与 PR 交付
- **Pull Request**: [https://github.com/catclever/Finnegan/pull/15](https://github.com/catclever/Finnegan/pull/15)
- **交付内容**: `BabelCardBody.svelte` 实现 Bluesky 来源检测 (`isBluesky`)、天蓝蝴蝶图腾 🦋、420x420 聚焦态转评赞微型操作栏与 `atproto:fetch_comments` 事件抛出。
- **验证结论**: 零文件冲突，Svelte 诊断检查通过。
