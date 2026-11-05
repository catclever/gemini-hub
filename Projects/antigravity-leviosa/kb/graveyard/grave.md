# 防坑公墓索引 (Negative Knowledge Base)

记录项目中排查过的死胡同、失败方案、反模式（Anti-Patterns）及排错教训：

- **[spa-css-variables-loss.md](./spa-css-variables-loss.md)**: SPA 路由切换时顶栏内联样式被重置导致自定义 CSS 变量丢失，需持久化校验与通用兜底锚点。
- **[kb-trigger-silent-crash-and-clipping.md](./kb-trigger-silent-crash-and-clipping.md)**: 知识注入面板一弹出即消失、内容透明且无报错的排查复盘：Strict Mode 未声明变量异常与 DOM overflow 剪裁。
