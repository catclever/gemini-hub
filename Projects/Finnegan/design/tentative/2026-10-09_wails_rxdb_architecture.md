---
title: "Wails + RxDB 跨进程存储架构选型"
date: 2026-10-09
status: active
---

# 架构选型：Wails + RxDB + IPC SQLite

## 1. 核心决策
为了兼顾 Finnegan 的“意识流瀑布交互 (RxDB 响应式)”和“百万卡片深网吞吐 (SQLite 原生性能)”，决定采用 **流派 3 (梦幻联动)**。

- **后端 (Go / Wails)**: 负责硬核的文件系统读写 (`fsnotify`)、SQLite 数据库的维护、以及深网探针（已有的 Bugu 模块）。
- **前端 (Vue/React / Webview)**: 负责 GUI 瀑布流渲染，采用 RxDB 作为状态管理器，**但通过自定义的 Storage Plugin，将其底层读写代理至后端的 SQLite**。
- **通信 (Wails IPC)**: 桥接前端 RxDB 和后端 SQLite 的专属通道。

## 2. 数据流转与懒加载 (Reactive Cache)
- **后端 (Go / SQLite)**: 绝对的“重型仓库”，负责海量数据的全量存储、分页 (`LIMIT/OFFSET`) 和全文检索。
- **前端 (RxDB Memory)**: 降级为“响应式橱窗 (Working Set)”。完全不落盘（不使用 IndexedDB），仅在内存中缓存当前视图需要展示的卡片。
- **懒加载 (Lazy Load)**: GUI 瀑布流初始仅拉取 50 张卡片。向下滚动时，通过 IPC 向 Go 请求下一页数据，并 `upsert` 进前端内存。
- **点对点响应**: 物理文件被 VS Code 修改 -> Go 更新 SQLite -> Go 广播单条卡片变动至前端 -> RxDB 内存池更新 -> 瀑布流对应卡片局部瞬间重绘。

## 3. 为什么不妥协
- 避免了 IndexedDB 的存储瓶颈和数据冗余。
- 维持了前端高度的响应式 (Reactive) 开发体验。
