---
id: stage1_dataset_rolling_continuation_fallback_043
title: Restore 30% Rolling Continuation Stream in ClauseStreamDataset when n_cont_docs=0
status: completed
priority: high
tags:
- phase5
- dataset
- continuation
- stage1
session: ce5e032f-64e2-4311-974a-55cddb715c0d
---

# Restore 30% Rolling Continuation Stream in ClauseStreamDataset when n_cont_docs=0

## 任务目标与背景
Fix `n_cont_docs=0 (cont_ratio eff=0.00, sampled cont frac=0.000)` in `ClauseStreamDataset` (`training/train_phase5_right_brain_stage1.py`):
When `--cont_paths` points to `omni_knowledge_corpus.jsonl` which contains only QA-formatted records (`n_cont_docs == 0`) and `cont_ratio > 0`, automatically synthesize rolling continuation documents (`source_id=1`, allvalid clauses supervised with `target_mask=True` for `t >= 1` and `stop_valid=False`) from multi-clause narrative/encyclopedia QA records (`>= 6` content clauses after stripping short colon headers `叙事片段：`/`背景资料：` and question prompts), restoring the 30% rolling continuation training stream (`samples qa/cont ~ 224/96`).

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
