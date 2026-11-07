---
id: web_capture_pipeline_and_router_164
title: 网页解析管道服务与二元形态路由（对话/笔记）
status: completed
priority: high
tags:
- backend
- webcapture
- chatlog
- note
session: null
---

# 网页解析管道服务与二元形态路由（对话/笔记）

## 任务目标与背景
Implement the WebCapture pipeline service in Go backend (core/webcapture).
1. Fetcher: Uses global Jina Reader to fetch URL Markdown. Fast-fail and return structured error if 403 / captcha / timeout / length < 30 (no dirty files).
2. Morphology Router: Check if AI dialogue share link (share.gemini.google/*, gemini.google.com/share/*, chatgpt.com/share/*, claude.ai/share/*) or chatlog.IsChatLog(md) -> CardTypeChatLog; otherwise CardTypeNote.
3. Capture & Wails Binding: Expose CaptureURL(url string) (*Card, error) on App, write standard .chat_log.md or .note.md to Scattering/, emit bus.EventThoughtCaptured for CosmicStage.
4. Comprehensive unit tests for fetcher, router, and capture.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
