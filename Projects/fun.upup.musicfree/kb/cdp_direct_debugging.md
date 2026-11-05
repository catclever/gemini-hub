---
description: 'MusicFree 本地直连 CDP (Chrome DevTools Protocol) 端口自动化排查与 React 状态探测规范'
---

# MusicFree CDP 直连端口排查与自动化调试规范

## 1. 核心端口认知与动态探测铁律
在 macOS 环境下开发/调试 MusicFree TaiChi 注入脚本时，存在多个 Electron/Chromium 调试端口，**严禁混淆，更严禁在排查脚本中写死端口**：
- **`9224`**：Antigravity IDE 自身的内部调试端口（Title 包含 `Antigravity`）。**必须排除**。
- **MusicFree 真实 CDP 端口**：虽然当前默认是 `9222`，但可能随用户启动参数改变。**必须动态自省探测**。

### 动态端口探测探针（Dynamic Probe）
在建立 CDP 连接前，必须通过以下探针动态锁定可用端口：
```python
import urllib.request, json, subprocess

ports = subprocess.check_output("lsof -n -P -iTCP -sTCP:LISTEN | grep MusicFree | awk '{print $9}' | cut -d: -f2", shell=True).decode().split()
cdp_port = None
for p in set(ports):
    try:
        url = f'http://127.0.0.1:{p}/json'
        with urllib.request.urlopen(url, timeout=0.5) as res:
            data = json.loads(res.read())
            if any('MusicFree' in t.get('title', '') for t in data):
                cdp_port = p
                break
    except Exception:
        continue
# 动态返回真实 cdp_port (如 9222)
```

---

## 2. 自动化排查与零人工复制 SOP
当用户反馈“按钮状态不对”、“未知歌单”或“无法获取数据”时，**严禁反复要求用户手动打开控制台复制粘贴日志**。必须优先走以下全自动流程：

### 步骤 1：探测 Targets 获取 WebSocket 地址
请求 `http://127.0.0.1:9222/json`，筛选 `type === 'page'` 且 `title.includes('MusicFree')` 的 target，提取 `webSocketDebuggerUrl`。

### 步骤 2：CDP 远程执行与 React 内存巡检
通过 Node.js (`ws` 模块) 连接该 WebSocket，使用 `Runtime.evaluate` 注入轻量巡检脚本：
- **查看当前页面实际 Hash 与按钮文本**：
  ```javascript
  (() => ({
      url: window.location.href,
      hash: window.location.hash,
      btn: document.querySelector('.xiaoan-subscribe-btn')?.innerText
  }))()
  ```
- **直接读取 React Fiber 树上的业务对象**：
  不要仅看 DOM，直接爬取组件 Fiber 节点的 `memoizedProps`。

### 步骤 3：静默热重载与路由测试
- 通过 `Page.reload` 远程刷新应用页面以加载最新的 `custom_panel.js`。
- 通过修改 `window.location.hash = ...` 驱动应用切换至目标测试歌单/专辑，静默验证修复结果。

---

## 3. MusicFree React 组件树与路由关键事实
通过 live CDP 探测沉淀的核心知识：

1. **歌单/专辑关键 Props 挂载点**：
   - 歌单详情页：数据挂载在头部组件（`.music-sheet-header__title` 或 `h1`）的 Fiber 树上，键名为 **`props.musicSheet`**（包含 `id`, `title`, `platform`, `artwork` 等）。
   - 专辑详情页：数据挂载在头部组件的 Fiber 树上，键名为 **`props.album`** 或 **`props.albumItem`**。
   - **绝对注意**：不要仅检索通用的 `props.sheetItem` 或 `props.playlist`，MusicFree 详情页原生使用的是 `musicSheet`。

2. **真实 Hash 路由格式**：
   - 歌单：`#/musicsheet/<platform>/<id>`（例如 `#/musicsheet/NeteasePVE/581589631`）。
   - 专辑：`#/album/<platform>/<id>`。
   - 本地收藏：`#/local-sheet/favorite`。
   - **注意**：正则匹配必须包含 `musicsheet`，不能写成 `/sheet/`。

3. **抽屉/播放队列陷阱**：
   - 右侧或底部的“当前播放队列”抽屉只包含纯歌曲数组，**不包含歌单 ID**。若在此容器中粗暴向下全局检索，极易误抓当前播放歌曲或背景歌单信息。
   - 必须优先从当前页面的 Header / Title 向上或向下精确定位，严禁全局盲目 querySelector。
