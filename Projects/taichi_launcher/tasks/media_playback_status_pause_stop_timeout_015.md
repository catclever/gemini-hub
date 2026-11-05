---
id: media_playback_status_pause_stop_timeout_015
title: 媒体管理状态细化：区分暂停与停止状态及10分钟超时状态机
status: in_review
priority: high
tags:
- media
- island
- lyrics
session: conversation://c34786fa-6f15-421a-95b4-9f7f7976af63
---

# 媒体管理状态细化：区分暂停与停止状态及10分钟超时状态机

## 任务目标与背景
区分媒体播放的「暂停」与「停止」两种状态：
1. 暂停状态：歌词保留、灵动岛依然保持外扩（不缩回），但停止所有动态动画（唱片停转、音波静止、走马灯文本静止、歌词时间不推进）。
2. 停止状态：灵动岛收起至基础刘海尺寸，歌词完全隐藏不再展示。
3. 手动操作限制：UI 与快捷键所有操作均为播放/暂停切换，不可手动直接进入停止。
4. 10分钟超时机制：进入暂停后启动10分钟倒计时；若10分钟内未恢复播放，自动转为停止状态并收起灵动岛。
5. 系统休眠唤醒：监听系统唤醒通知，核验暂停累计时间戳；若休眠跨越累计超过10分钟，唤醒后立即转入停止状态。
6. 恢复播放打断：一旦恢复播放，立即重置并打断10分钟倒计时。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

### 实施验证与交付记录
- 5个文件完成重构、备份与合并：
  - `MediaObserver.swift`: 引入 `MediaPlaybackStatus` (`.playing`, `.paused`, `.stopped`)；添加基于绝对时间戳的 10 分钟暂停定时器与 `NSWorkspace.didWakeNotification` 唤醒核验逻辑；流式与轮询双轨同步状态机；播放事件直接打断定时器。
  - `MarqueeText.swift`: 支持 `isPlaying` 响应，暂停时彻底注销 Task 并重置 offset，实现 0 CPU 唤醒与零视觉动态。
  - `IslandView.swift`: 暂停时歌词保持显示，灵动岛保持外扩；仅在 `.stopped` 时收起；唱片、音波、走马灯全部受 `isPlaying` 控制静止。
  - `StandaloneLyricView.swift`: 独立歌词窗适配暂停显示与无动态冻结。
  - `IslandManager.swift`: 将可见性统一委派至 `MediaObserver.shared.state.status`，去除冗余的局部计时器。
- 代码语法验证通过，`bash build_app.sh` 编译打包无误（遵循铁律未自动杀死或重启 App）。当前进入 `in_review` 待用户实测。

### Bug 修复：移除后台轮询对媒体状态的篡改
- **根因分析**：`performPolling` 仅轮询设置中预设的媒体 App。对于通过其他 App（如 `fun.upup.musicfree` 或浏览器）播放时，该轮询误将 `newActiveApps` 中未包含当前应用判定为「未在播放」，每 2 秒强行覆盖并触发 `.paused` 状态与定时器。
- **修复方案**：
  - 彻底剥离 `performPolling` 对 `state.status` 和 `state.isPlaying` 的读写，仅保留对 `activeMediaApps`（多 App 切换列表）的更新。
  - `parseJSON` 作为系统媒体状态的唯一权威来源，优化 `playbackRate` 与 `payload.playing` 的解析互斥容错。
- **构建状态**：执行 `bash build_app.sh` 编译完成。

### 增补：菜单栏歌词对齐暂停/停止状态机
- **问题**：`MenuBarLyricManager` 之前仅根据 `isPlaying` 执行 `orderOut` 隐藏，导致暂停时菜单栏歌词瞬间消失变成音符 `♪`。
- **修复**：
  - 在 `.paused` 状态下：菜单栏歌词保持常驻展示当前这行歌词（静态文本，禁用走马灯滚动），并停止 0.1s 定时器以确保 0 CPU 消耗。
  - 在 `.stopped` 状态下：菜单栏歌词收起，恢复为 `♪`。
  - 在 `.playing` 状态下：恢复 0.1s 定时器与动态滚动。
