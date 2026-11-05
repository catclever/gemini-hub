---
id: phase5_clause_stream_dataset_032
title: 'Phase 5 ClauseStreamDataset: Full-Prefix QA + Long-Text Continuation, T=32,
  Stop Masks, IDF Context-Pool Selector Labels'
status: completed
priority: high
tags:
- phase5
- dataset
- stage1
session: conversation://bbb61e5a-3f2d-42a0-87e1-63d289f3e410
---

# Phase 5 ClauseStreamDataset: Full-Prefix QA + Long-Text Continuation, T=32, Stop Masks, IDF Context-Pool Selector Labels

## 任务目标与背景
New file training/data/clause_stream_dataset.py (design: design/tentative/2026-11-02_phase5_staged_training_plan.md §2-3). Main stream = context prefix clauses + target clauses with target_mask; QA (prompt/target, multi-turn messages) and continuation ({text} long docs, random contiguous windows) mixed by cont_ratio; stop_labels/stop_valid (QA truncated windows -> valid zeros, continuation -> invalid); source_id for logging only; IDF-weighted rare-span context-pool relevance labels ctx_rel (T,T) + sink labels for the KnowledgeSelector.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## 交付 (2026-11-02 17:30)
- 草稿测试全部通过，合并为 training/data/clause_stream_dataset.py（新文件）。
- 真实数据统计（COIG-CQIA 等 6 个 QA 文件 + calibration_corpus_3k_omni 续写）：平均主干 26 行、目标 22 行、QA 截断 46%、sink=1 占目标行 91%。
- 决定：默认 rel_threshold=0.5/q=0.6 过严（分母为目标行全部稀有片段），训练脚本将暴露 --rel_threshold/--rel_min_idf_quantile，Colab 冒烟建议 0.3/0.3，以采择器评测（选择 vs none vs oracle 左脑解码准确率）定最终值。
- 已知：parquet 不支持（chunked_mixed_omni.parquet 可作为以后的续写源）；单 epoch 未必覆盖全部 QA，训练脚本需调用 set_epoch。
