---
description: 'macOS 多显示器壁纸目标匹配机制、静默降级陷阱及屏幕拓扑同步规范'
---

# macOS 多显示器壁纸目标匹配机制与避坑规范

## 1. 现象与问题背景

用户在外接显示器（如 `2490W1`）上触发 `paper.change()` 时：
- Hammerspoon 前端提示 `TaiChi paper.change triggered successfully for screen: 2490W1`；
- 日志显示 `WallpaperAction: Set wallpaper for screen 37D8832A-2D66-02CA-B9F7-8F30A301B230 to ...`；
- **实际表现**：外接屏幕无变化，MacBook 内建 Liquid Retina XDR 显示屏壁纸被意外替换。

---

## 2. 根因剖析（三重穿透与静默降级陷阱）

整个调用链路跨越 Hammerspoon（前端交互）、TaiChi Swift 服务端（业务逻辑与壁纸源抓取）、Hammerspoon Action（系统 API 设壁纸）：

### 陷阱 1：Payload 关键元数据丢失
- `paper_client.lua` 正确获取到了聚焦窗口所属的外接屏对象，解析出 `screenName = "2490W1"` 与 `screenUUID = "674E49B2-..."`。
- 但向 TaiChi API 发送请求时，仅将 `screenUUID` 放入 JSON payload，丢弃了 `screenName`。在用户通常以屏幕名配置频道的场景下，失去了容错依据。

### 陷阱 2：屏幕拓扑缓存更新不及时与监听器异常
- TaiChi 的 `WallpaperManager` 维护了 `connectedScreens` 缓存。在应用启动后若未及时刷新，缓存中可能仅存内建主屏幕。
- `event_watcher.lua` 中原先调用了未定义的 `utils.getScreens({ includeVirtual = true })`，导致外接屏插拔/切屏事件未能稳定广播 `screensChanged` 给 TaiChi。

### 陷阱 3：未命中时的致命静默降级（Fatal Fallback）
- 在 `WallpaperManager.swift` 中：
  ```swift
  let targetScreens = screens.filter { $0.uuid == uuid || $0.name == uuid }
  await triggerAutoChange(for: targetScreens.isEmpty ? nil : targetScreens)
  ```
- 当外接屏未在当前缓存中命中时，`targetScreens` 为空，代码三元表达式传递了 `nil`。
- `triggerAutoChange(for: nil)` 的语义被定义为「若为 nil 则更新所有已连接屏幕」，导致其直接拉取缓存中的内建屏幕，触发了内建屏幕的壁纸更换。

---

## 3. 架构规范与修复方案

### 规范 1：双重标识透传 (Dual-Identifier Binding)
- 前端（Hammerspoon `paper_client.lua`）派发请求时，必须同时携带 `screenUUID` 与 `screenName`：
  ```lua
  local payload = {
      screenUUID = screenUUID,
      screenName = screenName
  }
  ```
- 后端（`ServerManager.swift` / `WallpaperManager.swift`）必须同时接收两项标识，并在候选屏幕中同时比对 `uuid` 与 `name`。

### 规范 2：严禁静默降级 (Strictly No Silent Fallback)
- **动态主动刷新**：当指定了目标屏幕但本地缓存未命中时，必须主动异步请求一次最新的屏幕拓扑：
  ```swift
  if let fetched = try? await HSManager.shared.fetchScreens(), !fetched.isEmpty {
      screens = fetched
      await MainActor.run { TaiChiSettings.shared.connectedScreens = fetched }
      // 二次匹配
  }
  ```
- **显式拦截与退出**：刷新后若依然无法匹配目标屏幕，**必须直接记录 Warning 并安全 return**，绝不允许传入 `nil` 降级为更改主屏幕或所有屏幕。
- 执行端（`wallpaper_action.lua`）：若传入了指定的 `screenUUID`/`screenName` 却无法在 `hs.screen.allScreens()` 中定位，必须抛出错误并退出，禁止 fallback 至 `hs.screen.mainScreen()`。

### 规范 3：标准化屏幕事件监听
- Hammerspoon 拓扑监听统一使用官方 API `hs.screen.allScreens()`，确保事件能 100% 触发派发至 TaiChi 的 `handleScreensChanged`。

---

## 4. 工程与构建避坑 (SwiftPM Gotcha)

- **Swift Package Manager 备份文件命名**：
  SwiftPM 会扫描 `Sources/` 目录下所有以 `.swift` 为后缀的文件。如果将备份文件命名为 `Foo.bak.swift`，SwiftPM 会将其一同加入编译，导致 `invalid redeclaration of 'Foo'` 符号重复声明错误。
  **铁律**：Swift 源文件备份必须使用 `.swift.bak` 后缀，绝对不能以 `.swift` 结尾。
