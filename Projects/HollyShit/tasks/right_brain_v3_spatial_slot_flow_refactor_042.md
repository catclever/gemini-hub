---
id: right_brain_v3_spatial_slot_flow_refactor_042
title: 'Refactor Right-Brain v3: 32x32 Spatial-Slot 1D Flow, Explicit Clause Length
  Head, and Unified Slot Context Cross-Attention'
status: completed
priority: high
tags:
- phase5
- right-brain-v3
- spatial-slot-flow
- refactor
session: ce5e032f-64e2-4311-974a-55cddb715c0d
---

# Refactor Right-Brain v3: 32x32 Spatial-Slot 1D Flow, Explicit Clause Length Head, and Unified Slot Context Cross-Attention

## 任务目标与背景
Holistic Right-Brain v3 refactoring in `model/bicameral_right_brain.py` (100% compatible with frozen `TinyCharEncoderCUDA`, `HiPPOOracleCUDA`, `LeftBrainCrystallizer`, `ContinuousToTextTranslatorCUDA`, and existing trainer/eval calls):
1. Pillar 1 (Spatial-Slot Isomorphic Representation): Convert 1024-D Legendre clause vectors via `B^T` into 32x32 spatial character slots `X_slot: (..., L=32, d_sub=32)` inside `ThoughtFlowMatcher` and invert via `B` at output (`B^T B = I_32`).
2. Pillar 2 (Explicit Clause Length / Slot Validity Head + 1D Spatial-Slot Flow Network `SlotFlowNet`):
   - Add decoupled `slot_valid_head` predicting per-slot validity logits `(..., L=32)` supervised by BCE against ground-truth valid character slots (`l < L_valid`), cleanly zeroing `<PAD>` tail slots in `X_slot` at inference to eliminate degree-31 Legendre Gibbs ringing, Channel-0 600x anisotropy interference, and mid-clause `<EOS>` truncation.
   - Add 1D Spatial-Slot Conv (`kernel_size=3`) + Slot Self-Attention velocity branch (`SlotFlowNet`) over `(N, L=32, d_sub=32)` so adjacent character slots `(l-1, l, l+1)` coordinate locally in space without polynomial plateau stuttering (`三三月`, `主主练`).
3. Pillar 3 (Unified Retrieval & Generation):
   - In `CausalContextLookback`: mask out short colon-header clauses at `j=0` (`L_valid <= 6`, e.g. `叙事片段：`, `背景资料：`) from copy candidates and use local state transition `h_kv` to eliminate the `j=1` post-header shortcut on `qa#405886`; clamp base QK logits to `>= 0` on successor-boosted positions (`succ_boost > 0.35`) so negative `<Q_t, K_{tau+1}>` never cancels multi-clause relay (`qa#383582 c2`).
   - Add `SlotContextCrossAttn` inside `ThoughtFlowMatcher` (with diagonal span relay `l-1 -> l` and learnable sink) so the ODE velocity field can both lock onto full-clause copies and borrow partial entity/number spans (`16杯罗勒叶`, `8周` in `qa#653766`), and tighten copy-step prior `sigma` via `1 - 0.85 * g_lb`.
References: `kb/modular_bicameral_architecture.md`, `kb/phase5_right_brain_v2_polar_lookback.md`, `kb/graveyard/grave.md`.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
