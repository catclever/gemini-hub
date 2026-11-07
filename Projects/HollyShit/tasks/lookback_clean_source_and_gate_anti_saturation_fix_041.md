---
id: lookback_clean_source_and_gate_anti_saturation_fix_041
title: 'Fix Phase 5 progressive collapse: clean lookback source decoupling, gate_lb
  anti-saturation supervision, and radially-decoupled anti_stag'
status: completed
priority: high
tags:
- phase5
- right-brain
- lookback
- polar-loss
- bugfix
session: ce5e032f-64e2-4311-974a-55cddb715c0d
---

# Fix Phase 5 progressive collapse: clean lookback source decoupling, gate_lb anti-saturation supervision, and radially-decoupled anti_stag

## 任务目标与背景
Fix progressive training collapse (Step 4500->10000) observed in Colab HollyShit_phase5.ipynb:
1. Decouple Mamba's jittered/self-fed input `z_in` from `CausalContextLookback`'s clean copy/relay source `z_lookback_seq` (`z_discourse_seq[:, :-1, :]` in `MultiStreamRightBrain.compute_loss` and `forward_context`), so 30% `jitter_high_bands` O(32) rotations and 3-step Euler ODE self-feeding never corrupt `z_copy_unit` high Legendre bands (`k=6..31`) or `succ_boost` cosine similarity `sim(t, tau)`.
2. Prevent `attn_peak` / `gate_lb` saturation on non-extractive tasks (`qa#653766`) and `scale_qk` STE softmax Jacobian lock-in: clamp `scale_qk` to `max=12.0`, add length-aware sink scaling, expose `peak_logit = max_clause_logit - sink_clause_logit` in `ctx["peak_logit"]`, and add direct BCE-with-logits copy-gate supervision `gate_lb_loss` in `compute_loss` against detached oracle context match target `y_gate = ((max_ctx_cos - 0.55) / 0.25).clamp(0.0, 1.0)`.
3. Compute `dx_rms_pred` and `anti_stag` in `ThoughtFlowMatcher.compute_spatial_slot_loss` on radially-decoupled `dx_pred_iso` (`d/dr_k == 0`) so `anti_stag` optimizes cross-band phase transitions `u_pred_b` instead of inflating high-band radii `r_pred` away from `r_targ`.
4. Verify all unit and convergence tests in `tests/test_phase5_right_brain_v2.py` pass, merge drafts, and push `#040` + `#041` to `origin/main`.
References: `kb/phase5_right_brain_v2_polar_lookback.md`, `kb/graveyard/lookback_pos_emb_shortcut_and_st_jacobian_trap.md`.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
