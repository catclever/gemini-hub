# MusicFree Project Ironclad Rules (项目铁律)

## [Global]
- **Target Application Architecture**: MusicFree Electron 客户端配合 TaiChi 注入服务。注入入口为 `web/main.js`。
- **Port Distinction & Mapping (动态探测与严格区分)**:
  - **动态自省铁律（严禁写死端口）**：排查端口**绝不能硬编码写死**！必须通过 `lsof -n -P -iTCP -sTCP:LISTEN | grep MusicFree` 动态提取 MusicFree 进程占用的端口，并通过 `http://127.0.0.1:<port>/json` 探测包含 `title: MusicFree` 的 target 动态锁定当前活动 CDP 端口（当前默认通常为 `9222`）。
  - **`9224`**：**Antigravity IDE 自身的内部调试端口**。若探测到标题为 `Antigravity`，必须立即排除，严禁连接该端口排查 MusicFree。

## [Main Agent]
- **Zero-Copy Autonomous CDP Debugging Mandate (零人工复制直连调试铁律)**:
  - 当需要排查 MusicFree UI 状态、按钮异常（如“未知歌单”）、网络报错或 React 运行时属性时，**严禁反复要求用户手动打开控制台复制粘贴日志**。
  - 主 Agent 必须优先通过上述动态探针获取活动的 CDP WebSocket 地址，使用 `Runtime.evaluate` 直接在 live 内存中巡检 React Fiber 树与路由状态，实现全自动诊断与静默验证。
- **React Fiber 业务属性索引准则**:
  - MusicFree 歌单详情页将歌单业务数据挂载在头部组件（`.music-sheet-header__title` 或 `h1`）的 Fiber 树上，属性名为 **`memoizedProps.musicSheet`**。
  - 专辑详情页属性名为 **`memoizedProps.album`** 或 **`memoizedProps.albumItem`**。
  - 严禁仅依赖 `props.sheetItem` 或 `props.playlist` 进行单点检索。
- **Hash 路由解析准则**:
  - MusicFree 的路由格式为 `#/musicsheet/<platform>/<id>` 以及 `#/album/<platform>/<id>`，严禁使用 `/sheet/` 进行子串匹配。

## [Dev Agent]
- **源码写入边界**: 所有前端注入脚本逻辑必须严格维护在工作区的 `web/` 目录下。
- **防污染作用域约束**: 严禁从全局容器（如 `main`, `body`）向下做无限制的泛 DOM 扫描，防止意外抓取到右侧/底部“当前播放队列”抽屉中的后台临时歌曲数据。所有 Fiber 爬取必须严格绑定在当前视图的 Header / Title 或 Toolbar 上。

## [Ops Agent]
- **CDP 脚本执行环境**: 执行基于 WebSocket 的 CDP 探针脚本时，使用 Node.js 配合 `/tmp/cdp_tool/node_modules/ws`，并指定 `BypassSandbox: true` 保证本地环回网络连通性。
