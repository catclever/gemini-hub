---
id: phase5_stage1_single_stream_trainer_and_selector_033
title: Phase 5 Stage-1 Single-Stream Right-Brain Trainer + Independent KnowledgeSelector
  Trainer (sink/no-copy), Zero-Init Aux Paths
status: completed
priority: high
tags:
- phase5
- right-brain
- selector
- stage1
session: conversation://bbb61e5a-3f2d-42a0-87e1-63d289f3e410
---

# Phase 5 Stage-1 Single-Stream Right-Brain Trainer + Independent KnowledgeSelector Trainer (sink/no-copy), Zero-Init Aux Paths

## 任务目标与背景
Model: zero-init aux-dependent paths (alpha_aux=0, PriorHead aux-feature input weights=0); separate stop_valid mask in compute_loss; generic sigma grouping by source; KnowledgeSelector sink/no-copy logit + context-pool loss + selection returning no attractors when sink fires; handle all-False k_mask in left brain calls. New scripts: training/train_phase5_right_brain_stage1.py (single stream, QA+continuation, rollout w/ stop, diversity demo, sigma-vs-context-length curve, per-module timing) and training/train_phase5_selector.py (context-pool selector, GT-probe+noise, optional right-brain probes). Design: design/tentative/2026-11-02_phase5_staged_training_plan.md.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
