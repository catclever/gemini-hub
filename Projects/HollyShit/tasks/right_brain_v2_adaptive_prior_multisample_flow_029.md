---
id: right_brain_v2_adaptive_prior_multisample_flow_029
title: 'Phase 5 Right-Brain v2: 1+N Dynamic Streams, 32-Band Adaptive Prior, K-Way
  Soft-Competitive Flow Matching, Stop Head, Per-Clause Selector'
status: completed
priority: high
tags:
- phase5
- right-brain
- flow-matching
- mamba
- v2
session: conversation://bbb61e5a-3f2d-42a0-87e1-63d289f3e410
---

# Phase 5 Right-Brain v2: 1+N Dynamic Streams, 32-Band Adaptive Prior, K-Way Soft-Competitive Flow Matching, Stop Head, Per-Clause Selector

## 任务目标与背景
Implement design/tentative/2026-11-02_phase5_right_brain_v2_adaptive_prior.md.
Sub-requirements:
(A) model/bicameral_right_brain.py: 1+N shared aux stream with per-step gating + orthogonal force field; PriorHead (mu, 32-band sigma) trained by band-wise heteroscedastic Gaussian NLL; ThoughtFlowMatcher v2 (remove (h_t - z_tau) residual, z0 = mu + sigma*eps, K-way blind ODE rollout, 65% winner / 35% others with low-band Mahalanobis + high-band energy match); stop_head; band-preserving high-band jitter helper; legacy interface compat.
(B) training/data/knowledge_dataset.py: discourse_stop_mask (only when answer not truncated), cand_clause_rel (T, C) bigram-overlap pseudo labels.
(C) training/train_phase5_mamba_flow_cuda.py: aux stream construction (goal + each candidate) + stream dropout 60/20/20, scheduled self-feeding, per-clause selector loss, rollout with per-step selector probing z_thought and stop head, sigma diagnostics by stream condition, new ckpt_prefix bicameral_right_brain_v2.
Verification: CPU smoke tests with random weights + built-in fallback dataset; toy sigma calibration test.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## 进展 (2026-11-02)
- (A) model/bicameral_right_brain.py, (B) training/data/knowledge_dataset.py, (C) training/train_phase5_mamba_flow_cuda.py 已合并（原文件备份为 *.bak.py，未跟踪，勿提交）。
- CPU 冒烟：A 全部通过，toy σ 校准 主干/伴飞 两种信息来源均收紧 σ_sem (0.117/0.129 vs 0.996)；B 全部通过；C E2E/resume/discourse-only 三项 exit 0。
- 待办：Colab GPU 验收（σ 分组排序、低频饱和、多解演示）；更新 Colab notebook Cell 4 前缀为 bicameral_right_brain_v2；验收后更新 kb/modular_bicameral_architecture.md §5 与 phase5 KB。
