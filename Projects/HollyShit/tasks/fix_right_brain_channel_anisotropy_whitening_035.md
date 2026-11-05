---
id: fix_right_brain_channel_anisotropy_whitening_035
title: Fix Phase 5 Right-Brain 600x Subspace Channel Anisotropy via 1024-D Per-Dimension
  Whitening
status: completed
priority: high
tags:
- phase5
- right_brain
- whitening
- bugfix
session: bbb61e5a-3f2d-42a0-87e1-63d289f3e410
---

# Fix Phase 5 Right-Brain 600x Subspace Channel Anisotropy via 1024-D Per-Dimension Whitening

## 变更概述
Fix 600x PCA subspace channel variance anisotropy in Phase 5 Right Brain (`z_clause` Channel 0 has variance ~29.74 carrying 93% of energy as clause length, while Channels 1..31 have variance ~0.045 carrying 100% of lexical/character identity). Upgraded `ThoughtFlowMatcher` and `KnowledgeSelector` `z_mean` / `z_std` auto-calibration buffers from scalars to 1024-D per-dimension vectors, whitened Mamba stream inputs (`_normalize_clause_input`) and `jitter_high_bands` orthogonal rotations in `N(0, I_1024)` space, and moved `sample()` std-renormalization after `denormalize()`.

## 验证结论
- [x] 核心逻辑已实现并通过验证
