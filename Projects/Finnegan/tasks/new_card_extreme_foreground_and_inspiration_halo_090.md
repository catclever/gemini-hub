---
id: new_card_extreme_foreground_and_inspiration_halo_090
title: 新录入卡片极前置深度、中心就近投放与30分钟独享灵感呼吸微光
status: completed
priority: high
tags:
- stage
- depth
- animation
- inspiration
- optics
session: 58c97e35-a614-4542-ad8d-16f08d35616c
---

# 新录入卡片极前置深度、中心就近投放与30分钟独享灵感呼吸微光

## 变更概述
实现手动新创建卡片（Thought、ChatLog、Note）的黄金捕获三要素：
1. 极前置物理景深：z: 1.5 ~ 5.0（translateZ 约 +95px，scale 约 1.07x），确保新卡片置于舞台最靠近用户的第一前景层；
2. 视口中心就近投放：投放候选点限制在视口中心 380px 半径内，严格避开 > 400px 的外围边缘边缘虚化（edgeBlur 与 edgeFade），同时避开中央 Omnibar 禁入区；
3. 30分钟单卡独占微光脉冲呼吸：新增 isRecentVIP 响应式状态判定（30分钟内有效，且仅限当前最新诞生卡片独享，新卡到来时自动平滑转交 VIP 权），在 UICard 外框呈现 4s 慢速柔和琥珀金（rgba(245, 158, 11)）呼吸光晕，聚焦态无缝恢复正常聚焦外框。

## 验证结论
- [x] 核心逻辑已实现并通过验证
