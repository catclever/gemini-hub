---
title: 'Phase 5 Right-Brain v2: 时频双域极坐标流匹配与因果子句回看架构 (#036–#041)'
description: 'Phase 5 Right-Brain v2 (Tasks #036–#041): Per-dimension whitening, inverse-Legendre
  spatial slot & transition diff loss, polar radial-angular decoupling with radially-decoupled
  anti_stag, position-invariant CausalContextLookback with band-normalized ST Top-1
  copy, clean lookback source decoupling (z_lookback_seq), and BCE-with-logits gate_lb
  anti-saturation supervision.'
date: '2026-11-07'
---

# Phase 5 Right-Brain v2: 时频双域极坐标流匹配与因果子句回看架构 (#036–#041)

> **核心定位**：总结 Phase 5 Stage-1 单流右脑（[`MultiStreamRightBrain`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1349-L2200) + [`ThoughtFlowMatcher`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L357-L1035) + [`CausalContextLookback`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1094-L1325)）在解决“全维各向异性失明”、“句中多字连击结巴（`四四`、`给给给`）”、“长上文因果回看断链”、“第 5 槽位 `<EOS>/<PAD>` 污染截断”、“绝对位置 `j=1` 捷径与 Straight-Through 归一化雅可比零化”以及“训练中后期 `jitter_high_bands` / `self_feed` 污染回看源与非抽取任务 `gate_lb` 饱和崩坏（`#041`）”过程中确立的完整数学原理与工程实现。

---

## 一、 逐维流形白化与非阻塞内存布局 (`#036`)

1. **600 倍方差各向异性（PCA Channel 0 统治陷阱）**：
   - 在 `HiPPOOracleCUDA` 编码的 $1024$ 维子句向量（$K=32$ 个 Legendre 阶数 $\times d_{\text{sub}}=32$ 个 PCA 通道）中，每个频段的第 0 号 PCA 通道主要承载子句长度与 `<PAD>` 占比，其方差高达 $4.0 \sim 6.3^2$；而承载具体词汇语义的第 $1..31$ 号通道方差仅为 $0.08^2 \sim 0.15^2$（能量相差逾 **600 倍**）。
   - 若仅使用标量均值/标准差归一化，流匹配 MSE 与余弦损失的 $94\%$ 被第 0 号通道垄断，模型退化为仅预测句子长度而对词汇完全失明。
2. **优化方案**：
   - **逐维独立在线 EMA 白化（[`ThoughtFlowMatcher.calibrate_z`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L469-L505)）**：将 `z_mean` 与 `z_std` 升级为 `(1024,)` 逐维向量统计量，使全部 $1024$ 个频谱—通道维度独立标准化为 $\mathcal{N}(0, 1)$，1:1 均衡梯度权重。
   - **主干流输入自动白化（[`MultiStreamRightBrain._normalize_clause_input`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1523-L1528)）**：对所有非零输入子句先做逐维白化再送入 Mamba 主干流，同时保持全零 Padding 行严格为 $0$。

---

## 二、 逆 Legendre 空间槽位展开与一阶跳变差分损失 (`#037`)

1. **Legendre 多项式句中相消与平顶平台（Stuttering Plateau）**：
   - 高阶 Legendre 多项式 $P_k(t)$ 在区间两端 $t = \pm 1$（句首 `slot 0..3` 与句尾 `slot 31`）恒为 $|P_k(\pm 1)| = 1$，而在句子中段 $t \in (-0.7, +0.7)$（`slot 4..25`）振幅按 $\sqrt{\frac{2}{\pi k \sin\theta}}$ 衰减至 $\frac{1}{5} \sim \frac{1}{7}$ 且正负高频振荡。
   - 仅在频域独立监督 32 个频段时，句中缺乏跨频段相位锁定（Cross-Band Phase Locking），高频分量在句中正负相消，仅剩 4~5 阶低频慢变包络，每 3~4 个槽位形成一个平顶平台（解码为 `四四四`、`授授授`）。
