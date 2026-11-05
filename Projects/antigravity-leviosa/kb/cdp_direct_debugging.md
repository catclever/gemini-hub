---
description: 'Antigravity 本地直连 CDP (Chrome DevTools Protocol) 端口自动化排查与状态探测规范'
---

# Antigravity CDP 直连端口排查与自动化调试规范

## 1. 核心端口认知与动态探测铁律
在 macOS 环境下开发/调试 Antigravity TaiChi 注入脚本（`com.google.antigravity`）时：
- **`9224`**：Antigravity IDE 自身的常用内部调试端口（Title 包含 `Antigravity`）。
- **TaiChi 动态分配端口**：如果通过 TaiChi Gateway 启动，通常会被分配一个可用端口（如 `9222`, `9223`, `9225` 等）。
- **铁律**：**严禁在排查脚本中写死端口**，必须依赖动态探针进行探测自省。

### 自动化探针使用
在当前注入项目目录（`~/Library/Services/taichi/apps/com.google.antigravity/`）下已部署了专用探针 `debug_probe.js`：
```bash
# 1. 查看当前连接状态与所有激活窗口 Targets
node debug_probe.js

# 2. 自动化零人工执行 JS 巡检（读取实时 URL、标题或 DOM）
node debug_probe.js --eval "location.href"
node debug_probe.js --eval "document.title"
node debug_probe.js --eval "window.__taichi_injected"

# 3. 远程静默刷新目标应用窗口
node debug_probe.js --reload
```

---

## 2. 自动化排查与零人工复制 SOP
当排查注入效果、UI 按钮状态、主题切换或 DOM 结构时，**严禁反复要求用户手动打开控制台复制粘贴日志**。必须优先走以下全自动流程：

### 步骤 1：探测 Targets 获取 WebSocket 地址
直接运行 `node debug_probe.js`，探针会自动轮询 `9224`、`9222` 等端口，过滤并锁定目标 Antigravity 窗口。

### 步骤 2：CDP 远程执行与内存/DOM 巡检
利用 `node debug_probe.js --eval "<表达式>"`：
- **查看当前页面实际状态与注入标记**：
  ```bash
  node debug_probe.js --eval "(() => ({ url: window.location.href, title: document.title, injected: window.__taichi_injected }))()"
  ```
- **检查富文本编辑器 (Lexical) 或核心 DOM 节点**：
  结合 `dom-manipulation.md` 中的规范，可直接巡检编辑框内容：
  ```bash
  node debug_probe.js --eval "document.querySelector('[contenteditable=\"true\"]')?.innerText"
  ```

### 步骤 3：静默热重载测试
- 通过 `node debug_probe.js --reload` 远程刷新应用窗口以加载最新的 `web/` 脚本。
- 静默验证修改效果，无需用户干预。
