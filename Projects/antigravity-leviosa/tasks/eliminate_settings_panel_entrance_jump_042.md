---
id: eliminate_settings_panel_entrance_jump_042
title: 根除设置面板入场小跳跃与坐标二次瞬移
status: completed
priority: high
tags: []
session: fba8eb14-e6fb-4b79-a186-9eb1a0f0fda6
---

# 根除设置面板入场小跳跃与坐标二次瞬移

## 变更概述
深入定位设置面板呼出时出现小跳跃的物理根因：入场动画期间zoom/scale导致左上角坐标动态位移，且多重setTimeout延时重算引发坐标跳跃。通过引入几何中心不变性数学推导(Invariant Center Math)在首帧直接精确锁定静止态坐标，并在CSS中阻断弹窗摇晃动画与坐标过度，移除多阶段延时触发，彻底实现零延迟、零跳跃的如丝般顺滑定格呈现。

## 验证结论
- [x] 核心逻辑已实现并通过验证
