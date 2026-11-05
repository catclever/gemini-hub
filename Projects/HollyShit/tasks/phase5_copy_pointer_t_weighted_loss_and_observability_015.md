---
id: phase5_copy_pointer_t_weighted_loss_and_observability_015
title: Phase 5 Low-Rank CopyPointerHead, t^2-Weighted Potential Loss, Entity-Overlap
  Relaxation & Training Observability
status: completed
priority: high
tags:
- phase5
- mamba
- copy_pointer
- loss
- training
session: conversation://f89929c4-1b39-4cf5-b9cd-979e32cfc68f
---

# Phase 5 Low-Rank CopyPointerHead, t^2-Weighted Potential Loss, Entity-Overlap Relaxation & Training Observability

## 任务目标与背景
Implement the approved Phase 5 four-issue resolution plan without unfreezing Phase 4 Unet and without auxiliary CE loss:
1. Low-Rank CopyPointerHead in MultiStreamMambaPlanner (model/flow_mamba.py):
   - Add CopyPointerHead (d_ptr=64, DWConv1d(k=3) on knowledge keys, learnable sink_logit for 'no-copy' zero-pollution, identity value transport of normalized knowledge tokens without v_proj, pointer-generator gating (1 - p_sink) * h + copy_vec).
   - Integrate into the final 2 canvas layers of forward_canvas; expose copy_prob_mean in aux_dict / forward_canvas outputs. Keep total parameters < 80M (~79.0M).
2. Time-Weighted Potential Loss & t-Bucket Metrics (model/loss_mamba_cfm.py):
   - Weight loss_potential by w_pot(t) = 3.0 * t^2 (mean weight = 1.0 over U[0,1], suppressing irreducible L2 pull at t->0 while preserving scale).
   - Report t-bucketed raw potential MSE (pot_t_low for t<0.3, pot_t_mid for 0.3<=t<0.7, pot_t_high for t>=0.7) and copy_prob_mean in metrics.
3. Relaxed Clause-Disjoint / Entity-Overlap Allowed & Narrative Context Expansion (training/data/knowledge_dataset.py, scripts/build_phase5_knowledge_corpus.py):
   - Replace overly strict substring rejection (k not in target) with whole-clause non-identity check (allow entities, table/column names, numbers, equations, and short identifiers to naturally overlap between K+ and target while forbidding verbatim whole-sentence/clause copies >= 24 chars).
   - In scripts/build_phase5_knowledge_corpus.py: stop erasing eq from cot in math_rule; expand literature_lore prompt to multi-sentence narrative context (up to ~380 chars); preserve input in code_api even when identifiers appear in output.
   - Add optional return_domain_id=True to MultiStreamKnowledgeDataset (default False for backwards compatibility) returning 4-tuple (w_t, w_know, w_tgt, domain_id).
4. LR Warmup+Cosine Schedule, EMA & Per-Domain/t-Bucket Logging, Fixed Eval & Attractor Ablation Flag (training/train_phase5_mamba_flow_cuda.py):
   - Add linear warmup (--warmup_steps=1000) + cosine decay to --min_lr_ratio=0.1; align scheduler step with resumed global_step.
   - Track and print EMA (alpha=0.98) losses, t-bucket potential MSE, copy_prob, and per-domain loss breakdown every 50 steps.
   - Build a deterministic fixed cross-domain evaluation benchmark set (1 sample per domain) for periodic Euler ODE qualitative + quantitative evaluation, and add --attractor_mode (full | prompt_only | none) CLI flag.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
