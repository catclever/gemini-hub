---
id: soften_ink_wash_to_slate_gray_and_slow_spin_3x_102
title: 水墨流光色调青灰软化与旋转周期放慢3倍
status: completed
priority: medium
tags:
- water-ink
- animation
- tuning
- optics
session: 58c97e35-a614-4542-ad8d-16f08d35616c
---

# 水墨流光色调青灰软化与旋转周期放慢3倍

## 变更概述
微调新卡片水墨动态光晕体验：
1. 颜色更灰更柔：告别纯焦黑（#000000），全面过渡为温润淡雅的松烟黛墨与石板青灰（主锋峰值调整为 slate-600/700 的 rgba(51, 65, 85, 0.88) 与 rgba(71, 85, 105, 0.88)，辅锋渐变至轻柔雾灰 rgba(148, 163, 184, 0.20)）；
2. 旋转周期放慢 3 倍：旋转动画周期从 3.8s 延展至 11.4s 悠扬慢旋，行笔舒缓沉静；
3. 同步将外围呼吸投影周期调整至 8s 柔和青灰漫射（ink-vip-breathe），与慢速流光完美呼应。

## 验证结论
- [x] 核心逻辑已实现并通过验证
