---
id: fix_gateway_restart_freeze_and_async_button_state_016
title: 修复重启 9216 网关主线程卡死问题并增加重启中按钮状态防重
status: in_review
priority: high
tags:
- gateway
- concurrency
- ui
session: 02866a86-1e94-4132-aa50-d891547e4c67
---

# 修复重启 9216 网关主线程卡死问题并增加重启中按钮状态防重

## 任务目标与背景
1. 将 ServerManager.restart() 与 startWorker() 彻底移出 MainActor，异步化进程管理与启动监听，杜绝 semaphore.wait(5.0) 与 waitUntilExit() 阻塞主线程。
2. 修复 Node Worker 异常退出重试逻辑，增加防抖与指数退避，杜绝主线程无限循环自启雪崩。
3. 将 HSManager.initialize 中的 NSAppleScript 同步执行移至后台全局队列，防止 AppleEvent 阻塞。
4. ServerManager 暴露 @Published var isRestarting: Bool 状态（或 ObservableObject 发布），在 SettingsView 的重启网关按钮上增加重启中动画/状态展示，并在重启期间禁用按钮防止重复点击。
5. 消除 evaluateCyberScript 中的主线程死锁隐患。
参考知识库：kb/power_optimization_architecture.md

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
