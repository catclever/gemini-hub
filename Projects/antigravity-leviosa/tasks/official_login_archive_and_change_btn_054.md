---
id: official_login_archive_and_change_btn_054
title: 修复官方登录账号 id_token_email 归档解析与 Change 按钮注入自动入库逻辑
status: completed
priority: high
tags:
- auth
- account-switcher
- bugfix
session: 6647124a-b312-40df-9900-1be74adcf62a
---

# 修复官方登录账号 id_token_email 归档解析与 Change 按钮注入自动入库逻辑

## 变更概述
1. 修复官方 Google OAuth 登录账号在 Token 刷新后 `jetski-standalone-oauth-token` / Keychain 仅保留 `id_token_email` 而无 `id_token` 导致 `getActiveAccountInfo()` 返回 `null` 的问题（兼容 `stored.id_token_email` 并在首次归档缺少头像时通过 `enrichActiveAccountProfile()` 自动拉取 Google UserInfo 补齐 `name` 与 `picture`）。
2. 优化 `web/account_login_inject.js` 中 Settings 面板 `Change` 按钮注入时的 `getCachedActive()` 逻辑，将只读 `get_active` 改为调用 `archive_current`，并在回到未登录欢迎页时重置 `cachedActiveAccount`，同时优先定位 `#other-sign-in-options` 容器注入欢迎页按钮。

## 验证结论
- [x] 核心逻辑已实现并通过验证
