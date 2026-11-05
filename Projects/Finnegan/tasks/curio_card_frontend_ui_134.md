---
id: curio_card_frontend_ui_134
title: 实现奇物标本卡类型与双态高质感渲染组件 (CurioCardBody)
status: completed
priority: high
tags:
- frontend
- curio
- ui
session: b5c8342e-2cbb-4933-866c-87066dbde3ae
---

# 实现奇物标本卡类型与双态高质感渲染组件 (CurioCardBody)

## 任务目标与背景
Implement Curio Card Type & UI Component on Finnegan's Cosmic Stage:
1. Types (src/types/card.ts):
   - Add Curio fields to CosmicCard: brand, platform, price, intent ('wish'|'someday'|'archive'|'acquired'), availability ('deadstock'|'available'|'delisted'), snapshotPath, screenshotPath.
2. Component (src/components/cards/CurioCardBody.svelte):
   - Scattering Mode (200x190): Top bar with platform badge + price tag + intent badge; 92px hero image display case with subtle glow; title & fetish note snippet; interactive constellation tags.
   - Focused Mode (420x420): Specimen header with brand/price/availability/intent; multi-image detail gallery; archive action bar ([⚡ 打开离线网页快照], [🖼️ 查看长截图], [↗ 原始链接]); Markdown fetish notes; clickable tags.
3. Card Registry (src/components/cards/cardRegistry.ts):
   - Register 'curio' mapped to CurioCardBody.
4. Unit Tests & Build:
   - Add unit tests in src/lib/cardRegistry.test.ts for curio type.
   - Ensure node --test src/lib/*.test.ts passes 100%.
   - Ensure npm run build succeeds cleanly.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
