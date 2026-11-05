---
id: implement_gated_residual_anchor_translator_030
title: Implement Next-Gen Gated Residual Anchor & Decoupled Termination Translator
status: backlog
priority: low
tags:
- translator
- cnn
- architecture
- nextgen
session: db682d63-e9e1-4409-9788-273b3cdf86f1
---

# Implement Next-Gen Gated Residual Anchor & Decoupled Termination Translator

## 任务目标与背景
Design and train next-generation Continuous-to-Text Translator integrating the advantages of omni_translator_step_8106 and s32_clean:
1. Gated Residual Anchor Architecture:
   - Primary Anchor Head (fc_anchor): pure 1024D coordinate lookup skipping Conv1d, trained with standard CE loss.
   - Gated Context Residual Head (fc_ctx): local 3-gram Conv1d feature refinement, scaled by tanh(gate) (gate init 0.0) to fix typos/casing without overriding exact entity coordinates.
   - Decoupled Termination Head (fc_valid): independent binary classifier predicting active token vs pad, truncating text at first invalid position to cleanly eliminate <eos> trailing garbage.
2. Training Strategy:
   - Neighbor Perturbation (never perturb center token coordinate).
   - Mixed corpus (7:3 MOSS dialogues and omni_knowledge_corpus for rare entity coverage).
   - Hot-start fc_anchor from omni_translator_step_8106.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
