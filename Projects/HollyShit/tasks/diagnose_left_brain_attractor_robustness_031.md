---
id: diagnose_left_brain_attractor_robustness_031
title: Build Standalone Left-Brain Attractor Robustness Diagnostic Script & Google
  Drive Colab Notebook
status: completed
priority: high
tags:
- phase5
- left-brain
- diagnostic
- colab
- attractor
session: conversation://bbb61e5a-3f2d-42a0-87e1-63d289f3e410
---

# Build Standalone Left-Brain Attractor Robustness Diagnostic Script & Google Drive Colab Notebook

## 任务目标与背景
Create standalone diagnostic script evals/diagnose_left_brain_attractor_robustness.py and Google Drive Colab notebook HollyShit_LeftBrain_Diagnostic.ipynb to test frozen LeftBrainCrystallizer + ContinuousToTextTranslatorCUDA under 4 attractor conditions:
(A) Relevant Attractor (Gold context/K+)
(B) Pure Irrelevant Distractor Attractor (unrelated clauses from other domains)
(C) Empty / No Attractor (k_attractors=None)
(D) Mixed Attractor (1 Relevant + 3 Irrelevant Distractors)
Measures Cosine Similarity, Char Accuracy, Entity/Rare-Char Accuracy, and Distractor Contamination Rate, and outputs side-by-side decoded text comparisons.

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## 交付成果 (2026-11-02)
- 独立诊断脚本：`evals/diagnose_left_brain_attractor_robustness.py`
- Colab 诊断 Notebook：`Colab Notebooks/HollyShit_LeftBrain_Diagnostic.ipynb`（内置脚本自同步，无需先 git push 即可在 Colab 直接运行）
- 本地 `basencoder_step_115000` 初步特征观察：`OrthogonalAttractor` 中完全无关的跨领域干扰句（Condition B）的 `MaxSim` 平均达 `0.694`（高于阈值 `0.08`），使 `SnapGate` 饱和在 `0.998`，待 Colab 实测完整训练左脑下的字符污染率。

## 修复 (2026-11-02 12:55)
- Colab 报 `ImportError: cannot import name '_char_bigrams'`：原因是 Colab 从 GitHub 拉代码，而 `_char_bigrams` 只存在于尚未 push 的 #029 版 knowledge_dataset.py。
- 修复：诊断脚本内置同等 `_char_bigrams`，不再依赖 #029；已重新同步 Notebook Cell 2 内嵌脚本并覆盖 Drive 上的 Notebook。
- 验证：在 GitHub HEAD 版代码副本 (/tmp/hs_old) 上运行 exit 0。
- 已知问题：本地无左脑/翻译器 ckpt 时各指标全为 0%，自动结论仍会显示 RESILIENT（误导），Colab 上有 ckpt 不受影响；结论应以真实 ckpt 结果为准。

## 修复 2 (2026-11-02 13:30)
- 修复 `sample_corpus_records` 在旧版 `BicameralClauseChainDataset` (GitHub HEAD #027) 下调用 `label_stats_sample` 与 `_build_cand_entries` 的兼容性问题。
- 使用 `inspect.signature` 动态适配构造参数，并对候选条目提取增加版本向下回退分支。
- 在旧版代码镜像 (/tmp/hs_old) 下对内置 8 样本 + 语料 4 样本全流程实测 Exit 0。
- 已重新生成并推送 `HollyShit_LeftBrain_Diagnostic.ipynb` 到 Google Drive `Colab Notebooks` 目录。

## Colab 实测结果与结论 (2026-11-02, N=72)
- Edit Sim: A 95.74% / B 92.93% / C 94.58% / D 95.01%；Entity Recall: A 96.05 / B 88.26 / C 91.77 / D 94.86。
- 结论：不重训左脑；纯无关吸引子 (B) 比不给 (C) 差约 1.7%，故采择器需要“不抄/空选项”；混入 1 条相关 (D) 接近 A。
- 已知缺陷：Contam 指标在 C 条件下也非 0（math_formula 100%），该列不可信；部分错字源于编码器/翻译器往返（π→0、沃→奋）。
