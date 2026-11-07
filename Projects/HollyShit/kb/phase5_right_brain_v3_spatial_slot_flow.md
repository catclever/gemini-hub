---
title: 'Phase 5 Right-Brain v3: 32x32 空间字符槽正交同构流网络与滚动续写流架构 (#042–#043)'
description: 'Phase 5 Right-Brain v3 (#042-#043): Exact orthogonal isomorphism between
  32-band Legendre space and 32x32 spatial character-slot space, 1D SlotFlowBlock
  with in-flow SlotContextCrossAttn and decoupled slot_valid_head, j=0 short-header
  beacon elimination, succ_boost negative-logit protection, and automatic 30% rolling
  continuation stream derivation from QA passages.'
date: '2026-11-07'
---

# Phase 5 Right-Brain v3: 32x32 空间字符槽正交同构流网络与滚动续写流架构 (#042–#043)

> **核心定位**：总结 Phase 5 Stage-1 单流右脑从 v2（32 阶 Legendre 频域全局 MLP + 外部硬拷贝拔河）升级为 **v3（$32 \times 32$ 空间字符槽正交同构 1D 流网络 `SlotFlowBlock` + 流内字符槽跨注意力 `SlotContextCrossAttn` + 解耦子句长度/槽有效边界头 `slot_valid_head` + QA 语料自动派生 30% 滚动续写流）** 的数学同构原理与工程实现。

---

## 一、 核心数学同构发现 (`HiPPOOracleCUDA` $\leftrightarrow$ `LeftBrainCrystallizer`)

1. **正交基完全可逆性 ($K = L = 32, B \in O(32)$)**：
   - 在 [`HiPPOOracleCUDA.encode_sentence_vector`](file:///Users/kael/workbench/HollyShit/model/hippo_oracle.py#L147-L183) 中，长度为 $L=32$ 的子句经掩码零化 `<PAD>` 槽位后投影至 32 维 PCA 子空间 $X_{\text{low}} \in \mathbb{R}^{B \times 32 \times 32}$，随后左乘 $32 \times 32$ 离散标准正交 Legendre 矩阵 $B$ 得到 $Z_{\text{sub}} = B X_{\text{low}}$。
   - 在 [`FlowMatching1DUnet.unpack_sentence_vector`](file:///Users/kael/workbench/HollyShit/model/flow_unet_cuda.py#L342-L357)（`LeftBrainCrystallizer`）中，解包 `z_sent` 的第一步操作即为左乘 $B^\top$ 还原 $L=32$ 个空间字符槽！
   - 由于 $B^\top B = B B^\top = I_{32}$，全局 Legendre 频域 `z_norm: (..., 1024)` 与局部空间字符槽域 `X_slot: (..., L=32, d_sub=32)` 之间存在**零损正交同构映射**：
     - 正向还原：[`reconstruct_spatial_slots(z_norm)`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L710-L722)
     - 精确逆变换：[`from_spatial_slots(x_slot)`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L724-L735)
     - 切空间齐次速度变换：[`velocity_to_spatial_slots(v_norm)`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L737-L750) 与 [`velocity_from_spatial_slots(v_slot)`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L752-L764)（实测往返误差 `< 2.5e-6`）。
2. **为什么必须在空间字符槽域 $X_{\text{slot}}$ 运行右脑流网络**：
   - 在频域运行扁平 MLP 会导致 `<PAD>` 阶跃边界在 32 个频带上产生 Gibbs 振铃，且缺乏相邻字符槽 $(l-1, l, l+1)$ 的局部 1D 感受野（引发 `三三月`、`主主练` 等二字连击结巴）。
   - 在空间字符槽域 $X_{\text{slot}}$ 中，有效字符槽 $0 \le l < L_{\text{valid}}$ 为局部连续轨迹，而 `<PAD>` 尾部槽位 $l \ge L_{\text{valid}}$ 恒为精确零向量 $\mathbf{0} \in \mathbb{R}^{32}$。

---

## 二、 四大支柱架构设计 (`#042` & `#043`)

1. **支柱一：1D 空间字符槽流网络 ([`SlotFlowBlock`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L468-L563))**：
   - 将 `flow_version` 升级为 `3`（`find_compatible_ckpt` 自动跳过旧 v1/v2 权重）。
   - 每个 `SlotFlowBlock` 在 `(N, L=32, d_slot=128)` 上依次执行：
     1) **AdaLN 1D Local Conv (`kernel_size=3, padding=1`)**：直接协调相邻字符槽 $(l-1, l, l+1)$ 的局部一阶差分转移；
     2) **AdaLN 4-Head 双向 Slot Self-Attention**：全局协调 32 个槽位的句法结构；
     3) **流内上下文字符槽跨注意力 ([`SlotContextCrossAttn`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L357-L465))**：带可学习 `sink_logit`/`sink_v`、上下文槽对数权重偏置、1D 对角线跨度接力卷积 (`diag_conv`) 及 32 维原始槽速度直通旁路 (`delta_v_raw`)，既支持整句原样锁定，也支持在非抽取推理题中局部借用实体/数字片段（如 `16杯罗勒叶`、`8周`）；
     4) **AdaLN 通道 MLP**。