2. **优化方案（[`ThoughtFlowMatcher.compute_spatial_slot_loss`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L608-L695)）**：
   - **可交换右乘通道白化 + 左乘逆 Legendre 变换**：
     利用左乘正交基底 $B^\top \in \mathbb{R}^{32 \times 32}$ 与右乘逐通道标准差对角阵 $D_{\text{chan}}^{-1} \in \mathbb{R}^{32 \times 32}$ 的矩阵乘法结合律：
     $$X_{\text{slot}} = B^\top \left(Z_{\text{phys}} D_{\text{chan}}^{-1}\right) = \left(B^\top Z_{\text{phys}}\right) D_{\text{chan}}^{-1}$$
     在不破坏任何频段间相对模长比例（**严禁人为逐频带模长均衡**）的前提下，将 32 个频段相干还原为 32 个空间字符槽位轨迹 $X_{\text{slot}} \in \mathbb{R}^{N \times 32 \times 32}$。
   - **逐槽位余弦损失（`slot_cos_loss`）+ 相邻槽位一阶跳变差分损失（`slot_diff_loss` on $\Delta X(l) = X(l+1) - X(l)$）**：
     利用微分算子 $\Delta P_k(t) \propto k P_k(t)$ 的天然高通放大特性，抵消句中 $1/\sqrt{k}$ 衰减，强制相邻字符槽位按真实步长发生字跳变。

---

## 三、 极坐标径向—角向解耦监督：根治笛卡尔 MSE 的 $\cos\theta_k$ 高频模长塌缩 (`#038`, `#041`)

1. **笛卡尔欧氏 MSE 的高频 $\cos\theta_k$ 模长塌缩定理**：
   - 对任意频段 $k \in \{0,\dots,31\}$，设真实频段向量为 $z_{1,k}$，预测向量为 $x_{1,k} = r_k \hat{u}_k$，夹角余弦为 $\cos\theta_k = \langle \hat{u}_k, \hat{z}_{1,k}\rangle$。笛卡尔欧氏误差恒等分解为：
     $$\|x_{1,k} - z_{1,k}\|^2 = \left(r_k - \|z_{1,k}\|\cos\theta_k\right)^2 + \|z_{1,k}\|^2\left(1 - \cos^2\theta_k\right)$$
   - 对径向模长 $r_k$ 求偏导为零得唯一最优解 $r_k^* = \|z_{1,k}\| \cdot \cos\theta_k$。当高频频段 $k=10..31$ 方向尚未完全对齐时，笛卡尔 MSE 会把高频模长压扁，造成句尾结巴。
2. **优化方案**：
   - **极坐标频段解耦损失（[`ThoughtFlowMatcher.compute_polar_band_loss`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L559-L606)）**：将每频段误差拆解为仅依赖径向模长的 `band_norm_loss` 与仅依赖单位方向角向的 `band_cos_loss`。
   - **空间一阶差分与 `anti_stag` 径向梯度完全解耦（`#041`）**：在 `compute_spatial_slot_loss` 中，不仅 `slot_cos_loss`、`slot_diff_cos_loss`、`env_slot_loss` 必须在径向解耦后的 `x_pred_iso` 上计算，`dx_rms_pred` 与 `anti_stag` 也必须在 `dx_pred_iso`（配合 `u_pred_b` 径向正交投影 Hook 保证 $\frac{\partial}{\partial r_k} \equiv 0$）上计算，防止 `anti_stag` 通过逆 Legendre 矩阵反向拉升高频频带半径 $r_k$ 破坏推理期 Channel-0 `<EOS>` 截断包络。
   - **`PriorHead` 高斯 NLL 正交投影解耦与独立极坐标监督（[`MultiStreamRightBrain.compute_loss`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1997-L2028)）**：通过停梯度的频段正交投影 `mu_for_nll` 校准 $\sigma_{\text{band}}$，并对 `mu_v` 与 `mu_head_v` 分别施加极坐标频段损失 + 空间槽位损失。

---

## 四、 因果上下文子句回看、频段归一化 Straight-Through Top-1 整句选通与纯净源解耦 (`#038`–`#041`)

