---
id: atproto_backend_publisher_115
title: ATProto PDS 鉴权推流发帖与 Frontmatter 无损回写
status: completed
priority: high
tags:
- backend
- go
- atproto
- publisher
- jules
session: conversation://34fd952a-c2fe-491e-be53-488c3ec6081a
---

# ATProto PDS 鉴权推流发帖与 Frontmatter 无损回写

## 任务目标与背景
在 modules/atproto/publisher/ 与 modules/atproto/config/ 中实现 Bluesky PDS 鉴权与手动推流发帖。
1. 扩展 config.Config 支持 4 级后备配置注入 (handle, app_password, pds_url)；
2. 实现基于 com.atproto.server.createSession 的会话管理、JWT Token 缓存与自动刷新；
3. 实现 PublishCard(card Card, filePath string) (uri string, cid string, err error): 调用 com.atproto.repo.createRecord 发布至 app.bsky.feed.post，自动解析 Facets (链接与标签)；
4. 发帖成功后，调用 watcher.GetWatcher().WriteFile 无损回写 uri、cid 和 published: true 至本地 Markdown 的 Frontmatter；
5. 编写 publisher_test.go 单元测试验证核心流程。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## Jules 会话跟踪
- **Jules Session**: `sessions/15424792741386391512`
- **Jules Web Console**: [https://jules.google.com/session/15424792741386391512](https://jules.google.com/session/15424792741386391512)
- **Watchdog Signal**: `/tmp/atproto_backend_publisher_115.signal`

## 验证结论与 PR 交付
- **Pull Request**: [https://github.com/catclever/Finnegan/pull/14](https://github.com/catclever/Finnegan/pull/14)
- **交付内容**: `publisher.go`, `session.go`, `facets.go` 实现 PDS 鉴权与 Token 维护，XRPC 发帖，URL/Mention/Tag 的 Facets 解析，以及 Frontmatter 无损回写。
- **验证结论**: 包含完整 httptest 单元测试 `publisher_test.go`，测试全量 PASS。
