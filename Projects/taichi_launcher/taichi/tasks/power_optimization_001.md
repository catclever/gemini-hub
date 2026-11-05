---
title: "Taichi 播放器与动画高功耗优化 (MediaRemote 轮询、唱片动画、歌词 Timer)"
status: completed
priority: high
tags: [power-optimization, timer, animation, media-remote]
session: "conversation://5be557f6-45a3-46ef-b995-7681379ee97a"
---

# Taichi 播放器与动画高功耗优化记录

## 1. 问题背景
在功耗与电池使用排查中，发现 Taichi 在后台或未播放音乐时存在多处高频唤醒 CPU/GPU 的逻辑：
1. **2 秒无条件 AppleScript 轮询**：无论是否播放音乐，系统每 2s 通过 AppleScript IPC 强行查询后台所有媒体软件状态。
2. **60 FPS 唱片旋转 Timer**：在主线程使用 16.6ms 间隔的 `Timer.scheduledTimer` 频繁修改 `@State var rotation`，迫使 SwiftUI 图层全频重绘。
3. **100ms 歌词与菜单栏 Timer**：即使未开启菜单栏显示或未播放音乐，10Hz 定时器依然在后台死循环唤醒主线程。

## 2. 重构与优化方案
全面落实 **“按需触发”** 原则，将所有动画与刷新逻辑与 `MediaObserver.shared.state.isPlaying` 播放状态进行生命周期联动：

- **`Sources/TaiChi/Island/MediaObserver.swift`**：
  - `startPoller()` / `pollMediaApps()` 增加 `isPlaying` 判定；未播放时不启动轮询。
  - 收到 MediaRemote 播放开始（`isPlaying == true`）时自动启动 Timer；收到暂停（`isPlaying == false`）时做单次状态同步，随后彻底销毁 Timer。
- **`Sources/TaiChi/Island/IslandView.swift` (`SpinningRecord`)**：
  - 移除 60 FPS 主线程 Timer，改为 SwiftUI 原生硬件加速动画 `.rotationEffect(.degrees(isPlaying ? 360 : 0))` 搭配 `.linear.repeatForever(autoreverses: false)`，交由 Metal 合成器高效渲染。
- **`Sources/TaiChi/Island/MenuBarLyricManager.swift`**：
  - 仅在 `showMenuBarLyrics == true` 且 `isPlaying == true` 时才启动 100ms 刷新 Timer。
- **`Sources/TaiChi/Island/ExpandedPanelView.swift` & `StandaloneLyricView.swift`**：
  - `.onReceive(timer)` 增加 `guard isPlaying` 判断，并在暂停/视图消失时即刻销毁 Timer。

## 3. 验证与打包
- **编译验证**：`swift build` 顺利通过（0 Error, 0 Warning）。
- **应用打包**：运行 `./build_app.sh` 生成包含优化代码与最新签名的 `TaiChi.app`。
