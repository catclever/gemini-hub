---
title: 强杀语言服务导致端口漂移与 Electron 跨域外链拦截死锁
description: 切换账号时通过 pkill 重启 Language Server 会导致端口漂移，前端 window.location.href 触发 Electron
  will-navigate 跨域拦截弹出系统浏览器，并导致客户端被钉死在已死旧端口。
date: '2026-11-07'
---

# Post-Mortem: 强杀语言服务导致端口漂移与 Electron 跨域外链拦截死锁

## 问题现象
在 Antigravity 客户端切换账号时，系统会自动在 macOS 默认浏览器（Chrome / Safari）中弹出一个 `https://127.0.0.1:<port>/` 的网页，而 Antigravity 客户端窗口却与 Language Server 断开连接，页面变白或断联，刷新页面也报 `ERR_CONNECTION_REFUSED`，必须彻底退出并重新打开客户端才能恢复。

## 根本原因
1. **反模式：通过外部 `pkill` 强行击杀本地宿主服务**：
   旧设计在切换账号更新 Token 档案后，调用 `pkill -TERM language_server` 依赖 Electron 的 `monitorLsCrashInternal` 兜底拉起新服务。但：
   - 官方分配端口为 `DYNAMIC_PORT = 0`，每次重启分配到的端口必然改变（例如从 51234 变成 54321）；
   - Electron 对崩溃重启设计了 2 秒强制冷却（`RESTART_COOLDOWN_MS = 2000`），并在 60 秒内超过 3 次直接放弃重启（`Giving up`）；
2. **Electron 导航守卫跨端口同源误判**：
   前端注入脚本轮询检测到新端口后，调用了 `window.location.href = st.url`。然而 Electron 主进程在 `dist/utils.js` 中注册了 `will-navigate` 守卫：
   ```javascript
   const guardExternalNavigation = (event) => {
       if (!event.isMainFrame) return;
       if (isSameOrigin(event.url, hubContents.getURL())) return;
       event.preventDefault(); // 掐死客户端内部跳转！
       void openExternalSafely(event.url, 'unconfirmed'); // 调用系统默认浏览器打开！
   };
   ```
   在浏览器 URL 规范中，**端口不同即属于不同源（Cross-Origin）**。Electron 判定其为“未经授权的外部恶意跳转”，强行 `event.preventDefault()` 取消了客户端跳转，并唤起外部浏览器；
3. **断联死锁**：
   客户端窗口被强行留在旧端口上，而旧端口的语言服务已被杀死，导致客户端断开连接且无论怎么刷新都因旧端口关闭而无法自愈。

## 防御措施与规范
1. **优先利用宿主服务原生具备的原地热更新机制**：
   Antigravity Language Server 底层 Go 服务的 `authclient` 原生具备磁盘 Token 变动感知能力（`syncWithStoredToken` / `hasStoredMetadataChanged` / `storedTokenSyncKey`）。更新 Token 档案后**严禁杀死进程**，保持原服务进程与 HTTPS 端口不变；
2. **严禁在 Electron 渲染进程中发起跨端口 `window.location.href`**：
   渲染进程发起的任何跨端口跳转都会被 Electron 原生安全策略判定为外链并丢给系统浏览器。在同端口下使用 `window.location.reload()` 属于 100% 同源刷新，安全无拦截；
3. **若必须处理端口漂移，必须由主进程接管或通过 CDP 导航**：
   Electron 主进程的 `onPortChanged` 会通过 `win.loadURL(newUrl)` 统一重新加载，不走渲染进程 `will-navigate` 拦截；或者通过 CDP 发送 `Page.navigate`，严禁在页面 JS 中直接更改 `href`。
