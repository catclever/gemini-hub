---
title: Implement RxDB IPC Storage Plugin
status: completed
priority: high
tags:
- frontend
- backend
- rxdb
- wails
- sqlite
id: rxdb_ipc_002
---
# 实现 RxDB 的 IPC Storage 代理

**目标**:
打破 RxDB 默认的 IndexedDB 存储，实现一个自定义的 RxStorage，通过 Wails IPC 调用后端的 SQLite。

**关键步骤**:
1. Go 端实现通用的 KV/Doc 操作 API（接收 IPC 调用）。
2. TS/JS 端实现一套 `RxStorage` 接口，代理到 `window.go.main.App...`。
3. 跑通 RxDB 官方的基础测试用例以验证 Storage 可靠性。
