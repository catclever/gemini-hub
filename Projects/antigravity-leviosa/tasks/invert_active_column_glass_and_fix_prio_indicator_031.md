---
id: invert_active_column_glass_and_fix_prio_indicator_031
title: Active栏位与卡片磨砂视觉反转并强化内联优先级指示器
status: completed
priority: medium
tags:
- ui
- kanban
- glassmorphism
- styling
session: 4282f618-0b6a-49c7-a16e-c9884bc4f2c4
---

# Active栏位与卡片磨砂视觉反转并强化内联优先级指示器

## 变更概述
1. 修复此前因 Tailwind JIT 类未预编译导致 border-l-[3.5px] 无法生效的问题，全面改用绝对内联样式确保卡片左侧优先级脊线与卡片 ID 胶囊内的发光圆点稳定渲染；2. 将 Active 栏位视觉层级反转：Active 栏位底托改为高透轻量设计，内部卡片升级为深度磨砂深色玻璃与悬浮发光，与 Backlog/Completed 两栏形成层次鲜明且舒适的焦点对比。

## 验证结论
- [x] 核心逻辑已实现并通过验证
