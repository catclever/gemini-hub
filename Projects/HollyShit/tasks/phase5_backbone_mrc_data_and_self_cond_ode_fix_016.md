---
id: phase5_backbone_mrc_data_and_self_cond_ode_fix_016
title: Phase 5 Backbone MRC Corpus & Self-Conditioned ODE Anti-Collapse Fix
status: completed
priority: high
tags:
- phase5
- mamba
- mrc-data
- ode-collapse-fix
session: f89929c4-1b39-4cf5-b9cd-979e32cfc68f
---

# Phase 5 Backbone MRC Corpus & Self-Conditioned ODE Anti-Collapse Fix

## 任务目标与背景
Update Phase 5 Mamba backbone training and data pipeline:
1. Corpus & Dataset (`scripts/build_phase5_knowledge_corpus.py`, `training/data/knowledge_dataset.py`, `training/train_phase5_mamba_flow_cuda.py`):
   - Replace broken disjoint-split `encyclopedia_rag` (Wikipedia/Zhihu) with true grounded Reading Comprehension (`cmrc2018`, `dureader_robust`, `squad`), expanding ultra-short span answers into full factual clauses from the context passage so the backbone learns complete sentence trajectories.
   - Update `is_non_cheating_knowledge(k, target)` to allow extractive/reading-comprehension answers (`tgt_clean in k_clean`) as long as `k_clean != tgt_clean` and `len(tgt_clean) < 0.85 * len(k_clean)`, so MRC supporting passages are preserved in `K+`.
   - Default corpus builder and dataset `--active_domains` to the pure grounded backbone set (`grounded_instruct,encyclopedia_rag`, with CLI `--active_domains` and `--include_all_domains` flags so existing JSONL files in Colab automatically filter out ungrounded `literature_lore` and legacy disjoint-split records without needing a full re-download if desired, while also supporting fast HF streaming rebuild of the MRC+GroundedInstruct corpus).
2. Left-Brain Mamba Self-Conditioning & Anti-Collapse Loss (`model/flow_mamba.py`, `model/loss_mamba_cfm.py`, `training/train_phase5_mamba_flow_cuda.py`):
   - Equip Stage 1 `encode_macro` with `macro_copy_pointer` (`CopyPointerHead`) so `h_macro_potential` already incorporates copied knowledge entities at Euler step 0 (`t=0`).
   - Eliminate the teacher-forced `x_t_prev` autoregressive shortcut during training: in `FlowMamba.forward` (or via `x_t_prefix_source`), construct the causal prefix fed to `x_t_prev` from the model's own Stage 1 prediction `t * h_macro_potential.detach() + (1 - t) * x_0` (or `x_t_prefix`), aligning single-step training 100% with 10-step parallel Euler ODE inference.
   - Replace extreme `3 * t^2` potential weighting with gentle `0.5 + t`, raise `loss_macro` weight to `0.75`, add spherical cosine & radial norm preservation loss (`loss_cos`) to prevent origin collapse (`' '` / `'έ'`), and fix `per_sample_pot` denominator to normalize strictly over valid `target_mask` tokens.
   - Reference KB: `/Users/kael/.gemini/Projects/HollyShit/kb/phase5_multistream_mamba_planner.md`.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
