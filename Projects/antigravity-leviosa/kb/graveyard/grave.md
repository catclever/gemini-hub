# 防坑公墓索引 (Negative Knowledge Base)

记录项目中排查过的死胡同、失败方案、反模式（Anti-Patterns）及排错教训：

- **[spa-css-variables-loss.md](./spa-css-variables-loss.md)**: SPA 路由切换时顶栏内联样式被重置导致自定义 CSS 变量丢失，需持久化校验与通用兜底锚点。
- **[kb-trigger-silent-crash-and-clipping.md](./kb-trigger-silent-crash-and-clipping.md)**: 知识注入面板一弹出即消失、内容透明且无报错的排查复盘：Strict Mode 未声明变量异常与 DOM overflow 剪裁。
- [DOM 注入兜底选择器泛匹配导致穿透至会话折叠框](dom_injection_loose_regex_and_scope_bleeding.md): 登录界面注入脚本因包含超宽正则 `/continue with google|google/i`，导致 Agent 执行带 google 关键词的工具调用时被误判并注入账号选择按钮。
- [强杀语言服务导致端口漂移与 Electron 跨域外链拦截死锁](electron_cross_port_navigation_and_ls_killing.md): 切换账号时通过 pkill 重启 Language Server 会导致端口漂移，前端 window.location.href 触发 Electron will-navigate 跨域拦截弹出系统浏览器，并导致客户端被钉死在已死旧端口。
