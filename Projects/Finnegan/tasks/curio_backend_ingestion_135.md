---
id: curio_backend_ingestion_135
title: 实现 Curio 后端模块与多模态截图智能入库引擎
status: completed
priority: high
tags:
- backend
- curio
- vision
session: b5c8342e-2cbb-4933-866c-87066dbde3ae
---

# 实现 Curio 后端模块与多模态截图智能入库引擎

## 任务目标与背景
Implement Curio Backend Module & Vision Screenshot Ingestion Engine:
1. Module Scaffolding (modules/curio/):
   - Implement core/module.Module interface (Name: "curio", ConfigTarget, Init, Bindings).
   - Implement core/module.CommandProvider interface (/curio command).
2. Vision Screenshot Ingestion (modules/curio/):
   - Accept screenshot image payload + user notes + tags.
   - Use Core's Gemini LLM (via module.Context.LLMConfig()) to extract product title, brand, price, platform, intent, availability, and aesthetic tags.
   - Save full screenshot to archives/ and crop/save main product image to assets/curio/.
   - Save Markdown file to Scattering/ with .curio.md suffix and complete YAML frontmatter (intent, availability, tags, price, brand, images, screenshotPath).
   - Publish event to Global Event Bus so Watcher and RxDB pick it up instantly.
3. Tests & Quality:
   - Add unit tests in modules/curio/ for parsing, frontmatter serialization, and slug generation.
   - Ensure go test ./... passes 100%.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
