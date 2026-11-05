---
id: implement_bicameral_right_brain_training_and_rollout_pipeline_027
title: Implement Stage 2/3 Bicameral Right-Brain Training & Dual-Brain Rollout Pipeline
status: completed
priority: high
tags:
- right-brain
- mamba
- bicameral
- stage2-3
session: db682d63-e9e1-4409-9788-273b3cdf86f1
---

# Implement Stage 2/3 Bicameral Right-Brain Training & Dual-Brain Rollout Pipeline

## 任务目标与背景
Implement Stage 2 & Stage 3 Right-Brain Training and Dual-Brain Closed-Loop Evaluation Pipeline:
1. Add BicameralClauseChainDataset in training/data/knowledge_dataset.py (or dialogue_dataset.py) to slice dialogues and knowledge records into seq_len=32 punctuation-separated clauses (10-28 chars per clause):
   - w_goal: (max_goal_clauses, 32) user question/goal clauses
   - w_cand: (max_cand_clauses, 32) candidate knowledge/history clauses (positive K+ and negative distractors K-) with cand_pos_mask (max_cand_clauses,)
   - w_discourse: (max_discourse_clauses, 32) progressive sequence of punctuation clauses [lead_question_clause, target_clause_0, ..., target_clause_{T-1}] with discourse_valid_mask so MultiStreamRightBrain steps clause-by-clause (1 Mamba step = 1 punctuation clause).
2. Upgrade training/train_phase5_mamba_flow_cuda.py to train MultiStreamRightBrain + KnowledgeSelector (model/bicameral_right_brain.py) paired with frozen TinyCharEncoderCUDA, frozen HiPPOOracleCUDA(num_subbands=32), frozen LeftBrainCrystallizer(num_subbands=32), and frozen ContinuousToTextTranslatorCUDA:
   - Support --active_streams ('discourse' for Stage 2A single-stream warmup, or 'discourse,knowledge,goal' for Stage 2B full multi-stream with zero-init orthogonal gates).
   - Compute joint loss: MultiStreamRightBrain.compute_loss (ThoughtFlowMatcher in 1024-D clause-vector space) + selector_weight * KnowledgeSelector.compute_selection_loss.
   - Save/load right_brain and knowledge_selector via Checkpointer.
   - Perform End-to-End Dual-Brain Autoregressive Multi-Clause Rollout Evaluation across 8 domains (Right Brain samples z_thought^(t) -> KnowledgeSelector selects active character pool A_active^(t) -> frozen LeftBrainCrystallizer integrates 10-step Euler ODE -> Translator decodes full multi-clause response).

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
