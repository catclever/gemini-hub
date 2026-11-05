---
name: add-app
description: 快速为指定应用建立 TaiChi Cyber 注入脚手架，包含 CDP 通信 Worker、Web 注入入口、自动化 CDP 调试探针及开发知识规范。
---

# 目的
自动化创建 TaiChi Cyber 模式下的第三方应用注入工程，赋予其完整的 CDP 注入闭环、零人工复制自动化排查探针（Zero-Copy Probe）及配套的项目知识库。

# 执行步骤

当用户触发此命令 `/add-app [应用名称或Bundle ID]` 时，请严格按照以下步骤执行：

1. **确定 Bundle ID 与应用名称**：
   - 若用户输入的是普通应用名（例如 `eagle`），使用 `osascript -e 'id of app "eagle"'` 获取真实 Bundle ID（如 `tw.ogdesign.eagle`）。
   - 若用户输入的是 Bundle ID，可通过其反推常规应用名（如 `tw.ogdesign.eagle` -> `Eagle`）。
   - 提取应用显示名（如 `appName = "Eagle"`, `bundleId = "tw.ogdesign.eagle"`）。

2. **建立基础目录**：
   - 目标根目录为：`~/Library/Services/taichi/apps/<Bundle_ID>`
   - 执行创建目录：`mkdir -p ~/Library/Services/taichi/apps/<Bundle_ID>/{web,worker}`

