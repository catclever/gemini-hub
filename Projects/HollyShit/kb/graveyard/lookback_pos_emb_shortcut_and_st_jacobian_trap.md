---
title: CausalContextLookback 绝对位置 `pos_emb[j=1]` 捷径与朴素 Straight-Through 归一化雅可比零化陷阱
  (#040)
description: 'Graveyard #040: Why start-of-sequence `pos_emb` in `CausalContextLookback`
  creates a `j=1` QA shortcut (`qa#405886`), and why naive Straight-Through Top-1
  before band normalization suffers 1/sqrt(T) gradient loss and Euler-homogeneity
  Jacobian zeroing unless `z_soft` is band-normalized (`z_soft_unit`) prior to the
  Straight-Through swap.'
date: '2026-11-06'
---

# CausalContextLookback 绝对位置 `pos_emb[j=1]` 捷径与朴素 Straight-Through 归一化雅可比零化陷阱 (#040)

## 1. 故障现象
1. **实训 Step 1,000 → Step 1,500+ 长文首句位置倒退（`qa#405886`）**：
   - 在 18 句长上文叙事题 `qa#405886` 上，模型在 `Step 1,000` 已精准定位文末第 12~14 句真答案（`这群人并不是一直都守在这里等待的， | 而是知道今天是江守、郑先宇、 | 董静三个走出天化池的日子才刻意来迎接。`，`cos(GT) = 0.909 ~ 0.994`）；
   - 但训练推进到 `Step 1,500 ~ 3,000` 后，`c1` 反而跳回文章开头的第 1 句 `j = 1`（`时间一晃三个月后，`），并顺延复述第 1~5 句。
2. **移除 `pos_emb` 与 `out_lb` 中的 `out_feat` 后，合成 15 句检索 `test_2` 首句收敛退化**：
   - 直接使用朴素 Straight-Through Top-1 `attn_copy = one_hot - probs_norm.detach() + probs_norm`、`z_copy_unit = bmm(attn_copy, z_in)` 作为唯一回看谱 `out_lb` 时，`test_2_causal_context_lookback` 中 `cos_c1` 跌至 `0.7370`（其中第 3 个样本 `b=2` 卡死在 `0.0094`）。

## 2. 数学根因
1. **绝对位置编码 `pos_emb` 诱发 `j = 1` 统计捷径**：
   - 语料库中大量阅读理解题的第 `0` 句为标题（`背景资料：` / `叙事片段：`），标准答案直接从第 `1` 句（`j = 1`）开始。在 `k_in` 上直接叠加从句首计数的绝对正弦位置编码 `pos_emb[0..T-1]` 后，`k_proj` 在 `Step 1,000 -> 1,500` 间学会了对 `pos_emb[j = 1]` 赋予极高固定权重，只要提问句缺乏罕见实体词便无脑指向 `j = 1`。
2. **朴素 Straight-Through 在下游频段归一化 `u_lb = lb / r_lb` 处的雅可比错位（Euler 齐次零化）**：
   - 在 `MultiStreamRightBrain.predict_prior` 中，`z_lookback` 按频段执行单位化 $\hat{u}_{\text{lb}} = \text{lb} / r_{\text{lb}}$。
   - 朴素 Straight-Through 的前向值为硬选通单句 `z_hard`（半径 $r_{\text{hard}} \approx 1.0$），而非软加权组合 `z_soft = bmm(probs_norm, z_in)`（漫散时半径 $r_{\text{soft}} \approx \|p\|_2 \approx 1/\sqrt{T}$）。
   - 因此反向传播在 `z_hard` 处计算归一化雅可比 $\frac{1}{r_{\text{hard}}}(I - \hat{z}_{j^*}\hat{z}_{j^*}^\top)$，不仅丢失了 $\frac{1}{\|p\|_2} \approx \sqrt{T}$ 的梯度放大，更因 $(I - \hat{z}_{j^*}\hat{z}_{j^*}^\top)z_{j^*} \equiv 0$ 彻底抹杀了真软归一化 $\hat{z}_{\text{soft}} = \frac{\sum_k p_k z_k}{\|p\|_2}$ 对非目标子句 $k \neq j^*$ 的径向稀释惩罚 $-\frac{p_{j^*}p_k}{\|p\|_2^3}$。

## 3. 根治准则（铁律）
1. **严禁在 `CausalContextLookback` 的 `Q/K` 上叠加从 0 开始的绝对子句下标编码 `pos_emb`**；跨句顺承完全交由基于内容匹配的 `succ_boost` 与 Mamba 因果状态完成。
2. **凡在下游存在归一化算子（`v / ||v||`）的 Straight-Through Top-1 选通，必须在 Straight-Through 替换前先对软向量 `z_soft` 执行频段模长对齐（`z_soft_unit = z_soft * (r_hard.detach() / r_soft)`），再令 `z_copy_unit = z_hard.detach() + z_soft_unit - z_soft_unit.detach()`**，使前向保持 100% 单句纯净频谱，反向在 `z_soft` 处求取真实归一化雅可比。
