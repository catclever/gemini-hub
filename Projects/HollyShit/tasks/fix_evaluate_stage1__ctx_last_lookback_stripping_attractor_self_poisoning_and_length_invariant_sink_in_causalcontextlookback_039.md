---
id: fix_evaluate_stage1__ctx_last_lookback_stripping_attractor_self_poisoning_and_length_invariant_sink_in_causalcontextlookback_039
title: Fix evaluate_stage1 _ctx_last lookback stripping, attractor self-poisoning,
  and length-invariant sink in CausalContextLookback
status: completed
priority: medium
tags: []
session: bbb61e5a-3f2d-42a0-87e1-63d289f3e410
---

# Fix evaluate_stage1 _ctx_last lookback stripping, attractor self-poisoning, and length-invariant sink in CausalContextLookback

## 任务目标与背景
Fix three critical bugs discovered in the Step 0..380 Colab run of #038:
1. `_ctx_last(ctx)` in `training/train_phase5_right_brain_stage1.py` stripped `z_lookback` and `gate_lb`, causing `c1` and Diversity in `evaluate_stage1` to lose 100% of `CausalContextLookback`'s pointer contribution during evaluation.
2. `evaluate_stage1` appended the model's own generated `z_next` and `ids[0]` into the context attractor candidate pool `pool_z / pool_w`, causing `c2..c8` to match `c1`'s generated output (`attr=Y(cos=0.98..1.00)`) and lock into a self-feedback attractor loop; also pre-calibrate `fm.calibrate_z` before `--eval_at_start` when `calib_steps == 0`.
3. In `CausalContextLookback`, add length-invariant sink scaling `+ log(max(t, 1))` and peak-concentration weighting (`attn_peak = attn.amax(dim=-1)`) with additive residual `mu = mu_head + gate_lb * z_lookback` so diffuse attention over 15-18 clauses never damps `mu_head` or inflates `sigma_sem / sigma_syn`.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

Fixed 5 root causes identified from the Step 0–1,780 Colab evaluation logs (`HollyShit_phase5.ipynb`, commits `aa27050` and `1e28eef`):

1. **`_ctx_last(ctx)` stripped `"z_lookback"` and `"gate_lb"` on `c1` and `Diversity` ([`train_phase5_right_brain_stage1.py`](file:///Users/kael/workbench/HollyShit/training/train_phase5_right_brain_stage1.py#L499-L506))**:
   - `_ctx_last(ctx)` only copied `("h", "h0", "F_aux", "gates", "gate_max", "gate_sum")` and dropped `"z_lookback"` and `"gate_lb"`, causing `predict_prior(last)` on `c1` (and `Diversity`) to lose 100% of the `CausalContextLookback` pointer-generator path (`才应：即`, `ho“，，误*bo’>吗年素`, `向6是< <`), whereas `right_brain.step` kept `"z_lookback"` on `c2..c6` (`手里这些人还能用的都都赶紧再用用。`, `左右就有一大群身影围了上来，`).
   - Added `"z_lookback"` and `"gate_lb"` to `_ctx_last(ctx)`.

2. **Self-Feedback Attractor Poisoning in `evaluate_stage1` ([`train_phase5_right_brain_stage1.py`](file:///Users/kael/workbench/HollyShit/training/train_phase5_right_brain_stage1.py#L645-L680))**:
   - `evaluate_stage1` was appending the model's own generated `z_next` and `ids[0]` into `pool_z / pool_w`, causing `c2..c8` on `qa#653766` to match `c1`'s generated stub with `attr=Y(cos=0.74..0.89)` and lock into a self-feedback loop (`我《 即 * | 我应 即 即 | 我《 即 即`).
   - Kept `pool_z / pool_w` strictly fixed to the ground-truth context clauses `0 .. ctx_len - 1`, and added pre-calibration of `fm.calibrate_z` at Step 0 when `calib_steps == 0`.

3. **Unified Clause-Level Spectral Copy (`attn_clause`) in `CausalContextLookback` ([`bicameral_right_brain.py`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1165-L1215))**:
   - Replaced cross-head band-spliced `z_copy` (`z_heads = z_in.view(B, T, 8, 128)`) with unified clause-level copy attention `attn_clause` over all 32 Legendre bands, preserving per-band polar radius `r_copy_b` and preventing cross-clause band splicing and `<pad>` tail truncation (`目前东端：定`, `勇士敢尔：们`).
   - Added length-invariant sink scaling (`+ n_prev.log()`), peak concentration gating (`attn_peak`), and a `0.35` similarity threshold on `succ_boost`.

4. **Polar Band Interpolation in `predict_prior` + Standalone `mu_head` Supervision in `compute_loss` ([`bicameral_right_brain.py`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1717-L1875))**:
   - Interpolates `mu_head` and `z_lookback` in polar band coordinates (`r_blend`, `u_blend`) so high-frequency band norms never shrink when `0 < gate_lb < 1`.
   - Added `0.30 * (head_polar_loss + head_slot_loss)` directly on `mu_head` so `PriorHead` is always trained to generate full-length valid clauses even when `gate_lb == 0` (non-extractive math/reasoning like `qa#653766`).

Added commit `6fed567`:
5. **Straight-Through Top-1 Clause Copy (`attn_copy`) in `CausalContextLookback` ([`bicameral_right_brain.py`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1175-L1215))**:
   - Diagnosed why `勇士科尔：D`, `目前东端：定`, and `时间一菠三<三下，` broke right at character slot 5: in `omni_knowledge_corpus.jsonl`, Clause 0 is a 5-character header (`背景资料：`, `叙事片段：`, followed by `<EOS>` at slot 5 and `<PAD>` at slots 6..31). Because the HiPPO Legendre transform is linear, any soft/diffuse attention across multiple context clauses of different lengths adds the `<EOS>`/`<PAD>` tail (slots 5..31) of short clauses constructively into the middle of 15-character clauses!
   - Replaced soft-averaged `z_copy` with Straight-Through Top-1 (`attn_copy = (one_hot - probs_norm.detach() + probs_norm) * vm_col * has_prev`), so in the forward pass `z_copy_unit` is strictly a single intact context clause (`one_hot`), while in the backward pass dense softmax gradients flow through `probs_norm`.
   - Removed the double-penalizing `+ n_prev.log()` from `sink` (since `attn_peak = attn_clause.amax(dim=-1)` already scales inversely with `n_prev` under uniform logits) and aggregated head logits via `0.5 * mean + 0.5 * amax`.

Documented the complete mathematical principles, bug post-mortems, and architectural optimizations from `#036`–`#039` in:
- [`kb/phase5_right_brain_v2_polar_lookback.md`](file:///Users/kael/.gemini/Projects/HollyShit/kb/phase5_right_brain_v2_polar_lookback.md)
- [`kb/graveyard/grave.md`](file:///Users/kael/.gemini/Projects/HollyShit/kb/graveyard/grave.md#L56-L100) (§5 & §6)
- [`kb/knowledge.md`](file:///Users/kael/.gemini/Projects/HollyShit/kb/knowledge.md)
