---
id: atproto_backend_discovery_114
title: ATProto 公共端点推文发现与评论抓取实现
status: completed
priority: high
tags:
- backend
- go
- atproto
- discovery
- jules
session: conversation://34fd952a-c2fe-491e-be53-488c3ec6081a
---

# ATProto 公共端点推文发现与评论抓取实现

## 任务目标与背景
在 modules/atproto/fetcher/fetcher.go 中实现基于公开端点 (public.api.bsky.app) 的 Bluesky 发现与评论拉取。
1. SearchSimilar(keywords []string, limit int) ([]Card, error): 调用 app.bsky.feed.searchPosts 检索推文，输出标准化 Card 结构体（Type: 'babel', Origin: 'atproto', SourceURL, AuthorName, AuthorAvatar, EchoOf）；
2. FetchComments(postURI string) ([]Card, error): 调用 app.bsky.feed.getPostThread 拉取回复树并平铺映射为 Card 结构体；
3. 编写 fetcher_test.go 单元测试，Mock HTTP 响应验证模型映射正确性。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## Jules 会话跟踪
- **Jules Session**: `sessions/10173078786280267305`
- **Jules Web Console**: [https://jules.google.com/session/10173078786280267305](https://jules.google.com/session/10173078786280267305)
- **Watchdog Signal**: `/tmp/atproto_backend_discovery_114.signal`

## 验证结论与 PR 交付
- **Pull Request**: [https://github.com/catclever/Finnegan/pull/11](https://github.com/catclever/Finnegan/pull/11)
- **交付内容**: `fetcher.go` 实现基于 `public.api.bsky.app` 的 `SearchSimilar` 与 `FetchComments`，将推文与回复树映射为 `Type: "babel"`, `Origin: "atproto"` 的卡片模型。
- **验证结论**: 包含完整 httptest 单元测试 `fetcher_test.go`，测试全量 PASS。
