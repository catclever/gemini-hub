---
id: unified_launcher_gateway_and_dual_track_routing_010
title: TaiChi 统一启动器网关与双轨联动路由升级
status: completed
priority: medium
tags:
- launcher
- alfred_integration
- gateway
- routing
session: conversation://29fd48b2-227d-4b2d-9cc2-ede7115b7f64
---

## 任务背景与目标
目前 TaiChi 在 `ServerManager.swift` 中仅硬编码了 `/api/launcher/filter` 用于过滤 `cyber` 应用。现需升级为通用的**统一启动器网关（Unified Launcher Gateway）**，支持 Alfred / Raycast 的双轨联动路由：
1. **统一前缀下钻**：`tai <subcommand> <query>`（如 `tai cyber ...`、`tai service ...`）
2. **直达前缀穿透**：`<subcommand> <query>`（如 Alfred 单独绑定 `cyber` 或 `service` 关键字触发）
3. **全局探索与导航**：当用户仅输入 `tai` 或未匹配子命令时，展示顶层模块导航卡片并支持跨模块聚合搜索。

本任务**仅聚焦于 TaiChi 启动器网关框架与路由层的升级**（不包含具体 service 的业务实现），为后续所有子服务提供可插拔的接入插槽。

---

## 核心设计规范

### 1. 协议化模块处理器 (`LauncherModuleHandler`)
建议抽取或定义模块协议，使各业务模块可独立注册：
```swift
protocol LauncherModuleHandler: Sendable {
    var namespace: String { get }       // 如 "cyber", "service", "wall", "agent"
    var displayName: String { get }     // 如 "⚡️ Cyber 注入应用"
    var subtitle: String { get }        // 如 "管理与启动注入版 Chromium/Electron 应用"
    var iconPath: String? { get }
    
    func handleFilter(query: String) async -> [[String: Any]]
    func handleAction(arg: String) async -> Bool
}
```

### 2. 双轨路由解析器 (`GET /api/launcher/filter`)
- 参数：`q`（查询字符串）、可选 `scope`（显式指定命名空间）
- 解析逻辑：
  1. **显式 Scope 匹配**：若 URL 携带 `scope=cyber`，直接定向分发给对应 Handler。
  2. **首词 Token 匹配**：将 `q` 按空格分词。若首词与任一注册 Handler 的 `namespace` 匹配（如 `q="cyber music"` 或 `q="service hf"`），剥离首词后将剩余参数传给该 Handler。
  3. **导航与全局聚合**：
     - 若 `q` 为空：输出所有已注册模块的导航卡片（回车自动补全对应命名空间）。
     - 若 `q` 非空且未匹配命名空间：并行请求所有 Handler，聚合其结果进行模糊匹配。

### 3. 统一动作分发 (`/api/launcher/action` 或统一拦截)
- Alfred / Raycast 选中条目后按回车，触发统一 Action 端点。
- 参数格式形如 `<namespace>:<action>:<params>`，由网关拆分后自动分发至对应的 `handleAction`。

### 4. 既有逻辑平滑迁移
- 将 `ServerManager.swift` 中原有的 Cyber 过滤与启动退出逻辑，平滑封装入 `CyberLauncherHandler`，确保现有 Alfred 的 `cyber` 命令完全向下兼容、不受任何影响。
- 为 `service` 命名空间预留注册插槽（`ServiceLauncherHandler` 存根），以便后续任务无缝挂载。

---

## 验证与验收标准
1. `swift build` 在 Swift 6 模式下零错误编译。
2. HTTP 路由验证：
   - `curl "http://127.0.0.1:8888/api/launcher/filter?q="` -> 返回顶层导航卡片
   - `curl "http://127.0.0.1:8888/api/launcher/filter?q=cyber"` -> 返回 Cyber 列表
   - `curl "http://127.0.0.1:8888/api/launcher/filter?scope=cyber&q="` -> 返回 Cyber 列表
   - `curl "http://127.0.0.1:8888/api/launcher/filter?q=tai%20cyber"` -> 返回 Cyber 列表
3. 原有 `cyber` 应用注入与启动功能完全正常。

## 变更概述与验证结论

1. **统一协议与网关核心**：
   - 在 [`Sources/TaiChi/LauncherGateway.swift`](file:///Users/kael/Projects/taichi_launcher/Sources/TaiChi/LauncherGateway.swift) 中定义了 `LauncherModuleHandler` 模块化协议与线程安全的 `LauncherGateway` 启动器网关。
   - 实现了双轨联动路由：支持显式 Scope 定向直达、首词 Token 匹配与前缀下钻（`tai <subcommand> <query>` 及 `<subcommand> <query>`）、顶层导航卡片展示（空查询或 `tai`），以及未匹配时的跨模块并行聚合搜索。
2. **模块解耦与既有平滑迁移**：
   - 提取并封装了 [`CyberLauncherHandler`](file:///Users/kael/Projects/taichi_launcher/Sources/TaiChi/LauncherGateway.swift)，保持既有 Chromium/Electron 应用探测与 CDP 注入启动行为 100% 兼容。
   - 注册了 [`ServiceLauncherHandler`](file:///Users/kael/Projects/taichi_launcher/Sources/TaiChi/LauncherGateway.swift) 存根，为后续 Descartes Hub / 系统服务管理无缝接入提供标准插槽。
   - 升级统一 Action 动作分发，支持 `<namespace>:<action>:<params>` 格式并自动兼容历史 payload 结构。
3. **网关适配器精简**：
   - 重构 [`Sources/TaiChi/ServerManager.swift`](file:///Users/kael/Projects/taichi_launcher/Sources/TaiChi/ServerManager.swift)，将 `/api/launcher/filter` 和 `/api/launcher/action` 委托至 `LauncherGateway.shared`，支持 URL Query 与 POST Body 自动百分比解码。
4. **编译与 HTTP 路由全项验证**：
   - `swift build` 在 Swift 6 严格并发模式下构建成功（零错误）。
   - 实机 HTTP 路由全覆盖验证通过：
     - `curl "http://127.0.0.1:9216/api/launcher/filter?q="` -> 返回顶层导航卡片
     - `curl "http://127.0.0.1:9216/api/launcher/filter?q=cyber"` -> 返回 Cyber 列表
     - `curl "http://127.0.0.1:9216/api/launcher/filter?scope=cyber&q="` -> 返回 Cyber 列表
     - `curl "http://127.0.0.1:9216/api/launcher/filter?q=tai%20cyber"` -> 返回 Cyber 列表
     - `curl "http://127.0.0.1:9216/api/launcher/filter?q=service"` -> 返回 Service 列表
     - `curl "http://127.0.0.1:9216/api/launcher/action?payload=service:noop"` -> 返回 `{"success": true}`
     - `curl "http://127.0.0.1:9216/api/launcher/action?payload=cyber:open:com.google.antigravity"` -> 返回 `{"success": true}`