- **构建状态**：通过 `bash build_app.sh` 重新编译完成。

### 优化：调整后台多应用扫描轮询周期至 30s
- 将 `MediaObserver.pollerTimer` 的轮询周期由 2.0s 调整为 30.0s。
- 减少 93% 的后台 AppleScript 执行与 XPC 进程唤醒，极大降低后台待机功耗。
- 通过 `bash build_app.sh` 重新编译完成。

### 任务背景与核心目标
区分媒体播放管理的 `暂停 (paused)` 与 `停止 (stopped)` 两个明确状态：
1. **暂停状态 (paused)**:
   - 歌词保留展示，灵动岛与屏幕常驻歌词保持外扩/固定宽度；
   - 界面所有动态效果冻结（唱片旋转停止、音符波形静止、跑马灯停在当前、歌词滚动与高频定时器停止消耗，0 CPU/唤醒）；
   - 开启 10 分钟超时定时器，若 10 分钟内未恢复播放，则自动跃迁进入 `停止 (stopped)` 状态。
2. **停止状态 (stopped)**:
   - 灵动岛完全收起至基准刘海尺寸，歌词不再展示，状态栏回退为常驻静止音符 `♪`；
   - 媒体应用退出时清理媒体状态并立即进入 `stopped`。
3. **不可手动停止**:
   - 任何用户交互（灵动岛按钮、媒体快捷键、状态栏控制面板）仅触发播放/暂停，不能手动直接进入停止状态。
4. **休眠与唤醒处理**:
   - 监听 `NSWorkspace.didWakeNotification`，唤醒时以现实墙上时钟时间（Wall-clock time）比对暂停时间戳：若休眠时间累计超过 10 分钟，立即进入 `stopped` 并收起；若未超过，则按剩余时间续跑定时器。
5. **恢复播放打断**:
   - 任意时刻进入 `playing` 状态，立即打断并重置 10 分钟暂停定时器。
6. **修复暂停后菜单栏歌词消失变回音符♪缺陷**:
   - 根因 1：暂停时 `newState.elapsedTime` 未保留墙上时钟流逝时间，导致暂停时 `currentElapsedTime` 骤降回 0，引发歌词索引失真与重置。
   - 根因 2：`MediaObserver` 状态机过度保护判断 `self.state.status == .stopped` 导致暂停状态无法被稳定持久化。现已规范：有曲目信息时暂停必进入 `.paused` 并启动 10 分钟倒计时。
   - 根因 3：`MenuBarLyricManager` 暂停后停止定时器导致 WindowServer 异步更新状态栏宽度时悬浮窗未能对齐，并在空文本防守分支缺少曲目托底显示。现已补充下一 RunLoop 周期坐标同步与空歌词降级保护。

### 涉及修改文件
- `Sources/TaiChi/Island/MediaObserver.swift`: 
  - 增强 `currentElapsedTime`，暂停时瞬时冻结记录当前精准播放位置；
  - 优化 `parseJSON` 状态跃迁逻辑：有曲目存在时一律保持 `.paused` 状态并由 10 分钟定时器接管生命周期。
- `Sources/TaiChi/Island/MenuBarLyricManager.swift`:
  - 监听状态变化增加 `isPlaying` 触发维度；
  - 暂停状态保留当前静态歌词，更新并同步悬浮窗位置；
  - 空歌词安全回退至 `Title - Artist`，彻底防止意外回退为音符 `♪`。
- `Sources/TaiChi/Island/IslandView.swift`: 灵动岛根据 `.stopped` 区分收起与冻结外扩。
- `Sources/TaiChi/Island/StandaloneLyricView.swift`: 独立歌词栏根据播放状态启停 0.1s 驱动定时器。
- `Sources/TaiChi/Island/MarqueeText.swift`: 暂停时停用异步滚动任务并复位位移。

### 验收与验证
- `bash build_app.sh` 编译并打包完成 `TaiChi.app`。
- 遵循 Iron Rules：未执行任何杀进程与自动重启命令，待用户手动重启验证。
