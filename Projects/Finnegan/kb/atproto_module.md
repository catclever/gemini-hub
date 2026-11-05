---
title: "AT Protocol 模块 (AtProto Module)"
date: 2026-10-28
status: active
tags: [architecture, module, atproto, wails, omnibar, babel]
---

# AT Protocol 模块文档

`atproto` 是 Finnegan 的核心网络模块之一，负责将本地的“意识流卡片”与远端的 Bluesky (AT Protocol) 联邦宇宙桥接。

## 1. 架构定位
- **完全插件化与契约遵守**: 实现了 `core/module.Module` 与 `core/module.CommandProvider` 接口。
- **无感多态（形态与来源解耦）**: 远端发现与评论完全保持 `card.type === "babel"`，仅通过 `origin: "atproto"` 进行子类特化渲染。这种解耦完整保护了全局生命周期机制（如候选框过滤规则 `ExcludedTypes: ["note", "babel"]`、24小时 Pre-Inbox 挥发与显式收集转正）。
- **完全手动发布 (Zero Auto-Publish)**: 严格遵守“发帖自由”，去除了底层文件看门狗（Watcher）的自动发布监听，所有的发布与查询操作必须由 OmniBar 显式命令或卡片交互触发。

## 2. 模块专名体系与 OmniBar 命令 (`module.CommandProvider`)

模块定义了专名命名空间 `Namespace: "bsky"`，并向全局 OmniBar 注册了主命令与子命令：

### 2.1 专名主命令：`/bsky` 灵感回声 (`atproto:echo`)
- **专名**: `bsky` (`IsPrimary: true`)
- **触发词**: `bsky` (`/bsky`)
- **参数规格**: `ParamTypeCard`，`RequireKeywords: true`，`ExcludedTypes: ["note"]`，`AutoStageToViewport: true`。
- **运行链路**:
  1. OmniBar 选择卡片后，提取卡片关键词（或由卡片正文自动分词）；
  2. 前端触发 `buguController.startRadar` 激活母卡雷达波纹与光标；
  3. 后端异步调用 `fetcher.SearchSimilar(keywords, 10, cardID)`；
  4. 检索结果包装为 `models.Post` 并注入 `bus.GetBus().Publish(EventBabelCardSpawned)`；
  5. `app.go` 消费事件并注入 `CardManager`，同时向前端广播 `bugu:card_spawned`；
  6. 检索完成触发 `EventBuguRadarCompleted` 结束雷达扫描状态。

### 2.2 专名子命令：`/bsky-push` 手动发布 (`atproto:publish`)
- **专名**: `bsky` (`IsPrimary: false`, `SubCommand: "push"`)
- **触发词**: `bsky-push` (`/bsky-push`)，同时支持空格连缀解析（`/bsky push`）
- **参数规格**: `ParamTypeCard`，`RequireKeywords: false`，`ExcludedTypes: ["babel"]`（禁止直接转发生态外卡），`AutoStageToViewport: true`。
- **运行链路**:
  1. 读取本地 Markdown 文件正文；
  2. 剥离旧 YAML Frontmatter，通过已鉴权 PDS Session 创建 `app.bsky.feed.post` 记录；
  3. 自动解析 Facets（链接、Mention、Tag 字节偏移）；
  4. 无损写回 `uri`, `cid`, `published: true` 元数据至本地原 Markdown 文件。

## 3. UI 视觉特化与光线交互

### 3.1 Babel 卡片 Bluesky 多态展示 (`BabelCardBody.svelte`)
- **识别条件**: `isBluesky = card.origin === 'atproto' || (typeof card.sourceUrl === 'string' && card.sourceUrl.includes('bsky.app'))`
- **标头视觉**: 渲染蓝色蝴蝶标识 `🦋 @{card.authorName}` 与可点击外链。
- **420x420 聚焦模态底部交互栏**:
  - 磨砂玻璃毛玻璃卡条，显示实时转评赞计数：`💬 {replyCount}`、`🔁 {repostCount}`、`♥ {likeCount}`。
  - 点击 `💬` 按钮，通过 Wails 运行时分发 `atproto:fetch_comments`，传递 `{ uri: card.sourceUrl, parentCardId: card.id }`。

### 3.2 突触光纤网络联动 (`BuguRayNetwork.svelte`)
- 突触光线检测逻辑扩展为 `(child.origin === 'bugu' || child.origin === 'atproto') && child.echoOf`。
- 当通过 `/bsky` 发现回声或通过 `💬` 展开评论推文时，生成的子卡片与母卡之间将实时投射出定向脉冲光纤（Directed Decaying Cross-Screen Rays），呈现立体的联邦宇宙思想回声网络。
