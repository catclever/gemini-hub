---
description: '第三方媒体播控、mr_target 崩溃、按键模拟与显隐死锁防坑记录'
---

# 媒体播控与多媒体架构防坑公墓 (Anti-Patterns)

## 1. 试图解决什么问题
在 macOS 上为第三方音乐播放器（如网易云音乐 `com.netease.163music`、QQ 音乐等）提供后台播控（播放/暂停/切歌）、前置唤起窗口，并在状态栏和灵动岛正确展现曲目与播控弹窗。

---

## 2. 失败的方案是什么

### 方案 A：使用编译好的 `mr_target` CLI 工具向指定 bundleId 派发播控命令
- **做法**：在 `MediaObserver.sendCommand` 中通过 `Process` 调用预编译的 `mr_target <bundleId> <commandId>` 二进制。
- **现象**：在现代 macOS 运行时中，`mr_target` 触发系统级内存段错误，进程以 `exit code 139 (SIGSEGV)` 瞬间崩溃退出，播控完全无响应。

### 方案 B：依赖 `simulateMediaKey` 模拟硬件多媒体键 (NX_KEYTYPE_PLAY)
- **做法**：通过 `NSEvent.otherEvent(with: .systemDefined)` 生成系统级多媒体按键事件（Play/Next/Prev），并调用 `cgDown.post(tap: .cgSessionEventTap)`。
- **现象**：
  1. 硬件多媒体键受 macOS 系统焦点调度机制严格限制，若网易云处于后台且近期未被选为活动播放源，按键事件会被系统直接丢弃或意外触发其他带有音频的网页/应用；
  2. 生成系统级事件若未正确绑定光标坐标，极易导致鼠标光标物理瞬跳至屏幕刘海区。

### 方案 C：仅使用 `tell application id ... to activate` 或 `runningApp.activate()` 唤醒应用
- **做法**：在用户要求唤醒播放器窗口时，仅执行 AppleScript 的 `activate` 命令或 AppKit 的 `NSRunningApplication.activate`。
- **现象**：对于通过 `Cmd+W` 关闭了主界面的第三方播放器（如网易云），这两个调用仅将菜单栏置顶，主播放窗口依然保持关闭，用户看到毫无反应。

### 方案 D：通过硬编码 `Bundle.module.resourcePath + "/MediaRemoteAdapter/..."` 加载资源
- **做法**：假设 SwiftPM 的 `Bundle.module.resourcePath` 始终是静态扁平路径。
- **现象**：Swift 6.3 调整了 Bundle 内部构建规范（生成了标准 App 嵌套资源目录 `Contents/Resources/Resources`），导致路径拼接找不到文件，底层的 `mediaremote-adapter.pl stream` 默默启动失败，应用彻底收不到任何播放更新。

### 方案 E：将灵动岛的窗口显隐严格绑定在 `activeMediaApps.isEmpty`
- **做法**：在 `IslandManager.isIslandVisibleDueToApps()` 中只根据 `!activeMediaApps.isEmpty` 判断是否显示。
- **现象**：由于功耗优化将 AppleScript 轮询拉长至 30s 且应用冷启动时不阻塞轮询，`activeMediaApps` 初始为空数组，导致灵动岛窗口 `alphaValue` 保持为 `0.0`，即便底层权威媒体流已经源源不断收到网易云的歌曲元数据，灵动岛在用户眼中依然完全“隐身”。

---

## 3. 为什么失败

1. **二进制架构与系统私有 API ABI 变迁**：`mr_target` 使用的硬编码私有符号绑定在较新 macOS 版本中存在内存结构不匹配，导致段错误；
2. **macOS 焦点黑盒机制**：硬件级按键事件（HID Tap）依赖 `NowPlaying` 注册实体的优先级抢占，无法指定 `targetBundleId`；
3. **AppKit 生命周期与 Reopen 事件缺位**：Mac 应用程序在所有窗口被关闭后，仅通过常规激活无法触发 `applicationShouldHandleReopen:hasVisibleWindows:`；
4. **Swift 编译输出与 SPM 资源封装规范升级**：Swift 6 采用了全新的资源打包与输出目录策略，硬编码相对路径极度脆弱；
5. **权威数据源（Push）与辅助轮询（Pull）时序倒挂**：用辅助低频拉取的数组去决策即时推送的 UI 显隐，造成了首屏状态死锁。

---

## 4. 绝对不要做什么

1. **绝对不要**使用已废弃崩溃的 `mr_target` 二进制，媒体播控统一走经过验证的 `mediaremote-adapter.pl <frameworkPath> send <commandId>` 通道；
2. **绝对不要**将 `simulateMediaKey` 作为第三方播放器的主要播控手段；
3. **绝对不要**仅凭单一 `activate` 命令唤醒媒体应用，必须附加 `NSWorkspace.openApplication` 派发 `kAEReopenApplication` 事件；
4. **绝对不要**假定 SwiftPM `Bundle.module` 的物理路径深度固定，必须采用基于 `FileManager.fileExists` 的自适应候选探测函数；
5. **绝对不要**让主界面或灵动岛的核心显隐依赖于低频降级的 AppleScript 辅助轮询列表；必须以权威的 `MediaRemote` 事件流为主导。
