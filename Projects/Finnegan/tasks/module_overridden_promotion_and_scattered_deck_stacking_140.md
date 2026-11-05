---
id: module_overridden_promotion_and_scattered_deck_stacking_140
title: 模块可覆写收集机制与散落态母子卡物理层叠堆放
status: in_review
priority: high
tags:
- promotion
- module-override
- deck-stacking
- bugu
session: a7bf5827-3993-452d-b349-56f141101111
---

# 模块可覆写收集机制与散落态母子卡物理层叠堆放

## 任务目标与背景
实现模块可覆写收集机制与母子卡物理层叠堆放架构：
1. 后端与数据层：扩展 PromoteTempCard 支持传入 user_comment 和 echoOf，保存并在 ParseCardFile 中解析；
2. 模块覆写收集层：建立 PromotionOverrideRegistry，Bugu 模块覆写专属图标、提示词与附着母卡策略；
3. 前端交互层：在卡片右上角实现就地展开微输入条，Enter 提交附着收录（空 Enter 直接跳过），并提供微型独立收录按钮；
4. 空间与展示层：散落态下拥有 echo_of 的已收集子卡物理吸附在母卡正下方 (+5px 阴影与微倾斜层叠厚度，禁止散落态翻牌)，仅在聚焦态通过 VirtualCardProxy 解锁 < 1/N > 翻牌控制器与呈现公主批注。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

### 修正与确认（散落态与单屏容量隔离）
1. **布谷发现阶段（临时态）保持散落**：
   - 严格通过 `isTemporaryCard(card)` 识别临时卡（`isTemporary !== false && (origin === 'bugu' || ...)`）。
   - 未收集的临时卡（即使带有 `echoOf`）直接绕过物理层叠，继续执行 Mitchell 最佳候选空间散落算法，并在深度 `z: [20, 30]` 空间散落展示，同时由 `CosmicRayNetwork` 维持母子激光连线。
2. **收集机制（转正态）物理层叠**：
   - 只有通过布谷收集机制收集并转正的卡片（`isTemporary: false` 且持有有效 `echoOf` 且母卡在场），才会在散落态以微小偏移（`+5px x/y, +2.5 z, +1.2deg rot`）叠在母卡后方。
   - 叠层状态下的子卡与母卡之间自动抑制微距激光连线。
3. **单屏卡片数量容量隔离**：
   - 级联推挤 `applyCascade`、舞台补充 `replenishStageCandidates`、最大活跃卡片上限 `activeSolidCards` 以及视口溢出检测 `hasCardsBelow` 中，均已通过 `!isClusteredChildCard(c, cards)` 严格排除物理层叠子卡，确保叠放的子卡完全不占用单屏卡片配额（不计入一屏卡片数量）。
4. **测试验证**：
   - 前端 190 项单元测试全绿 (`npm test`)。
   - Vite 生产编译零报错 (`npm run build`)。
   - Go 后端单元测试通过 (`go test .`)。