2. **支柱二：解耦子句长度/槽有效边界头 ([`predict_slot_validity`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L766-L783))**：
   - 遵循墓地铁律 #1 & #2（将离散 `<EOS>`/`<PAD>` 边界几何与连续语义流解耦），由 `slot_valid_head` 从 `(cond, mu)` 的空间槽特征预测 32 个槽位的有效概率 `valid_logits: (N, 32)`，通过 `slot_valid_loss` (BCE) 与 `pad_tail_loss` 监督。
   - 推理采样 ([`sample()`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1401-L1413)) 时，在空间槽域将预测句长 $\hat{L}_{\text{valid}}$ 之后的 `<PAD>` 尾部槽位直接置零后再经 $B$ 变换回 Legendre 空间，彻底消除 `<PAD>` 尾部能量泄露（实测 `<PAD>` 尾部能量降至 `7.35e-15`）。
3. **支柱三：消除 `j=0` 短标题信标与保护 `succ_boost` 多子句接力 ([`CausalContextLookback`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1590-L1850))**：
   - Key/Value 状态特征改用局部 Mamba 创新量 `h_kv = self.kv_norm(h0 - 0.85 * h_prev)`，并在 $j=0$ 有效槽位数 $\le 7$（如 `叙事片段：`、`背景资料：`）且 $j=1$ 有效时对 $t \ge 2$ 掩码屏蔽 `key_allow[:, 2:, 0] = False`，彻底根除 `qa#405886` 盲目拷贝 `j=1` 的位置捷径；
   - 当 `succ_boost > 0.15` 时先对基础 QK 内积执行 `logits.clamp(min=0.0)` 再叠加 `succ_boost`，防止提问句 $Q_t$ 与后续跟进子句 $K_{\tau+1}$ 的负内积抵消接力信号（修复 `qa#383582 c2`）；推理时按 `sigma * (1.0 - 0.85 * g_lb)` 收缩先验噪声半径。
4. **支柱四：从多子句 QA 语料自动派生 30% 滚动续写流 ([`ClauseStreamDataset._populate_cont_from_qa`](file:///Users/kael/workbench/HollyShit/training/data/clause_stream_dataset.py#L445-L495), `#043`)**：
   - 当 `--cont_paths` 为空且 `cont_ratio > 0` 时，自动从 `qa_records` 中剥离前导短冒号标题与末尾问句，提取 $\ge 6$ 子句的连续叙事段落（以及 $\ge 8$ 子句的长解释性回答）填充 `self.cont_docs`，恢复 `eff_cont_ratio = 0.30` 与 `3 QA + 3 Cont` 评测基准。
