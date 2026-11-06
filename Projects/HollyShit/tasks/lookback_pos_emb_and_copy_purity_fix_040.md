---
id: lookback_pos_emb_and_copy_purity_fix_040
title: Remove CausalContextLookback Absolute Positional Shortcut & Purify Top-1 Copy
  Spectrum
status: completed
priority: high
tags:
- phase5
- right-brain
- lookback
- pos-emb
session: bbb61e5a-3f2d-42a0-87e1-63d289f3e410
---

# Remove CausalContextLookback Absolute Positional Shortcut & Purify Top-1 Copy Spectrum

## 变更概述
Remove absolute clause index positional embedding (`pos_emb`) from `CausalContextLookback.forward` to eliminate the `j=1` positional shortcut (`qa#405886`), keep `out_lb = z_copy_unit` uncorrupted by multi-clause soft-attention `out_feat`, and tighten inference prior `sigma` proportional to `gate_lb` in `MultiStreamRightBrain.predict_prior`. 100% shape-compatible with existing checkpoints (`right_brain_stage1_step_3000`).

## 验证结论
- [x] 核心逻辑已实现并通过验证
