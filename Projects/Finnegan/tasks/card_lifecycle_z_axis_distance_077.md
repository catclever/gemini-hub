---
id: card_lifecycle_z_axis_distance_077
title: Link Card Temporal Lifecycle and TTL to Z-Axis Depth and Multi-Screen Cascading
status: completed
priority: high
tags:
- frontend
- algorithm
- stage
- decay
- jules
session: conversation://58c97e35-a614-4542-ad8d-16f08d35616c
---

## 需求描述
根据 `features/卡片生命周期联动z轴距离.md`：
1. 常态卡片（非搜索激活）：创建时间越早离得越远，为不同时间范围（今日、近3天、近1周、更早）设定清晰的 z 轴梯度。
2. 临时卡片：按照消失的剩余时间决定距离（剩余寿命越短，z 轴越深，向深空沉退）。
3. 搜索命中卡片：最高 z 轴优先级（前景 z 极小），但单屏配额有限（如 4~6 张），超出配额的自动级联推至下一屏。
4. 用户新创建卡片：最高 z 轴高度（与优先级第一梯队一致）。
5. 新卡片入场：优先挤占当前屏幕中 z 轴位置最远的卡片。
6. 被挤出卡片：若 z 轴位置低于阈值（如 z >= 85 或生命周期将尽）则直接淡出消失（isFadingOut: true），否则推向下一屏幕并触发连锁位移逻辑（applyCascade 递归）。

## 改造范围
- `frontend/src/lib/stageCoords.ts` & `frontend/src/lib/stageDecay.ts`。

## 验收标准
- [ ] Z 轴计算与时间、寿命、搜索状态严格映射。
- [ ] 连锁逐出与屏幕配额逻辑正确生效。
- [ ] 单元测试通过，编译无报错。
