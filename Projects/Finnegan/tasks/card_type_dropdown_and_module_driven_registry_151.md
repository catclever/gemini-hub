---
id: card_type_dropdown_and_module_driven_registry_151
title: 实现 OmniBar 冒号卡片类型选择面板与模块动态驱动注册降级机制
status: completed
priority: high
tags:
- frontend
- omnibar
- dropdown
- card_registry
session: b5c8342e-2cbb-4933-866c-87066dbde3ae
---

# 实现 OmniBar 冒号卡片类型选择面板与模块动态驱动注册降级机制

## 任务目标与背景
Frontend interaction upgrade & module-driven card registry:
1. Build CardTypeDropdown.svelte in src/components/omnibar/ displaying available types (thought, note, chat_log, curio, etc.) with icons & descriptions.
2. In OmniBar.svelte, detect ':' at start of input, show CardTypeDropdown, support ArrowUp/Down and Tab/Enter to autocomplete e.g. ':curio '.
3. In cardRegistry.ts & App.svelte, dynamically sync available card types based on backend GetModuleManifests(); if curio module is not active, curio cards gracefully fall back to ThoughtCardBody.
4. Support :curio in OmniBar submission and forward to onCaptureCurio.
5. Unit tests in frontend and ensure node --test src/lib/*.test.ts passes.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
