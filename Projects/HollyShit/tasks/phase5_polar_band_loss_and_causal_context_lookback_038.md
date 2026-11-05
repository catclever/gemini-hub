---
id: phase5_polar_band_loss_and_causal_context_lookback_038
title: Phase 5 Polar Decoupled Spectral-Slot Loss, Causal Context Lookback & Auto
  Context Attractors
status: completed
priority: high
tags:
- phase5
- right-brain
- polar-loss
- context-lookback
- attractors
session: bbb61e5a-3f2d-42a0-87e1-63d289f3e410
---

# Phase 5 Polar Decoupled Spectral-Slot Loss, Causal Context Lookback & Auto Context Attractors

## 任务目标与背景
1. Replace Cartesian MSE shrinkage (||x_{1,k}||* = ||z_{1,k}|| cos(theta_k)) in ThoughtFlowMatcher and PriorHead with Polar Decoupled Band & Spatial-Slot Supervision (matching per-band RMS norms ||x_{1,k}||_rms -> ||z_{1,k}||_rms and slot transition step sizes ||dx_pred||_rms -> ||dx_gt||_rms + anti-stagnation hinge independently of cosine angles).
2. Add CausalContextLookback (Multi-Head Causal Context Attention + Clause-Level Successor Relay + Sink Gate) to MultiStreamRightBrain so the main stream can directly attend back to earlier context clauses z_{0..t} after reading the question at step t, with strict checkpoint backward-compatibility pre-hook.
3. Upgrade evaluate_stage1 in train_phase5_right_brain_stage1.py to default --eval_attractors to 'auto' (using whitened clause cosine top-M context attractor retrieval when no separate Stage-2 selector checkpoint is loaded) and pass history_z/history_h across rollout steps.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
