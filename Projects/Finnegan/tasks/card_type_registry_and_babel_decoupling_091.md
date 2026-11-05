---
id: card_type_registry_and_babel_decoupling_091
title: 升级卡片类型注册与动态分发机制并彻底解耦巴别塔通用形态
status: completed
priority: high
tags:
- frontend
- architecture
- card_registry
session: b5c8342e-2cbb-4933-866c-87066dbde3ae
---

# 升级卡片类型注册与动态分发机制并彻底解耦巴别塔通用形态

## 任务目标与背景
Refactor card type registration and dispatch architecture:
1. Establish frontend Card Type Registry (src/components/cards/cardRegistry.ts) with built-in core types (thought, note, chat_log, babel) and extensible registerCardType API.
2. Decouple babel card type from bugu module ownership: babel is a universal bilingual/echo/intelligence card form usable across any module.
3. Clean up hardcoded type === 'babel' couplings across auraSearch.ts, paramCandidateEngine.ts, stageCoords.ts, etc.
4. Replace hardcoded if/else chains in UICard.svelte and VirtualCardProxy.svelte with dynamic <svelte:component this={getCardComponent(card.type)} ... />.
5. Standardize CardBody props interface (card, isFocused, isHovered, displayTime).
6. Add comprehensive unit tests in src/lib/cardRegistry.test.ts (or cardType.test.ts) covering fallback, registration, and prefix parsing.
7. Ensure all existing 73 frontend tests and backend Go tests continue to pass.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
