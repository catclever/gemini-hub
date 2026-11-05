---
id: universal_cosmic_ray_network_staggered_cascade_132
title: Universal CosmicRayNetwork with Staggered Cascading Photon Flow
status: completed
priority: high
tags:
- ray-network
- frontend
- animation
- night-shift
session: 34fd952a-c2fe-491e-be53-488c3ec6081a
---

# Universal CosmicRayNetwork with Staggered Cascading Photon Flow

## 任务目标与背景
Merge BuguRayNetwork and SynapseRayNetwork into a single unified CosmicRayNetwork with beamMath.ts and staggered cascading photon flow animation.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## 验证结论
- [x] 抽取 frontend/src/lib/beamMath.ts，收拢三次贝塞尔曲线、2px 吸附（Docking Inset）与卡片多层 Z 轴缩放几何计算，编写并通过全面单元测试。
- [x] 将 BuguRayNetwork 与 SynapseRayNetwork 合并为单一通用组件 CosmicRayNetwork.svelte，消除 80% 重复代码与样式冗余。
- [x] 实现瀑布式错峰级联发光 (Staggered Cascading)，多条连线依次按 90ms 梯次点亮，解决连线瞬间同步点亮的生硬感。
- [x] 实现光斑流淌脉冲 (Traveling Photon Pulse) 与端点光晕激发 (Aperture Bloom)，支持琥珀金（Bugu）与冰蓝（Bluesky/突触）双主题色彩。
- [x] 在 CosmicStage.svelte 中挂载单一通用的 CosmicRayNetwork，保留旧组件为轻量向前兼容转发器。
- [x] 全局构建 wails build -tags webkit2_41 编译成功，前端测试 180/180 通过。
