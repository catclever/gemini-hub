---
id: chatlog_speaker_filter_and_bold_tolerance_168
title: 完善对话卡片发言人识别与 Markdown 加粗容错机制
status: completed
priority: medium
tags:
- frontend
- chatlog
- parser
- markdown
session: 80c9dc92-1244-46ad-ac30-e2dd22f5b22a
---

# 完善对话卡片发言人识别与 Markdown 加粗容错机制

## 任务目标与背景
在 parseDialogue 中增强已知 participants 感知与非发言人行（有序列表、标题、中文句式）过滤，避免正文列表项误识别为角色；同时在 renderInlineDialogue 中加入大模型中文引号/星号倒挂容错与未闭合加粗自愈，并支持角色名富文本渲染。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
