---
description: 'macOS MediaRemote 通信协议、第三方应用精准播控、全生命周期窗口唤醒与 SwiftPM 6.3 资源 Bundle 解析架构规范'
---

# macOS MediaRemote 播控、窗口唤醒与 SwiftPM 资源 Bundle 架构规范

## 1. 媒体播控架构链路 (Media Playback Control Pipeline)

### 1.1 现状与分层策略
macOS 上的媒体应用分为两类：
1. **AppleScript 原生支持应用**：如 `com.apple.Music`、`com.spotify.client`，具备完整的 OSA Dictionary，可直接执行 `tell application id ... to playpause / next track / previous track`。
2. **非原生/自渲染第三方应用**：如网易云音乐 (`com.netease.163music`)、QQ 音乐 (`com.tencent.QQMusicMac`) 等。此类应用不支持标准 AppleScript 播放命令，且窗口常常采用自绘引擎。

### 1.2 播控命令派发三级降级机制
在 `MediaObserver.sendTargetedCommand(_:)` 中，播控必须严格按照以下顺序执行：
1. **第一级（Custom Cyber Handler）**：检查前端通过 WebSocket/RPC 注册的自制媒体处理器（如网页端注入脚本）；
2. **第二级（AppleScript Direct）**：命中白名单应用（`com.apple.Music`, `com.spotify.client`）时，执行预定义 AppleScript；
3. **第三级（MediaRemote Direct Adapter）**：
   - 针对非白名单或第三方播放器，严禁使用硬件按键模拟，必须直接调用 `mediaremote-adapter.pl <frameworkPath> send <commandId>`（基于 `MRMediaRemoteSendCommand` 私有 C API）；
   - 常用 Command ID 映射：
     - `2`: `kMRPlay` / `kMRPause` / `kMRTogglePlayPause`
     - `4`: `kMRNextTrack`
     - `5`: `kMRPreviousTrack`
   - 此通道无需目标应用处于前台焦点，在应用后台、最小化或隐藏时均可 100% 精准响应。

---

## 2. 媒体应用窗口全生命周期唤醒规范 (Window Activation SOP)

### 2.1 常见唤醒失效场景
- **Cmd+W 关闭窗口**：网易云等应用在按 `Cmd+W` 后，主窗口被销毁或隐藏，此时传统的 `runningApp.activate(options:)` 或单一 AppleScript `activate` 仅拉起菜单栏，无法重新拉起主界面；
- **全屏 / 跨 Space**：窗口存在于另一个虚拟桌面（Space），直接调用 AppKit 方法无法触发系统的跨桌面平滑过渡。

### 2.2 三步保活唤醒管线 (Three-Step Activation Pipeline)
在 `MediaObserver.activateMediaApp(bundleId:)` 中，必须按以下三步串行保证窗口唤出：
```swift
// 1. 确保未处于隐藏态 (Unhide)
if let runningApp = NSWorkspace.shared.runningApplications.first(where: { $0.bundleIdentifier == targetBundleId }) {
    runningApp.unhide()
}

// 2. 触发 AppleScript activate（强制激活并触发 macOS 跨桌面 Space 自动平移）
let scriptSource = "tell application id \"\(targetBundleId)\" to activate"
if let script = NSAppleScript(source: scriptSource) {
    var errorInfo: NSDictionary?
    script.executeAndReturnError(&errorInfo)
}

// 3. 触发 NSWorkspace.openApplication（关键：派发 kAEReopenApplication 事件）
// 针对 Cmd+W 关闭主界面的应用，kAEReopenApplication 会触发其 AppDelegate 的 applicationShouldHandleReopen，重建主窗口
if let url = NSWorkspace.shared.urlForApplication(withBundleIdentifier: targetBundleId) {
    let config = NSWorkspace.OpenConfiguration()
    config.activates = true
    NSWorkspace.shared.openApplication(at: url, configuration: config, completionHandler: nil)
}
```

---

## 3. SwiftPM 6.3+ 资源 Bundle 路径解析规范

