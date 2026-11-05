---
id: temp_card_focus_bg_075
title: Temporary Card Focus Mode Translucent Background Polish
status: completed
priority: medium
tags:
- frontend
- svelte
- ui
- jules
session: conversation://58c97e35-a614-4542-ad8d-16f08d35616c
---

## 需求描述
根据 `features/临时卡片的聚焦态背景色.md`：
- 和散落态的背景色一致，并且可以更透明，体现它是临时卡片。
- 在 `frontend/src/UICard.svelte` 中优化 `.card.temporary.focused` 样式。
- 继承散落态冷调雾蓝渐变色相 `linear-gradient(135deg, rgba(226, 236, 248, 0.58) 0%, rgba(210, 222, 238, 0.42) 100%)`，并保持通透毛玻璃感，避免原先近乎不透明高亮白灰（0.96）的生硬感。

## 验收标准
- [ ] 临时卡片在聚焦态下拥有与散落态一致的雾蓝冷调半透明渐变。
- [ ] 文字保持高易读性，backdrop-filter 模糊柔和。
- [ ] 前端编译通过（`npm run check` & `npm run build`）。
