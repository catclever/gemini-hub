---
id: bugu_distiller_scheme1_and_pipeline_hardening_158
title: Bugu 蒸馏门控方案一升级、废除拒绝后摘要重试、多模态摘要接入与防扎堆收口
status: completed
priority: high
tags:
- bugu
- distiller
- babel
session: conversation://20e28f53-3575-42ff-b7fb-f69ec7e182aa
---

# Bugu 蒸馏门控方案一升级、废除拒绝后摘要重试、多模态摘要接入与防扎堆收口

## 任务目标与背景
升级 Bugu 蒸馏门控（方案一）、多模态上下文打通、防扎堆与 Babel 门卫收口：
1. 在 `modules/bugu/llm/distiller.go`：
   - 采用方案一升级共鸣门控 Prompt：保留 `object`、`motif`、`mood`、`concept` 四维平权独立通关，但明确当命中 `object` 锚点时，内容必须包含具体的经验分享、观点讨论、巧妙用法或有趣视角，过滤掉纯安装说明书、导航目录、营销软文或仅顺带提及该词却非核心讨论对象的文章。
   - 清洗传入 `keywords` 中的尾部 `*` 号，且对最终输出的 `card.MatchedAnchor` 执行 `strings.TrimRight(strings.TrimSpace(card.MatchedAnchor), "*")`。
   - 当 `keywords` 为空（如自由文本雷达或关键词尚未生成）时，允许基于 `USER INTENT` 提取核心概念作为 `matched_anchor`，避免 `keywords` 为空时 100% 丢弃。
   - 支持在 JSON Schema 中可选提取 `"title"`（若 LLM 未提取则由调用方回填 SearxNG 的 `item.Title`）。
2. 在 `modules/bugu/api/radar.go` 与 `modules/bugu/module.go`：
   - 默认 `TargetLanguage` 从 `"English"` 修正为 `"Chinese"`（`module.go:54`）。
   - 读取母卡时，一并提取 `keywords.ExtractSummariesFromMarkdown`（`visual_summary` 与 `link_summary`）拼入 `intent` 上下文，并清洗 `ExtractKeywordsForDoc` 返回词条尾部的 `*` 号。
   - 彻底移除 `radar.go:380-388` 中“全文被 Distiller 拒绝（`card == nil && !usedSearchSnippet`）后又用 Search Snippet 二次重试”的反模式逻辑；且当 Jina/Reddit 抓取失败降级到 Search Snippet 时，要求 `len([]rune(strings.TrimSpace(item.Content))) >= 80` 才允许送入 Distiller。
   - 增加单域名上限（Per-Domain Cap：单次 `ExecuteRadar` 同一主域名最多入围 2 张有效卡片）及 URL 归一化去重。
   - 在 `modules/bugu/fetcher/jina.go` 中使用 `io.LimitReader(resp.Body, 256*1024)` 并将返回的 Markdown 安全截断至最多 `15000` runes，防止超长网页撑爆上下文。
   - 卡片生成后回填 `card.Title`（优先 LLM title，回退 `item.Title`），并通过 `core/babel.UniversalSpamFilter` 校验。
参考文档：`kb/knowledge.md` 第 12、25 节。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
