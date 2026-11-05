# AgentK 架构避坑指南：Monorepo 下的 Vite 热更新与幽灵依赖陷阱

**记录时间：** 2026年04月
**涉及模块：** Lerna/Yarn Workspaces, Vite (Dev Server), React-Moveable 交互层
**问题描述：** 在极度复杂的 Monorepo 环境中（如 `shoggoth` 作为主应用依赖 `@agent-k/tentacles` 等跨文件包），如果修改了子包的源码，Vite 能够监听到文件改动，但前端界面却出现**所有新逻辑均不生效，表现如物理锁死、代码根本没有运行**的灵异现象。

---

## 🐞 幽灵 BUG 还原发现过程

在重构 `@agent-k/tentacles` 插件以支持 Canvas 级坐标去耦合、旋转原点 `transformOrigin` 统一以及解除边框幽灵漂移的过程中，写出了一套极其完美的 `react-moveable` 事件代数剥离代码。但是，不论代码逻辑修得多么天衣无缝，在用户前台依然报“缩放、旋转完全失效”并且表现出极度反直觉的崩溃。

最终发现核心病因**完全不在代码逻辑中**，而在打包体系与热更新配置上。

## 🔍 问题根因剖析 (Root Cause)

1. **跨目录静态拉取**
`shoggoth` 使用 Vite 启动。当 Vite 导入 Node_Modules 里由 Monorepo 软链接过来的本地包 `@agent-k/tentacles` 时，它会默认寻找该子包 `package.json` 中的 `main` / `module` / `exports` 入口。
2. **`package.json` 的导出断层**
子包利用 `tsc && vite build` 编译了自己的发布库文件（通常输出到 `dist/tentacles.js`）。然而，`package.json` 中的导出路径因为曾经历过改名或者初始模板未更新，依然死死锁在类似 `"main": "./dist/hand.umd.cjs"` 这样的错误**遗留文件名**上。
3. **“幽灵”热更新灾难**
尽管你在 IDE 里正疯狂猛写 `TentaclesOverlay.tsx` 子包源码，并且终端可能会提示 HMR （热更新触发），但这会遇到无法跨越的壁垒：
   - 如果 Vite 解析时读取的是预打包好的 `.js` 文件，那么没重新跑子包的 `npm run build`，新源码就永远无法送达前端。
   - 更致命的是，由于导出设置错误或者之前遗留的重名旧产物，Vite dev server 实际上一直从缓存或者**老旧版本的编译废料**中拉取了一段“活着的木乃伊代码”。
   - 导致我们陷入长达一小时的错觉：以为自己的新架构触发了 Moveable 的极硬核级矩阵死锁，其实浏览器里运行的完全是改版前一小时最原始那套代码！

## 🚀 防治方案 & 最佳实践 (Best Practices)

### 1. 强同步 `package.json` 的出口名与构建名
在任何一个新建的原子包、组件库包中，必须严格校验 `vite.config.ts` 中的 `build.lib.fileName`（或rollup配置）与 `package.json` 的 `main/module/exports` 强一致：

```json
/* package.json 中必须精准匹配打包输出名 */
{
  "name": "@agent-k/tentacles",
  "main": "./dist/tentacles.umd.cjs",
  "module": "./dist/tentacles.js",
  "exports": {
    ".": {
      "import": "./dist/tentacles.js",
      "require": "./dist/tentacles.umd.cjs"
    }
  }
}
```

### 2. 双边联动开发流 (Monorepo Dev Flow)
当主项目严重依赖子包源码的交互式实时开发时，决不可只在主应用跑 `vite dev` 而放任子包冷落在一边。
必须：
*   要么给子包开启 `--watch` 热编译监听模式，实时将改动吐到 `dist` 里。
*   要么在主应用的 `vite.config.ts` 中的 `resolve.alias` 里做源码级越级强绑定，直接指向 `../libs/tentacles/src`。让主应用代理接管所有 TypeScript 的在线编译（适合轻量工具包，可跳过子包编译直达最新环境）。

### 3. 当现象极度反物理、反逻辑时，优先排查“幽灵加载”
如果你十分确信一个强制修改 DOM 样式的基本语句（如 `e.target.style.width = '100px'`）没有生效，那**一定不是你的 CSS 写得不够强，而是那句代码压根不存在于目前的运行时里**。请直接刷新浏览器或清理 `.vite/deps` 硬缓存再战！