3. **生成 CDP 通信与注入服务 (`worker/index.js`)**：
   - 在 `~/Library/Services/taichi/apps/<Bundle_ID>/worker/index.js` 写入标准注入逻辑：
   ```javascript
   module.exports = async function(query) {
       const port = query.port;
       if (!port) {
           return { success: false, error: "Missing port parameter" };
       }

       const appId = "<Bundle_ID>";
       const entryUrl = `http://127.0.0.1:9216/src/apps/${appId}/web/main.js`;

       const fs = require('fs');
       const logFile = '/tmp/taichi_worker.log';
       const log = (msg) => fs.appendFileSync(logFile, `[${new Date().toISOString()}] ${msg}\n`);
       
       log(`Starting injection for app ${appId} on port ${port}...`);

       try {
           log(`Fetching targets from http://127.0.0.1:${port}/json/list...`);
           const injectedTargets = new Set();
           const maxTime = Date.now() + 15000;

           const expression = `
               (function() {
                   if (window.__taichi_injected) return;
                   window.__taichi_injected = true;
                   console.log("[TaiChi] Injection script active on " + window.location.href);
                   
                   const loadMod = () => {
                       import('${entryUrl}')
                           .then(() => console.log("[TaiChi] Import successful! Mod should be active."))
                           .catch(e => console.error("[TaiChi] Import Error:", e));
                   };

                   const startMod = () => {
                       setTimeout(loadMod, 1500);
                   };

                   if (document.readyState === 'complete' || document.readyState === 'interactive') {
                       startMod();
                   } else {
                       window.addEventListener('load', startMod);
                   }
               })();
           `;

           const injectIntoTarget = (target) => {
               return new Promise((resolve) => {
                   const ws = new WebSocket(target.webSocketDebuggerUrl);
                   let timeoutId = setTimeout(() => {
                       ws.close();
                       resolve();
                   }, 5000);

                   ws.onopen = () => {
                       ws.send(JSON.stringify({ id: 1, method: "Page.enable" }));
                   };

                   ws.onmessage = (event) => {
                       const res = JSON.parse(event.data);
                       if (res.id === 1) {
                           ws.send(JSON.stringify({
                               id: 2,
                               method: "Page.addScriptToEvaluateOnNewDocument",
                               params: { source: expression }
                           }));
                       } else if (res.id === 2) {
                           ws.send(JSON.stringify({
                               id: 3,
                               method: "Runtime.evaluate",
                               params: { expression: expression }
                           }));
                       } else if (res.id === 3) {
                           log(`Injection successful for target ${target.id}!`);
                           clearTimeout(timeoutId);
                           resolve();
                       }
                   };

                   ws.onerror = () => {
                       clearTimeout(timeoutId);
                       resolve();
                   };
               });
           };

           while (Date.now() < maxTime) {
               try {
                   const response = await fetch(`http://127.0.0.1:${port}/json/list`);
                   const targets = await response.json();
                   
                   for (const t of targets) {
                       if (t.type === 'page' && !t.url.includes('devtools://') && !t.url.startsWith('data:')) {
                           if (!injectedTargets.has(t.id)) {
                               injectedTargets.add(t.id);
                               log(`Discovered new target: ${t.id} - ${t.url}`);
                               injectIntoTarget(t);
                           }
                       }
                   }
               } catch (e) {}
               await new Promise(r => setTimeout(r, 1000));
           }

           if (injectedTargets.size === 0) {
               return { success: false, error: "No suitable page target found for CDP injection." };
           }

           return { success: true, message: `Injected into ${injectedTargets.size} targets.` };
       } catch (e) {
           return { success: false, error: e.message };
       }
   };
   ```

4. **生成前端注入主入口 (`web/main.js`)**：
   - 在 `~/Library/Services/taichi/apps/<Bundle_ID>/web/main.js` 中写入初始化脚本与注入反馈浮标：
   ```javascript
   // main.js - Entry point for <AppName> Mod
   console.log('🚀 [TaiChi <AppName> Mod] 注入脚本已激活');

   if (window === window.top) {
       function showBadge() {
           if (!document.body) {
               setTimeout(showBadge, 100);
               return;
           }
           const badge = document.createElement('div');
           badge.textContent = '✅ TaiChi (<AppName> Mod) Injected!';
           badge.style.cssText = 'position: fixed; bottom: 20px; right: 20px; background: #2BA0FA; color: white; padding: 8px 14px; border-radius: 8px; font-weight: bold; font-size: 13px; z-index: 999999; box-shadow: 0 4px 12px rgba(0,0,0,0.25); pointer-events: none; transition: opacity 0.5s;';
           document.body.appendChild(badge);
           
           setTimeout(() => {
               badge.style.opacity = '0';
               setTimeout(() => badge.remove(), 500);
           }, 4000);
       }
       showBadge();

       // 在此处初始化业务增强逻辑
   }
   ```

5. **赋予零人工复制自动化 CDP 探针 (`debug_probe.js`)**：
   - 读取模板 `~/Library/Services/taichi/templates/cdp_probe.js`。
   - 将 `{{APP_NAME}}` 替换为 `<AppName>`，将 `{{BUNDLE_ID}}` 替换为 `<Bundle_ID>`。
   - 写入到应用目录：`~/Library/Services/taichi/apps/<Bundle_ID>/debug_probe.js`。
   - 赋予执行权限：`chmod +x ~/Library/Services/taichi/apps/<Bundle_ID>/debug_probe.js`。

6. **生成项目管理知识库与指南**：
   - 在应用目录下生成 `README.md`，重点标注如何使用该探针进行零人工控制台调试：
   ```markdown
   # <AppName> (Bundle ID: `<Bundle_ID>`) 注入与调试指南

   ## 目录结构
   - `web/` : 前端 DOM 与业务逻辑脚本（主入口 `web/main.js`）。
   - `worker/` : TaiChi Gateway 调度的 CDP 自动注入服务（入口 `worker/index.js`）。
   - `debug_probe.js` : 自动化零人工排查探针工具。

   ## 自动化 CDP 调试（零人工复制）
   无需手动打开控制台，在终端直接运行：
   - **查看连接状态与所有窗口 Targets**：
     `node debug_probe.js`
   - **远程静默执行 JS 巡检（读取实时 URL、标题或组件数据）**：
     `node debug_probe.js --eval "location.href"`
     `node debug_probe.js --eval "document.title"`
   - **远程静默刷新目标应用窗口**：
     `node debug_probe.js --reload`
   ```

7. **完成汇报**：
   - 向用户展示初始化完成清单，包括已生成的目录、通信 worker、注入入口、以及如何使用 `node debug_probe.js` 快速开始排查。
