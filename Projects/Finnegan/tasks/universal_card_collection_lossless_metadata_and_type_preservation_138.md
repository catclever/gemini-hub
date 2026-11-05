---
id: universal_card_collection_lossless_metadata_and_type_preservation_138
title: 通用卡片收集无损元数据与原始卡片类型持久化保留
status: completed
priority: high
tags:
- cards
- promotion
- metadata
- babel
session: a7bf5827-3993-452d-b349-56f141101111
---

# 通用卡片收集无损元数据与原始卡片类型持久化保留

## 任务目标与背景
实现通用卡片转正与收集无损持久化机制：1) 保留卡片原始类型(babel, curio, chat_log, note, thought等)避免降级为local/thought；2) 前端与后端无损落盘与回写Frontmatter元数据(author_name, author_avatar, published_at, source_url, echo_of, matched_anchor等)；3) storage.go支持解析上述元数据，确保重启或重载后信息不丢失。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
