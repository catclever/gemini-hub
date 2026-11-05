---
id: card_external_edit_hot_refresh_084
title: 卡片外部编辑后内容热更新与自动刷新同步
status: completed
priority: high
tags:
- frontend
- backend
- watcher
- hot-reload
session: conversation://23d9961a-73cc-490d-9a09-b0c7743584e9
---

# 卡片外部编辑后内容热更新与自动刷新同步

## 变更概述
修复卡片在外部编辑器（Qled 或系统默认编辑器）修改保存后，CosmicStage 舞台未自动刷新内容的问题。实现 GlobalWatcher 文件变更事件总线广播、ParseCardFile 解析及前端 card:updated 响应流。

## 验证结论
- [x] 核心逻辑已实现并通过验证

## 问题根因分析
1. `GlobalWatcher` 在检测到外部编辑器保存文件时，虽然正常计算哈希并发布了 `bus.EventFileModified`，但 Go 主线程未监听该事件向 Wails 前端抛出通知；
2. `App.svelte` 阶段仅在 `onMount` 时通过 `LoadLocalCards()` 读取一次静态数据，未建立 `card:updated` 的动态监听链路，导致内存中的卡片池（`cards`、`localVaultPool`、`memoryPool`）未能响应外部文件更新。

## 解决方案与实现
1. **统一文件解析能力**（`storage.go`）：
   - 提取 `ParseCardFile(filePath string) (*Card, error)`，统一 Frontmatter 元数据及标题正文提取逻辑；
   - 重构 `LoadLocalCards` 复用此方法。
2. **事件流打通与卡片重新加载**（`app.go` & `app_search_cmd.go`）：
   - 在 `app.go` 订阅 `bus.EventFileModified` 和 `bus.EventFileDeleted`，触发卡片重解析后通过 Wails IPC 广播 `card:updated` 和 `card:deleted`；
   - 在 `app_search_cmd.go` 抽象 `findCardPath` 路径解析器，并新增 `ReloadCard(cardID string) (*Card, error)` 绑定。
3. **前端舞台响应式同步**（`App.svelte`）：
   - 监听 `card:updated` 事件，基于 ID 与 FilePath 准确定位卡片，无缝更新 `cards`、`localVaultPool`、`memoryPool` 中的标题、内容与媒体资产，且保留 3D 物理空间坐标与动力学状态不变；
   - 监听 `card:deleted` 移除被删除卡片；
   - 监听窗口 `focus` 事件，当用户从 Qled 切回 Finnegan 时针对聚焦态卡片做瞬时补救性二次对齐。

## 验证
- Go 单元测试覆盖全套生命周期并通过：`ok Finnegan 6.145s`
- 前端 TypeScript 严格类型检查通过：`svelte-check 0 errors, 0 warnings`
