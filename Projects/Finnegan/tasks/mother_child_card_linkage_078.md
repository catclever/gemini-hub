---
id: mother_child_card_linkage_078
title: Implement Mother-Child Card Hover Linkage, Virtual Proxy Card, and Stack Deck
  Navigation
status: completed
priority: high
tags:
- frontend
- svelte
- interaction
- virtual-card
- jules
session: conversation://58c97e35-a614-4542-ad8d-16f08d35616c
---

## 需求描述
根据 `features/母子卡片的联动.md`（Wave 2 待第一波完成后触发）：
1. 散落态悬浮在母卡上时，当前屏幕中的所有子卡回正（rotation: 0），且连线动画持续展示。
2. 散落态悬浮在子卡上时，在屏幕右上方虚拟展示母卡（设计通用的虚拟卡片组件，负责展示不在当前屏幕的卡片微缩代理）。
3. 聚焦态进入母卡时，右侧虚拟卡位置列出所有的子卡（展示最上面一张，带堆叠效果且可切换）。
4. 聚焦态进入子卡时，虚拟卡位置展示母卡。

## 验收标准
- [ ] 悬浮与聚焦下的母子卡片双向联动与连线常亮。
- [ ] 通用虚拟代理卡（VirtualCardProxy）与堆叠卡（Stack Deck）流畅交互。
- [ ] 前端构建与测试通过。
