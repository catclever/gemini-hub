---
id: fix_checkpoint_emergency_step_and_auto_resume_014
title: Fix Checkpointer Emergency Step Tracking and Auto-Resume Architecture Compatibility
  Validation
status: completed
priority: medium
tags:
- training
- checkpoint
- phase5
session: f89929c4-1b39-4cf5-b9cd-979e32cfc68f
---

# Fix Checkpointer Emergency Step Tracking and Auto-Resume Architecture Compatibility Validation

## 变更概述
1. Dynamically sync checkpointer.current_step = global_step on each training step and within Checkpointer.save() so SIGINT/SIGTERM emergency checkpoints reflect the true global step rather than step 0.
2. In train_phase5_mamba_flow_cuda.py, implement find_compatible_mamba_ckpt to test candidate checkpoints in descending step order with strict state_dict compatibility, skipping incompatible legacy checkpoints (e.g. #012 weights) and preventing newer compatible saves from being shadowed.

## 验证结论
- [x] 核心逻辑已实现并通过验证
