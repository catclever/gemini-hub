---
title: "AT Protocol 发现机制设计 (Discovery Mechanisms)"
date: 2026-10-11
status: tentative
tags: [architecture, atproto, discovery]
---

# AT Protocol 发现机制演进路线

基于 Finnegan 的 Local-First 与“意识流沙盒”理念，网络交互不应是主动的浏览（刷 Feed），而应是被动的“降维与捕获”。

除了 MVP 阶段的“搜索相似帖子 (Search)”与“拉取本地交互 (Thread)”外，未来还规划了以下四种高级发现机制，统一通过 `atproto` 代理捕获，并作为 `DocSaveRequest` 沉淀入本地 Inbox。

## 1. 自定义信息流订阅 (Curated Streams)
- **原理**: 调用 XRPC `app.bsky.feed.getFeed`。
- **机制**: 允许用户订阅第三方开发者编写的特定算法 Feed（例如 #LocalFirst 专属流、学术流）。
- **落盘**: 系统通过定时任务（Cron），每日清晨拉取特定 Feed 的 Top N 帖子，静默投递至 Inbox，实现高信噪比的被动知识摄入。

## 2. 深海声纳监听 (The Firehose Radar)
- **原理**: 订阅全局 WebSocket 状态机 `com.atproto.sync.subscribeRepos`。
- **机制**: 抛弃传统 HTTP 轮询，采用持久化长链接，用极低的资源和纯文本正则监听全网每一秒涌现的帖子。
- **落盘**: 一旦匹配到设定的极端冷门关键词（如极其特定的学术概念），在毫秒级内抓取落盘。这是真正的“跨时空共鸣”。

## 3. 数字邻居脑图同步 (Neighborhood Sync)
- **原理**: 调用 XRPC `app.bsky.feed.getAuthorFeed`。
- **机制**: 用户指定若干高度认同的思考者 DID 作为“数字邻居”。
- **落盘**: 定期全量或增量同步这些思考者的公开帖子，化为本地卡片。本质上是把别人的“数字大脑”缓存到本地进行双链图谱合并。

## 4. 引用与反向链接发现 (Backlink / Quote Discovery)
- **原理**: 监听通知流 `app.bsky.notification.listNotifications`。
- **机制**: 将广域网上的 Mention（提及）和 Quote（引用）行为，等价映射为本地笔记系统中的 Backlink（反向链接）。
- **落盘**: 当远端发生引用时，提取引用者的语境与正文，作为子卡片或关系元数据存入本地 SQLite。在本地阅读原卡片时，可直接看到全网的“思想回声”。

## 5. 设计哲学勘误与边界重申 (2026-10-12 更新)
**“发现” (Inflow) 允许自动化，但“发布” (Outflow) 必须绝对手动。**

早期的设计曾考虑将 `atproto` 模块与全局文件看门狗（Global Watcher）深度绑定，一旦检测到文件 YAML 中的 `publish: true` 标签发生变化，即自动触发远端发帖。

经过 2026-10-12 的架构审查，该“自动发布”逻辑已被**永久否决**，原因如下：
1. **用户意志不可侵犯**：草稿的随意保存（Cmd+S / 远端 Mutagen 同步）可能误触自动监听器，导致半成品内容被强制推流至联邦宇宙。
2. **纯粹的模块解耦**：`atproto` 模块的发布能力 (`PublishNote`) 被剥离为纯粹的 RPC 方法，交由 Wails 前端 (Svelte) 显式调用。只有当用户在界面中按下具体的“推流”按钮时，才允许执行广域网写入。
