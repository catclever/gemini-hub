---
id: scattered_card_option_click_edit_088
title: 散落态卡片支持 Option+单击 快捷编辑
status: completed
priority: medium
tags:
- frontend
- interaction
- shortcut
- editor
session: conversation://23d9961a-73cc-490d-9a09-b0c7743584e9
---

# 散落态卡片支持 Option+单击 快捷编辑

## 变更概述
在散落态（非聚焦态）下，支持按住 Option 键（altKey）单击卡片直接在外部编辑器中打开该卡片进行编辑，不进入聚焦动画，提升快速编辑流体验。

## 验证结论
- [x] 核心逻辑已实现并通过验证

## 变更概述
在 `frontend/src/UICard.svelte` 中增强了卡片的点击交互：
1. **Option (⌥) + 单击快捷编辑**：
   - 在卡片的 `handleClick` 事件处理中检测 `e.altKey`；
   - 若用户按住 Option (⌥) 单击散落态卡片，则阻止默认动作并直接调用 `triggerOpenEditor()`（通过优先 qled://、回退系统默认调起外部编辑器）；
   - 不会触发 `onToggleFocus()` 进入聚焦放大动画，实现秒级快速呼出外部编辑器。
2. **交互提示优化**：
   - 在未聚焦卡片根元素上增加悬停提示：`title="⌥ + 单击在外部编辑"`，与聚焦态的 `双击进行编辑` 形成完整的交互辅助反馈。

## 验证结论
- [x] 前端 TypeScript / Svelte 诊断检查通过：`npm run check` 0 errors, 0 warnings
- [x] 事件逻辑无侵入性，常规单击仍然平滑触发聚焦态过渡，双击仍保持聚焦态编辑。
