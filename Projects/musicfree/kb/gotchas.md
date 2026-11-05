# 注入避坑指南 (Gotchas)

## TaiChi 动态注入 (ES Module) 的缓存与异常问题

1. **强缓存陷阱**: 
   - 依赖 `import(url)` 动态加载模块时，由于底层 Chromium 的 Module Cache 机制，单纯修改本地 JS 文件后刷新网页（即使是 Cmd+R），经常无法读取到最新代码。
   - **错误做法**: 在 `import('${entryUrl}?t=' + Date.now())` 里加 query string。TaiChi 的简易静态服务器可能无法正确处理 query string，这会导致返回 404 HTML 页面。而 HTML 页面开头为 `<`，进而会引发注入脚本侧报出 `SyntaxError: Invalid or unexpected token`。
   - **正确做法**: 最好使用 DevTools 的 `Disable cache` 或者完全重启客户端来清理缓存，避免去魔改注入器的请求路径。

2. **透明背景注入尝试失败**:
   - 尝试通过动态插入 `<style>`，将 `data-window="main"` 下所有元素的背景置为 `transparent` 配合 `backdrop-filter: blur`，以期实现毛玻璃透视效果。
   - 结果：不仅在不修改主进程 `transparent: true` 配置的情况下无法透视桌面，在部分环境下还可能因为字符编码或模块解析引发未知 `SyntaxError` 导致整个入口脚本崩溃。
   - **结论**: 在完全确定底层窗口状态并掌握完整调试日志前，不要贸然向正在稳定运行的主入口动态加载复杂样式的外部模块文件。
