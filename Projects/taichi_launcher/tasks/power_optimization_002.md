---
title: Taichi 二次高功耗深度优化 (音频保活、全局鼠标监听、全量窗口过滤、条件渲染)
status: completed
priority: critical
tags:
- power-optimization
- audio-engine
- ipc
- gpu-rendering
- hammerspoon
session: conversation://5be557f6-45a3-46ef-b995-7681379ee97a
id: power_optimization_002
---
# Taichi 二次深度高功耗优化记录

## 1. 问题背景
尽管一期优化了媒体轮询与部分动画 Timer，Taichi 在特定场景下依然出现在系统高功耗列表中。经二次深度排查，定位了四大隐形杀手：
1. **音频保活引擎锁死硬件**：`AVAudioEngine` 持续输出静音，阻止 Mac CoreAudio 及外接蓝牙耳机休眠。
2. **灾难性全局鼠标监听**：`NSEvent.addGlobalMonitorForEvents(matching: .mouseMoved)` 拦截全局鼠标像素级移动，每秒唤醒 CPU 几百次。
3. **沉重的全局焦点监听**：Hammerspoon 使用 `hs.window.filter.new(nil)` 跨进程追踪全系统的应用和窗口切换，且 Swift 后端并未实际消费该事件。
4. **GPU 后台模糊渲染**：`FluidCoreView` 能量球大半径高斯模糊在不可见时未从渲染树彻底剥离。

## 2. 彻底重构与铲除方案
- **`AudioKeepAliveManager` 状态绑定**：加入 `isPlaying` 判断，音乐暂停立即停止 `AVAudioEngine`。
- **废弃全局 `.mouseMoved`**：删除了所有 `NSEvent.addGlobalMonitorForEvents` 监听逻辑，替换为 SwiftUI 零成本的 `.onHover` 修饰符，实现原生的区域触碰感知。
- **剔除无用 Hammerspoon IPC**：删除了 `event_watcher.lua` 中的 `windowFocused` 监听区块，切断了系统级的 Accessibility 辅助功能轰炸。
- **条件渲染 (Conditional Rendering)**：在调用 `FluidCoreView(isVisible:)` 处，严格使用 `if isVisible` 将视图从 SwiftUI 节点树中剔除，切断隐性 GPU 渲染管线。

## 3. 验证与发布
- 代码修改完毕后，通过 `swift build` 及 `./build_app.sh` 编译打包生成最新版 `TaiChi.app`，相关耗电监控数据恢复正常基准线。
