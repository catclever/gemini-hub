---
id: fix_bugu_search_rotating_border_beam_color_155
title: 修复布谷搜索时旋转边框错误显示为飞白水墨色的问题
status: completed
priority: high
tags:
- bugfix
- ui
- beam
session: a7bf5827-3993-452d-b349-56f141101111
---

# 修复布谷搜索时旋转边框错误显示为飞白水墨色的问题

## 变更概述
1. 根因修复：在执行布谷雷达搜索时，母卡因沉降保护被赋予 isVIP 状态，且原先由于母卡本身不是 bugu 来源且无 echoOf，被判断为 isRecentVIP 并跌入兜底的 ink 预设，导致母卡在搜索雷达展开时呈现灰色的水墨飞白色；
2. 搜索态识别与优先分发：在 CosmicStage 与 UICard 中透传 isBuguScanning / isBskyScanning 标志，并在 borderBeamRegistry 中赋予主动扫描状态最高模块优先级，直接分发纯正的琥珀金（bugu）或冰蓝（atproto）边框预设；
3. 来源解绑 echoOf 强依赖：对于 card.origin === 'bugu' 的卡片（包括无母卡的独立搜索结果），统一佩戴琥珀金彗尾边框；
4. 单元测试（229 项测试全绿）与 Vite 生产打包验证通过。

## 验证结论
- [x] 核心逻辑已实现并通过验证
