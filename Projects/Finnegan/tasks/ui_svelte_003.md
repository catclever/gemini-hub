---
title: Implement Finnegan Svelte UI (Scattering & Focus States)
status: completed
priority: high
tags:
- frontend
- svelte
- css
- ui
- wails
id: ui_svelte_003
---
# 构建 Finnegan 前端界面 (精装修)

**目标**:
在 `frontend/src` 中使用 Svelte 实现 Finnegan 的核心意识流界面，并配置 Wails 原生窗口为高透毛玻璃效果。

**核心规范 (遵循设计文档)**:
1. **透明毛玻璃窗口**: 修改 `main.go` 和 `wails.json`，开启 macOS 的原生透明支持 (`Mac.WindowIsTranslucent: true`, 且清除 CSS 背景颜色)，使应用呈现无边框且带背景壁纸透视的效果。
2. **散落态 (Scattering State)**: 
   - 界面无侧边栏。中心存在一个全局的输入框 (Omnibar)。
   - 渲染一组测试用的卡片，使用随机的旋转角度 (`-30deg` 到 `+30deg`) 和绝对定位/Flex 布局散布在屏幕上。
   - 层级较低的卡片具有一定的透明度和置灰效果 (Z 轴景深)。
3. **聚焦态 (Focus State)**:
   - 点击某张卡片时，使用 Svelte 的 `spring` 或 `tweened` 动画，将该卡片平滑移动至屏幕正中央。
   - 旋转角度归零 (`0deg`)，透明度恢复 100%，背景纯白，放大显示。
   - 其他所有未选中的卡片大幅度降低透明度并开启 CSS 模糊 (`filter: blur(10px)`)，在背景中退隐。

**输出要求**:
请将代码写入带有 `_ui_svelte_003` 后缀的草稿文件中 (如 `App_ui_svelte_003.svelte`、`main_ui_svelte_003.go`)。
完成后修改本任务状态为 `ready_for_review`。
