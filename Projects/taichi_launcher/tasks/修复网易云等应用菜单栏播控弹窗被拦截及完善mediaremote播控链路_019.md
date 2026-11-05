---
id: 修复网易云等应用菜单栏播控弹窗被拦截及完善mediaremote播控链路_019
title: 修复网易云等应用菜单栏播控弹窗被拦截及完善MediaRemote播控链路
status: completed
priority: medium
tags: []
session: null
---

# 修复网易云等应用菜单栏播控弹窗被拦截及完善MediaRemote播控链路

## 任务目标与背景
解决网易云音乐等非 AppleScript 白名单应用在菜单栏歌词无法点击弹出播控浮层的问题，并将 sendTargetedCommand 和 toggleApp 升级为优先通过 MediaRemote 原生发送播控指令，确保网易云、QQ 音乐等应用能够稳定播控。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

### 根因排查与修复完成
1. **菜单栏歌词单机弹窗拦截根因**：
   - `MediaObserver.swift` 中的 `isPlaybackControlSupported()` 之前硬编码限制仅支持 Apple Music 和 Spotify (`["com.apple.Music", "com.spotify.client"]`)。当播放网易云音乐、QQ 音乐或其它媒体时，此方法直接返回 `false`，导致 `MenuBarLyricManager.handleStatusItemClick` 判定不支持播控而直接 `return` 退出，使得播控 Popover 无法弹出。
   - **修复**：更新 `isPlaybackControlSupported()` 判定逻辑，只要系统当前有活动音频（有曲目名、处于播放状态或有媒体 Bundle ID），均支持弹出菜单栏播控浮层。
2. **播控执行链路升级（MediaRemote 原生控制）**：
   - 经实测，网易云音乐 Mac 客户端不响应 AppleScript 的 `playpause` 词典；原本代码在 AppleScript 报错后降级至模拟硬件媒体键 `simulateMediaKey`，在部分状态下由于没有获得焦点无法接收系统级 F8。
   - 重新启用了 `MediaRemoteAdapter` 脚本通道（`mediaremote-adapter.pl send 2/4/5`），并通过 `/usr/bin/perl` 直接调用系统级 `MediaRemoteAdapter.framework`，移除了存在 SIGSEGV 崩溃风险的 `mr_target` 二进制。现在切歌与播放/暂停指令能直接、稳定地投递至系统活动播放器（包括网易云音乐）。

### 补充根因排查：为什么此前重新打包的 `TaiChi.app` 未生效？
1. **`build_app.sh` 产物路径陈旧导致一直拷贝 10 月 29 日的旧二进制（核心根因）**：
   - 升级 Xcode / Swift 6.3 后，`swift build` 的新编译产物输出在 `.build/out/Products/Debug/TaiChi`，但磁盘上残留了 10 月 29 日的旧目录 `.build/arm64-apple-macosx/debug/TaiChi`；
   - `build_app.sh` 原逻辑优先判断 `if [ -d ".build/arm64-apple-macosx/debug" ]`，导致每次执行 `bash build_app.sh` 虽然编译成功，最终拷贝进 `TaiChi.app/Contents/MacOS/TaiChi` 的却是 **10 月 29 日的旧二进制**（二进制校验显示 `RecordClick`、`Activating media app`、`Sending MediaRemote command` 均为 `False`）！
   - **修复**：清理残留的 `.build/arm64-apple-macosx` 目录，并更新 `build_app.sh` 优先读取 `.build/out/Products/Debug`。
2. **网易云音乐关闭主窗口（`Cmd+W`）状态下的唤起修复**：
   - 当网易云主窗口被关闭（仅驻留后台/状态栏）时，单独执行 AppleScript `tell application id "com.netease.163music" to activate` 不会报错但也不会重新打开主窗口；
   - **修复**：在 `activateMediaApp` 中执行 AppleScript 激活后不再提前 `return`，而是继续调用 `NSWorkspace.shared.openApplication(at:configuration:)` 发送 `kAEReopenApplication` 事件，确保关闭的主窗口也能被立即重新拉起。
