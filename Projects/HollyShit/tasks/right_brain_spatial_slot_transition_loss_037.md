---
id: right_brain_spatial_slot_transition_loss_037
title: Right Brain Inverse-Legendre Spatial Slot & Transition Alignment Loss
status: completed
priority: high
tags:
- phase5
- right-brain
- legendre-slots
- flow-matching
session: bbb61e5a-3f2d-42a0-87e1-63d289f3e410
---

# Right Brain Inverse-Legendre Spatial Slot & Transition Alignment Loss

## 变更概述
Add inverse-Legendre spatial slot cosine alignment (`slot_cos_loss`) and adjacent-slot first-difference transition alignment (`slot_diff_loss` on `ΔX(l) = X(l+1) - X(l)`) to `ThoughtFlowMatcher` and `MultiStreamRightBrain` (`prior_nll` and `win_loss`). Uses right-multiplying channel-wise RMS scaling `D_chan^{-1}` that commutes with the left-multiplying orthogonal Legendre basis `B^T`, eliminating the 600x PCA channel-0 anisotropy while preserving 100% of the relative band norms and cross-band phases across all 32 Legendre bands. Eliminates interior destructive phase interference (`slot 4..25`) and multi-character flat plateaus (`四四四` / `授授授`) while keeping strict=True checkpoint compatibility.

## 验证结论
- [x] 核心逻辑已实现并通过验证
