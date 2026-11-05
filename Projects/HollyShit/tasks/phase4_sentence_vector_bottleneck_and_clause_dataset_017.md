---
id: phase4_sentence_vector_bottleneck_and_clause_dataset_017
title: Phase 4 2D Sentence Vector Bottleneck & Punctuation-Split Clause Dataset
status: completed
priority: high
tags:
- phase4
- sentence-vector
- hippo-oracle
- clause-dataset
session: f89929c4-1b39-4cf5-b9cd-979e32cfc68f
---

# Phase 4 2D Sentence Vector Bottleneck & Punctuation-Split Clause Dataset

## 任务目标与背景
Redesign Phase 4 Right-Brain (`FlowMatching1DUnet` + `HiPPOOracleCUDA`) data loading and training around a 2D Sentence Vector bottleneck (`Z_sent` of shape `(B, 1024)`) and punctuation-split single-clause sequences (`seq_len = 128`):
1. `model/hippo_oracle.py`:
   - Add `encode_sentence_vector(x_seq, valid_mask=None)` and default `forward(x_seq, return_sequence=False, valid_mask=None)` so when `return_sequence=False` (now the Phase 4 default), it computes a rich 2D Sentence Vector `Z_sent` of shape `(B, 1024)` strictly over the `valid_mask` span `[0, L_eff)`:
     - Projects the valid token sequence `[0, L_eff)` onto `K=16` orthonormal shifted Legendre polynomials $P_0(s) \dots P_{15}(s)$ on $s_t = (t + 0.5) / L_{\text{eff}} \in (0, 1)$, packs the 16 temporal moments across the 16 channel sub-bands ($16 \times 64 = 1024$ channels) blended with the global valid mean $c_0$ and length ratio $\rho = L_{\text{eff}} / L$, and normalizes each sample's 2D vector to unit RMS (`Std = 1.0`).
     - Eliminates `<PAD>` contamination and provides a true 2D `(B, 1024)` sentence bottleneck so `FlowMatching1DUnet` cannot act as a 1:1 token repeater and must use `OrthogonalAttractor(x, k_attractors)` + 1D dilated convolutions.
2. `model/loss_hippo_cfm.py`:
   - Pass `return_sequence=False, valid_mask=valid_mask` to `hippo_oracle(x_target_norm, return_sequence=False, valid_mask=valid_mask)` so `h_hilbert` is a 2D Sentence Vector `(B, 1024)`.
   - Also return optional `metrics` dict (`loss_valid_raw`, `z_sent_std`) when `return_metrics=True`.
3. `training/data/dialogue_dataset.py` (`GenericPairDataset`):
   - Add punctuation-based clause/sentence chain splitting (`split_by_punctuation: bool = True`, `max_clause_chars: int = 120`, `min_clause_chars: int = 12`):
     - When loading JSONL/JSON/Parquet records (including `omni_knowledge_corpus.jsonl` records that contain `"prompt"`, `"knowledge"`, `"target"`):
       * Filter out fake negative distractors $K^-$ from `"knowledge"` (retaining only genuine $K^+$ items that share content bigrams/tokens with `prompt` or `target`), and combine genuine $K^+$ + `prompt` into a unified `base_context` string (used as `x_prompt` / `k_attractors` for Right Brain!).
       * Split multi-sentence `target` by sentence-ending punctuation (`。！？；\n`, and `.!?;` + space) into progressive single-sentence pairs `(progressive_context, target_clause)` where prior clauses are appended to `progressive_context`!
4. `training/train_phase4_hippo_flow_cuda.py`:
   - Set default `--seq_len 128`, `--min_target_len 10`, `--attractor_prob 0.90` (high-probability `k_attractors` active on 90% of training batches instead of starting at 0.0), and auto-detect `/content/omni_knowledge_corpus.jsonl` if present.
   - Pass `return_sequence=False, valid_mask=tgt_valid_mask` into `hippo_oracle(...)` during ODE evaluation, sync `checkpointer.set_step(global_step)` on every step, and add warmup + cosine LR scheduler + EMA loss logging.
   - Reference KB: `/Users/kael/.gemini/Projects/HollyShit/kb/sequence_flow_matcher.md`.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