### 3.1 Swift 6 产物结构变迁
- **构建输出目录**：Swift 6.3 默认输出目录从 `.build/arm64-apple-macosx/debug` 迁移至 `.build/out/Products/Debug/`。打包脚本必须优先检查该输出路径，杜绝复制陈旧二进制。
- **Bundle 结构嵌套**：SwiftPM 在 CLI/App 构建中生成的 `TaiChi_TaiChi.bundle` 遵循标准 macOS Bundle 规范：
  `TaiChi.app/Contents/Resources/TaiChi_TaiChi.bundle/Contents/Resources/Resources/<TargetResource>`
  直接使用 `Bundle.module.resourcePath + "/MediaRemoteAdapter/..."` 会因缺少嵌套的 `Resources` 层级导致路径失效。

### 3.2 自适应资源路径探测机制
凡涉及从子进程（如 Perl、Python 辅助脚本）加载打包资源的模块，严禁硬编码单一绝对路径，必须通过探测函数获取真实存在的文件目录：
```swift
private func resolveMediaRemoteDirectory() -> String? {
    let fm = FileManager.default
    var candidates: [String] = []
    if let mainRes = Bundle.main.resourcePath {
        candidates.append(mainRes + "/MediaRemoteAdapter")
        candidates.append(mainRes + "/Resources/MediaRemoteAdapter")
    }
    if let modRes = Bundle.module.resourcePath {
        candidates.append(modRes + "/MediaRemoteAdapter")
        candidates.append(modRes + "/Resources/MediaRemoteAdapter")
    }
    for dir in candidates {
        if fm.fileExists(atPath: dir + "/mediaremote-adapter.pl") {
            return dir
        }
    }
    return nil
}
```

---

## 4. 灵动岛显隐与流式播控状态解耦规范

### 4.1 轮询与流式监听职责分离
- `mediaremote-adapter.pl stream` 是**系统级权威全局播放状态源**（高频即时更新 `title`、`artist`、`isPlaying`、`elapsedTime`、`artworkData`）；
- `pollMediaApps()`（30秒周期）仅用于获取**支持 AppleScript 的辅助媒体应用列表**（`activeMediaApps`），严禁参与实时播控与首屏显隐仲裁。

### 4.2 显隐仲裁与防死锁规则
在 `IslandManager.isIslandVisibleDueToApps()` 中：
```swift
private func isIslandVisibleDueToApps() -> Bool {
    let state = MediaObserver.shared.state
    if state.status == .stopped {
        return false
    }
    // 只要权威流有曲目、正在播放，或轮询探测到活跃应用，灵动岛必须立即对用户可见
    return !state.title.isEmpty || state.isPlaying || !MediaObserver.shared.activeMediaApps.isEmpty
}
```
**防死锁要求**：
- 当应用启动时，若已有歌曲处于播放/暂停状态，必须在初始化阶段执行一次异步单次轮询（`triggerOneShotPoll()`）；
- `IslandManager` 必须同时监听 `MediaObserver.shared.$state` 与 `$activeMediaApps`，一旦曲目名称或播放状态到达，立即在主线程刷新 `positionWindow()` 并设置 `window.alphaValue = 1.0`。

---

## 5. 悬浮面板命中测试 (Hit-Testing) 与交互规范

### 5.1 AppKit 坐标系转换陷阱
在嵌入 SwiftUI 的 `NSHostingView` 或叠加在自定义图层之上的事件拦截视图（如 `RecordClickOverlay`）中：
- `NSView.hitTest(_ point: NSPoint)` 传入的 `point` 为父视图坐标系（`superview`）；
- 必须首先通过 `let localPoint = convert(point, from: superview)` 转换至当前视图坐标系，再进行 `bounds.contains(localPoint)` 判定，否则在复杂布局或多重嵌套视图下会导致点击事件被静默穿透丢弃。

### 5.2 唱片双模交互契约
- **左键单击**：0ms 延迟立即触发 `togglePlayPause`（极致响应）；
- **右键单击 / Control+左键**：触发当前媒体应用的保活唤醒（`activateMediaApp`），并配合 200ms 防抖计时器避免快速右键触发连续多进程拉起。
