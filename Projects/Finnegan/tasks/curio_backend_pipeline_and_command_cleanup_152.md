---
id: curio_backend_pipeline_and_command_cleanup_152
title: 清理 curio 冗余命令并实现后端 CaptureCurio 视觉摄取与落盘流水线
status: completed
priority: high
tags:
- backend
- curio
- vision
session: b5c8342e-2cbb-4933-866c-87066dbde3ae
---

# 清理 curio 冗余命令并实现后端 CaptureCurio 视觉摄取与落盘流水线

## 任务目标与背景
Backend Curio module pipeline cleanup & CaptureCurio:
1. In modules/curio/module.go, remove the unused /curio slash command so Omnibar command list stays clean.
2. Provide App.CaptureCurio(text string, images []ImagePayload) (string, error) bound to Wails frontend (or routed via curio module).
3. Connect CaptureCurio to IngestScreenshot in modules/curio/vision.go:
   - If images are provided, decode payload, run Gemini Vision analysis (title, brand, price, platform, intent, availability, tags), crop hero image, save full screenshot, write .curio.md, and emit bus event.
   - If no images provided, create .curio.md directly with YAML frontmatter from user text/tags.
4. Add comprehensive unit tests in modules/curio/ and ensure go test ./... passes 100%.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
