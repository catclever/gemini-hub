# macOS 状态栏歌词与桌面灵动岛功耗深度优化规范

## 1. 状态栏动画架构与 `_updateReplicants` 陷阱 (Critical)
- **底层机制**：在 macOS 11+ 架构下，`NSStatusItem` 由系统的 `ControlCenter` 进程托管。任何嵌入在 `NSStatusItem.button` 内部的高频子视图移动（如 `animator().frame` 或高频 Timer 修改 `origin.x`）都会触发 AppKit 的 `-[NSStatusItem _updateReplicants]`。这会导致主线程每帧调用 CPU 软件光栅化（`CALayer.renderInContext:`）截图，并通过 XPC 围栏（`CAFenceHandle`）强制同步 `ControlCenter` 和 `WindowServer`，使 CPU 占用飙升至 50%+。
- **最佳实践（Floating Overlay Window）**：
  - 严禁在 `NSStatusItem.button` 内部做动画。
  - 使用独立的透明穿透 `NSPanel`（`.statusBar` 窗口层级，`ignoresMouseEvents = true`，`backgroundColor = .clear`，`hasShadow = false`）精确覆盖在 `NSStatusItem.button` 屏幕坐标上方。
  - `NSStatusItem.button` 仅作为透明占位与鼠标点击捕获器。
  - 动画由独立的 `NSPanel` 承载，直接走 GPU/Metal 硬件合成，CPU 占用降至 <0.5%。
  - 暂停时悬浮窗 `orderOut(nil)`，状态栏原生显示 `"♪"`。

## 2. 状态栏文字在多显示器与壁纸下的自适应 (Appearance Adaptation)
- **动态外观镜像**：macOS 底层会根据每个显示器顶部壁纸的明暗度自动为 `statusItem.button.effectiveAppearance` 分配 `.aqua`（浅色壁纸）或 `.darkAqua`（深色壁纸）。
- **纯透明文本色彩映射**：
  - 严禁在悬浮穿透窗中使用带磨砂背景的 `NSVisualEffectView`（会产生丑陋的灰色底板矩形）。
  - 直接在更新位置时读取 `button.effectiveAppearance.bestMatch(from: [.darkAqua, .aqua])`，动态计算文本对比度：深色壁纸使用 `white.withAlphaComponent(0.95)`，浅色壁纸使用 `black.withAlphaComponent(0.90)`。
  - 监听 `NSApplication.didChangeScreenParametersNotification` 和 `NSWorkspace.activeSpaceDidChangeNotification` 实现跨屏与切桌面时的外观无缝跟随。

## 3. SwiftUI 幽灵窗口与后台 Timer 冻结
- **隐藏窗口脱离合成**：仅设置 `alphaValue = 0.0` 无法阻止 WindowServer 合成背后的毛玻璃与图层。隐藏状态下必须调用 `window.orderOut(nil)`，显示时再 `orderFront(nil)`。
- **严格绑定 Timer 生命周期**：独立歌词窗（`StandaloneLyricView`）必须同时校验 `isLyricPinned && isLyricDetached && isPlaying`，否则在隐藏状态下每 0.1 秒都会触发 `body` 重新求值。

## 4. AppleScript 预编译缓存与 XProtect/YARA 防抖
- **问题**：每次调用 `NSAppleScript(source:)` 编译脚本源码时，macOS 安全子系统（`libInterpreterSecurity.dylib`）都会拉起 `XProtect` 重新解析编译全套 YARA 规则，在 2 秒轮询下造成持续 CPU 尖峰。
- **方案**：使用串行队列和预编译字典 `[String: NSAppleScript]` 缓存已编译脚本实例，整个生命周期只编译 1 次。
