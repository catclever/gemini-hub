---
id: fix_prompt_tail_truncation_and_clause_reordering_in_corpus_and_dataset_022
title: Fix Prompt Tail Truncation and Clause Reordering in Corpus Builder and Dataset
  Loader
status: completed
priority: high
tags:
- phase4
- dataset
- corpus
- bugfix
session: f89929c4-1b39-4cf5-b9cd-979e32cfc68f
---

# Fix Prompt Tail Truncation and Clause Reordering in Corpus Builder and Dataset Loader

## 任务目标与背景
Fix prompt tail truncation and unnatural clause/comma reordering in both training/data/dialogue_dataset.py (for immediate effect on existing JSONL datasets) and scripts/build_omni_knowledge_corpus.py (for clean corpus generation): preserve full question lines when trimming context to prompt_seq_len, strip forum boilerplate prefixes like '划重点：'/'谢邀', repair inverted trailing clauses, and keep natural sentence/comma order in corpus builders.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
