---
id: unified_border_beam_engine_and_aesthetic_isolation_141
title: 统一流动边框引擎架构并精准隔离水墨扫掠与单段彗尾美学
status: completed
priority: medium
tags:
- ui
- aesthetic
- refactor
session: a7bf5827-3993-452d-b349-56f141101111
---

# 统一流动边框引擎架构并精准隔离水墨扫掠与单段彗尾美学

## 变更概述
1. 统一 CardAuraGlow 为单一 BorderBeam 引擎（1 套 HTML 结构 + 1 个通用 keyframes + 统一 inset: 1.5px 贴合卡片最外沿无留边）；
2. 独享隔离：仅水墨飞白（Ink）保留卡面微透漫射扫描流光，布谷与 Bluesky 遮罩层 100% 不透明隔断，彻底禁止光线漏入卡面；
3. 尾迹净化：布谷与 Bluesky 严格回归 290°~360° 单段纯净彗尾，并抑制 temporary 呼吸晕光干扰，消除污染；
4. 修复外边缘间隙：为 .card.bugu-echo 与 .card.bsky-echo 补齐 border: 1px solid transparent，彻底消除原先外层 1px 原生白边残留。

## 验证结论
- [x] 核心逻辑已实现并通过验证
