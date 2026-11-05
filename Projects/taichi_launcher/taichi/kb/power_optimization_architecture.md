# Taichi 功耗控制与 Timer 生命周期管理规范 (Knowledge Base)

## 核心架构原则

为了保持 Taichi 作为轻量挂件/灵动岛软件的低功耗与高性能特性，所有涉及定时器（Timer）、动画（Animation）和跨进程查询（IPC/AppleScript）的功能模块必须严格遵守以下原则：

---

### 1. 媒体事件与轮询控制 (Media State & Poller)
- **事件优先**：以 `MediaRemote` 系统通知为第一数据源。只在系统暴露事件变更时响应。
- **轮询防死循环**：所有后台轮询 Timer（如多应用状态查询 `MediaObserver`）必须只在 `isPlaying == true` 时工作。
- **暂停销毁**：音乐暂停瞬间，执行一次单次状态更新后，必须立即 `invalidate()` / 彻底销毁 Timer，严禁后台无条件死循环轮询。

---

### 2. 动画渲染与 SwiftUI 图层刷新 (Animation & Rendering)
- **禁用高频 Timer 修改 `@State`**：严禁在 Swift 主线程通过 `Timer.scheduledTimer`（如 60 FPS / 16.6ms）频繁修改 `@State` 变量驱动旋转或位移。这会导致全图层 Invalidated。
- **使用硬件加速动画**：涉及持续旋转（如唱片 `SpinningRecord`），应优先使用 SwiftUI 声明式 `.rotationEffect(.degrees(...))` 与 `.linear.repeatForever(autoreverses: false)`，直接下沉至 Metal 与 WindowServer 处理。

---

### 3. UI 视图 Timer 生命周期 (View Timers)
- **按需开启**：菜单栏歌词（`MenuBarLyricManager`）、独立歌词面板（`ExpandedPanelView` / `StandaloneLyricView`）的 100ms 进度刷新定时器，只有在 **“功能开关开启”** 且 **“音乐正在播放”** 且 **“视图处于 Visible 状态”** 时才允许激活。
- **离开与销毁**：在 SwiftUI `.onDisappear` 或底层状态变为 `isPlaying == false` 时，必须立即 `cancel()` / `invalidate()`。