3. **灵动岛常态左侧小唱片同步接入 `RecordClickOverlay`**：
   - 将 `IslandView.swift` 左侧小唱片也由 `.onTapGesture` 升级为 `RecordClickOverlay`，使常态小唱片与展开面板大唱片一致支持「左键单击播放/暂停、右键单击唤起播放器」。

- **根因 1 (菜单栏歌词播控弹窗被拦截)**: `MediaObserver.isPlaybackControlSupported()` 原先硬编码仅允许 `["com.apple.Music", "com.spotify.client"]` 返回 `true`，导致网易云音乐 (`com.netease.163music`)、QQ音乐等应用在 `MenuBarLyricManager.handleStatusItemClick` 中被 `guard MediaObserver.shared.isPlaybackControlSupported() else { return }` 直接拦截返回。
- **根因 2 (`mr_target` 崩溃与焦点依赖)**: `MediaObserver.sendCommand` 原先调用的 `mr_target` 二进制文件在当前系统下触发 `SIGSEGV (exit code 139)` 崩溃，而 `simulateMediaKey` 模拟硬件按键在无焦点或部分第三方播放器下不生效。
- **根因 3 (`build_app.sh` 旧产物缓存)**: Swift 6.3 (`swift-build`) 将最新编译产物输出在 `.build/out/Products/Debug/TaiChi`，而 `build_app.sh` 原先优先检查 `.build/arm64-apple-macosx/debug`（10月29日旧产物），导致新代码未被拷贝进 `TaiChi.app/Contents/MacOS/TaiChi`。
- **根因 4 (`Bundle.module.resourcePath` 目录层级差异与 `isIslandVisibleDueToApps` 可见性死锁)**:
  - Swift 6.3 生成的 `TaiChi_TaiChi.bundle` 为标准 macOS Bundle 结构（`Contents/Resources/Resources/MediaRemoteAdapter`），`Bundle.module.resourcePath` 指向 `Contents/Resources`，导致原先拼接 `/MediaRemoteAdapter/mediaremote-adapter.pl` 找不到脚本，`mediaremote-adapter.pl stream` 启动失败；
  - 轮询间隔改为 30s 后，`startPoller()` 未立即执行首次轮询，且 `IslandManager.isIslandVisibleDueToApps()` 原先仅判断 `!activeMediaApps.isEmpty`，导致收到 MediaRemote 流式曲目信息时窗口 `alphaValue` 仍为 `0.0`。
- **修复方案**:
  1. 在 `MediaObserver` 中新增 `resolveMediaRemoteDirectory()`，自动探测 `Bundle.main.resourcePath` 与 `Bundle.module.resourcePath` 下的 `MediaRemoteAdapter` 及 `Resources/MediaRemoteAdapter` 路径并校验 `mediaremote-adapter.pl` 存在性；
  2. 将 `MediaObserver.isPlaybackControlSupported()` 放宽为只要存在有效曲目、播放状态或 `bundleIdentifier` 即允许弹出播控面板；
  3. 将 `MediaObserver.sendCommand` 改为通过 `mediaremote-adapter.pl ... send <commandId>` 直接调用 `MRMediaRemoteSendCommand`；
  4. 修复 `IslandManager.isIslandVisibleDueToApps()`，当 `state.status != .stopped` 且 (`!state.title.isEmpty || state.isPlaying || !activeMediaApps.isEmpty`) 时立即显示灵动岛，并订阅 `$state` 与 `$activeMediaApps` 变化；
  5. 修复 `RecordClickOverlay` 的 `hitTest(_:)` 坐标系转换（`convert(point, from: superview)`）及 `activateMediaApp` 唤醒逻辑（结合 `unhide()`、AppleScript `activate` 与 `NSWorkspace.shared.openApplication`）；
  6. 清理 `.build/arm64-apple-macosx` 并更新 `build_app.sh` 指向 `.build/out/Products/Debug`。
