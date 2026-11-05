---
description: 'MusicFree 远端 API 的登录 Token 存储及使用说明'
---

# 远端登录 Token 说明 (Remote Login Token)

### 核心结论
- 远端服务（如 QQMusicApi / NeteaseCloudMusicApi 等）通常是无状态的，**不负责存储用户的登录凭证（Token/Cookie）**。
- 真正的 Token **完全保存在本地**。
- 在与远端通信获取状态（如“查询某首歌是否被喜欢”）时，必须由本地显式地将 Token 传递给远端接口，远端才能正确鉴权并返回状态。

### 如何获取 Token
- 用户维护的 Token 实际上保存在 MusicFree 本地环境的插件源码中。
- **存储位置**：在 `/Users/kael/Projects/musicfree/` 目录下的具体插件文件（如 `qq_pve.js` 和 `netease_pve.js`）里，常被定义为 `MY_COOKIE` 变量。
- **最佳实践**：编写注入脚本（如自定义 UI 面板）时，需要 Token 则应该直接以这些插件文件内的 `MY_COOKIE` 作为数据源 (Single Source of Truth) 提取，或者保持配置同步，避免自行瞎编或去远端寻觅。

### 如何带 Token 请求远端接口
此类基于 Node.js 的本地化远端 API（如 jsososo 和 Binaryify 的库）普遍通过手动传参的方式接收 Cookie，而不是依赖原生 HTTP Cookie 头：
- **GET 请求拼接**：必须显式提取 `MY_COOKIE` 字符串，通过 `URLSearchParams` 将其 URL-encode 后拼接到请求路径的 Query 参数中（例如 `?cookie=xxxxxx`）。
- **缓存击穿**：部分接口（如网易云）为了防止缓存导致状态不同步，还会要求在参数里追加 `timestamp` 等变量（如 `?cookie=xxx&timestamp=12345`）。
- **POST 请求**：如果是通过 POST 调用接口（如 `customFetch`），则一般在 body 里将 Cookie 以 JSON 格式传入（如 `{ cookie: MY_COOKIE }` 或是 `form-urlencoded`）。
