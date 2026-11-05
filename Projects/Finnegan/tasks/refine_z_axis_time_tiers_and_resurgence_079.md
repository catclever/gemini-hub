---
id: refine_z_axis_time_tiers_and_resurgence_079
title: Refine Z-Axis Age Tiers up to 1 Year and Implement Distant Memory Resurgence
  Echo
status: completed
priority: medium
tags:
- frontend
- stage
- z-axis
- algorithm
session: conversation://58c97e35-a614-4542-ad8d-16f08d35616c
---

## 变更概述
根据公主的建议，对 `frontend/src/lib/stageCoords.ts` 中的常态卡片 Z 轴时间沉淀公式进行了细腻分级并加入了“回光返照（Resurgence Echo）”机制：
1. **细化分档梯度**：
   - 今日内（0~24h）：`z: 15 ~ 27`（活跃前景）
   - 近 3 天（1~3d）：`z: 27 ~ 39`（短期记忆）
   - 近 1 周（3~7d）：`z: 39 ~ 52`（近期关注）
   - 近 1 个月（7~30d）：`z: 52 ~ 65`（中期沉淀）
   - 近 3 个月（30~90d）：`z: 65 ~ 77`（远期记忆）
   - 3 个月 ~ 1 年（90~365d）：`z: 77 ~ 88`（深空沉睡）
2. **回光返照机制（> 1 年）**：
   - 超过 1 年的远古记忆卡片触发回光返照，不再深坠于暗处，而是跃升至贴近“近 1 周”的景深层（`z: 45 ~ 55`），在潜意识与回忆边缘重新浮现。

## 验证结论
- [x] TypeScript 类型检查与 svelte-check 校验通过（0 报错）。
- [x] Vite 打包构建成功。
- [x] 变更已同步 PVE 并推送到 GitHub main 分支 (`2b586a8`)。