1. **长上文问答的 Mamba 因果记忆瓶颈与第 5 槽位 `<EOS>/<PAD>` 污染定律**：
   - 语料第 0 句通常为 5 字短标题（`背景资料：`、`叙事片段：`）。一旦对多个不同长度的上下文子句做软注意力加权平均或混入软注意力均值残差 `out_feat`，短句在 `slot 5..31` 同相的 `<EOS>/<PAD>` 向量会相长叠加，直接将 18~20 字长句在半句处截断。
2. **优化方案（[`CausalContextLookback`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1094-L1325) & [`MultiStreamRightBrain`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1763-L2080)）**：
   - **位置无关内容寻址 + 严格因果掩码（$j \le t - 1$）+ 顺延接力偏置（`succ_boost`）+ 防原地复读抑制（`repeat_pen`）（`#040`）**：移除 `Q/K` 上的绝对位置编码 `pos_emb` 消除 `j=1` 捷径，并将 `out_lb = z_copy_unit * vm_col * has_prev` 与软注意力残差 `out_feat` 彻底隔离。
   - **频段归一化 Straight-Through Top-1 整句选通（`z_soft_unit` & `z_copy_unit`，`#040`）**：在 Straight-Through 替换前先将 `z_soft` 按频段（解耦 Channel 0 与第 $1..31$ 词汇通道）缩放到匹配 `z_hard.detach()` 的目标频段半径，前向 100% 保持单句拷贝频谱，反向 100% 保留 `z_soft` 处的归一化雅可比与错误子句径向稀释惩罚。
   - **Mamba 抗噪/自喂养输入 `z_in` 与 `CausalContextLookback` 纯净拷贝源 `z_lookback_seq` 解耦（`#041`）**：
     - 训练时 `z_in_override` 包含 30% 的 `jitter_high_bands`（在 $k=6..31$ 高频频带乘随机正交阵 $Q \in O(32)$）以及 Step 2000 后爬升至 25% 的 `self_feed`（3 步 Euler ODE 采样替换目标行）。若将 `z_in_override` 直接传入 `context_lookback`，会导致正确拷贝的上下文子句有 30% 概率在高频频带与 GT 完全正交而受重罚，并破坏 `succ_boost` 的余弦匹配 `sim(t, tau)`。
     - 在 `forward_context` 中新增 `z_lookback_seq`（在 `compute_loss` 中传入纯净未抖动的 `z_discourse_seq[:, :-1, :]`）：`main_stream` 继续接收带抖动和自喂养的 `z_main_in`，而 `context_lookback` 始终检索与拷贝纯净上下文谱 `z_lb_in`。
   - **非抽取任务门控反饱和对比监督（`gate_lb_loss`）与 `scale_qk` 限幅（`#041`）**：
     - 将 `scale_qk` 上限收紧至 `[1.0, 12.0]` 并在 `sink` 中补齐 `+ 0.5 * log(n_prev)` 长度偏置；
     - 在 `compute_loss` 中利用真实白化上下文最大余弦相似度构造软门控标签 `y_gate = ((max_ctx_cos - 0.55) / 0.25).clamp(0.0, 1.0)`，通过永不发生 Sigmoid 梯度消失的 `F.binary_cross_entropy_with_logits` 直接监督真值匹配槽位 `pos_logit`、压制错误干扰槽位 `neg_peak` 并在无匹配子句时（如数学推理题 `qa#653766`）将 `peak_logit` 压至负值（实测非抽取题 `gate_lb` 收敛至 `0.0004`）。

---

## 五、 双脑闭环评估管线与 PCA Channel-0 句长包络正交监督 (`#038`–`#039`)

1. **`_ctx_last(ctx)` 完整保留回看状态**与**自动白化余弦上下文吸引子（严禁将自生成子句追加进吸引子池）**。
2. **废除反归一化后 `z_out / z_out.std(dim=-1)` 的 `<PAD>` 偏移放大**，并在极坐标与空间槽位损失中对径向解耦后的 Channel-0 句长阶跃包络 `env_slot_loss` 施加显式正交监督。
