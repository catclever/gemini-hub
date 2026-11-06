---
id: omnibar_single_url_capture_165
title: OmniBar 纯 URL 嗅探捕获与卡片生成后连续输入交互
status: completed
priority: medium
tags:
- frontend
- omnibar
- ux
session: null
---

# OmniBar 纯 URL 嗅探捕获与卡片生成后连续输入交互

## 任务目标与背景
Frontend OmniBar integration for standalone single URL capture.
1. Strict Single URL Trigger: Detect exact standalone URL (^https?://\\S+$). If mixed with other text or annotations, do not trigger web capture (fallback to normal thought capture).
2. UX States: While parsing URL, show subtle parsing status / spinner in OmniBar.
3. On Success: Card spawned in CosmicStage; OmniBar input box resets and refocuses so user can immediately type follow-up thoughts/annotations.
4. On Failure: Catch error from CaptureURL, show clear toast/banner error notification (e.g. 抓取失败：页面受保护或无法提取), reset state without leaving dirty artifacts.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
