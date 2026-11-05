---
description: '知识注入面板一弹出即消失、内容透明且无报错的排查复盘：Strict Mode 未声明变量异常与 DOM overflow 剪裁'
---

# Post-Mortem: KB Trigger Dropdown Silent Crash & Clipping

## Context
在 Antigravity 客户端扩展 (`com.google.antigravity`) 中，`web/kb_trigger.js` 负责监听用户输入 `#cmd` / `#kb` 触发词，并从后端拉取全局及项目知识库条目，通过悬浮下拉菜单（Dropdown）供用户选择并注入至输入框。

## What Was Tried
1. **相对父容器定位 (`position: absolute; bottom: 100%`)**：试图将下拉菜单作为子节点挂载到输入框的父级 `.relative.w-full` 或 `inputElement.parentElement` 上，利用绝对定位向上弹出。
2. **重构渲染项样式时省略了变量声明**：在将 Tailwind 样式类重构为动态 inline style 时，直接对作用域变量 `badgeText` 进行赋值而未声明（如 `badgeText = 'Global';`）。
3. **强制项目名门禁**：在 `#cmd` 作用域由 `all` 细化为 `cmd-all` 时，设置了必须存在 `projName` 才能开启面板的拦截分支。

## Why It Failed
1. **父级容器裁切 (CSS Clipping)**：Antigravity / Gemini 新版前端对输入框外层卡片应用了 `overflow: hidden` / `overflow: clip`（用于包裹圆角边框）。当绝对定位的子元素被放置在 `bottom: 100%`（即父容器上方）时，整块菜单被 100% 裁切，导致 DOM 树虽然处于激活状态但视觉上完全不可见。
2. **ES Module 严格模式静默打断 (ReferenceError)**：
   - `kb_trigger.js` 使用 ES Module，默认在严格模式（`"use strict"`）下执行。
   - `renderRules` 循环在第一步执行了 `dropdownContainer.innerHTML = ''` 清空了 Loading 文案，紧接着在第一条数据的赋值处抛出 `ReferenceError: badgeText is not defined`。
   - 异常瞬间腰斩了后续所有 DOM 节点的生成，使得下拉菜单变成了一个高度为 0 的空白幽灵容器。
   - 与此同时，接口数据早已缓存入内存数组 `rulesData`，且 `isMenuVisible = true` 仍然生效，造成了“**一弹出 Loading 就瞬间消失、眼睛看不见、但键盘上下键能选中且能回车插入**”的极具迷惑性的假象。
3. **未识别项目名时静默关闭**：新开会话或非项目根路径下 `extractActiveProjectName()` 返回 `null`，导致常规命令直接被分支判定拦截，全局知识库也无法弹出。

## What NOT To Do
1. **绝对不要在富文本输入框容器内部使用 `position: absolute` 做浮层面板**：富文本外框为了圆角和滚动往往随时增加 `overflow: hidden`。所有悬浮层（下拉菜单、浮动工具栏）必须挂载在 `document.body` 并使用 `position: fixed`，通过 `getBoundingClientRect()` 映射视口绝对坐标。
2. **绝对不要在 ES Module 中书写任何隐式全局变量**：在 `"use strict"` 环境下，未带 `let`/`const` 的变量赋值直接触发运行时不可逆的中断。在发布前必须通过严格语法解析和 Node 模拟测试。
3. **不要在多源混合检索中设死单源门禁**：对于兼具 Global 与 Local 的复合命令（如 `#cmd`），即使 Local 上下文为空，也必须降级呈现 Global 结果，绝不能直接拦截关闭交互。
