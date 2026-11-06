# Phase 5 Right-Brain v2: 时频双域极坐标流匹配与因果子句回看架构 (#036–#039)

> **核心定位**：总结 Phase 5 Stage-1 单流右脑（[`MultiStreamRightBrain`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1240-L2060) + [`ThoughtFlowMatcher`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L357-L1035) + [`CausalContextLookback`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1045-L1225)）在解决“全维各向异性失明”、“句中多字连击结巴（`四四`、`给给给`）”、“长上文因果回看断链”与“第 5 槽位 `<EOS>/<PAD>` 污染截断”过程中确立的完整数学原理与工程实现。

---

## 一、 逐维流形白化与非阻塞内存布局 (`#036`)

1. **600 倍方差各向异性（PCA Channel 0 统治陷阱）**：
   - 在 `HiPPOOracleCUDA` 编码的 $1024$ 维子句向量（$K=32$ 个 Legendre 阶数 $\times d_{\text{sub}}=32$ 个 PCA 通道）中，每个频段的第 0 号 PCA 通道主要承载子句长度与 `<PAD>` 占比，其方差高达 $4.0 \sim 6.3^2$；而承载具体词汇语义的第 $1..31$ 号通道方差仅为 $0.08^2 \sim 0.15^2$（能量相差逾 **600 倍**）。
   - 若仅使用标量均值/标准差归一化，流匹配 MSE 与余弦损失的 $94\%$ 被第 0 号通道垄断，模型退化为仅预测句子长度而对词汇完全失明。
2. **优化方案**：
   - **逐维独立在线 EMA 白化（[`ThoughtFlowMatcher.calibrate_z`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L469-L505)）**：将 `z_mean` 与 `z_std` 升级为 `(1024,)` 逐维向量统计量，使全部 $1024$ 个频谱—通道维度独立标准化为 $\mathcal{N}(0, 1)$，1:1 均衡梯度权重。
   - **主干流输入自动白化（[`MultiStreamRightBrain._normalize_clause_input`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1461-L1466)）**：对所有非零输入子句先做逐维白化再送入 Mamba 主干流，同时保持全零 Padding 行严格为 $0$。

---

## 二、 逆 Legendre 空间槽位展开与一阶跳变差分损失 (`#037`)

1. **Legendre 多项式句中相消与平顶平台（Stuttering Plateau）**：
   - 高阶 Legendre 多项式 $P_k(t)$ 在区间两端 $t = \pm 1$（句首 `slot 0..3` 与句尾 `slot 31`）恒为 $|P_k(\pm 1)| = 1$，而在句子中段 $t \in (-0.7, +0.7)$（`slot 4..25`）振幅按 $\sqrt{\frac{2}{\pi k \sin\theta}}$ 衰减至 $\frac{1}{5} \sim \frac{1}{7}$ 且正负高频振荡。
   - 仅在频域独立监督 32 个频段时，句中缺乏跨频段相位锁定（Cross-Band Phase Locking），高频分量在句中正负相消，仅剩 4~5 阶低频慢变包络，每 3~4 个槽位形成一个平顶平台（解码为 `四四四`、`授授授`）。
2. **优化方案（[`ThoughtFlowMatcher.compute_spatial_slot_loss`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L620-L685)）**：
   - **可交换右乘通道白化 + 左乘逆 Legendre 变换**：
     利用左乘正交基底 $B^\top \in \mathbb{R}^{32 \times 32}$ 与右乘逐通道标准差对角阵 $D_{\text{chan}}^{-1} \in \mathbb{R}^{32 \times 32}$ 的矩阵乘法结合律：
     $$X_{\text{slot}} = B^\top \left(Z_{\text{phys}} D_{\text{chan}}^{-1}\right) = \left(B^\top Z_{\text{phys}}\right) D_{\text{chan}}^{-1}$$
     在不破坏任何频段间相对模长比例（**严禁人为逐频带模长均衡**）的前提下，将 32 个频段相干还原为 32 个空间字符槽位轨迹 $X_{\text{slot}} \in \mathbb{R}^{N \times 32 \times 32}$。
   - **逐槽位余弦损失（`slot_cos_loss`）+ 相邻槽位一阶跳变差分损失（`slot_diff_loss` on $\Delta X(l) = X(l+1) - X(l)$）**：
     利用微分算子 $\Delta P_k(t) \propto k P_k(t)$ 的天然高通放大特性，抵消句中 $1/\sqrt{k}$ 衰减，强制相邻字符槽位按真实步长发生字跳变。

---

## 三、 极坐标径向—角向解耦监督：根治笛卡尔 MSE 的 $\cos\theta_k$ 高频模长塌缩 (`#038`)

1. **笛卡尔欧氏 MSE 的高频 $\cos\theta_k$ 模长塌缩定理**：
   - 对任意频段 $k \in \{0,\dots,31\}$，设真实频段向量为 $z_{1,k}$，预测向量为 $x_{1,k} = r_k \hat{u}_k$，夹角余弦为 $\cos\theta_k = \langle \hat{u}_k, \hat{z}_{1,k}\rangle$。笛卡尔欧氏误差恒等分解为：
     $$\|x_{1,k} - z_{1,k}\|^2 = \left(r_k - \|z_{1,k}\|\cos\theta_k\right)^2 + \|z_{1,k}\|^2\left(1 - \cos^2\theta_k\right)$$
   - 对径向模长 $r_k$ 求偏导为零得唯一最优解：
     $$r_k^* = \|z_{1,k}\| \cdot \cos\theta_k$$
   - 当高频频段 $k=10..31$ 方向尚未完全对齐（$\cos\theta_k \approx 0.30$）时，所有笛卡尔 MSE 项（`vel_loss`、`end_mse`、`band_gaussian_nll` 对 $\mu$ 的二次项、以及 $\Delta X$ 的欧氏差）都会在数学上把高频模长强行压扁到真实模长的 $30\%$（能量仅剩 $9\%$），形成天然低通滤波器并造成句尾两字结巴（`四四`、`给给给`、`话话`）。
2. **优化方案**：
   - **极坐标频段解耦损失（[`ThoughtFlowMatcher.compute_polar_band_loss`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L580-L618)）**：
     将每频段误差拆解为仅依赖径向模长的 `band_norm_loss`（最优解恒为 $r_k^* = \|z_{1,k}\|$，与 $\cos\theta_k$ 完全解耦）与仅依赖单位方向角向的 `band_dir_loss`。
   - **空间一阶差分极坐标化与防驻留铰链惩罚（`slot_diff_cos_loss` + `slot_diff_norm_loss` + `anti_stag`）**：
     废除 $\Delta X(l)$ 上的笛卡尔欧氏 MSE，改为独立监督跳变方向 $\cos(\Delta X_{\text{pred}}, \Delta X_{\text{gt}})$ 与跳变步长模长 $\|\Delta X_{\text{pred}}\| \leftrightarrow \|\Delta X_{\text{gt}}\|$，并对真实发生换字（$\|\Delta X_{\text{gt}}\| > 0.35$）的位置施加防驻留惩罚 $\text{ReLU}(0.75 \|\Delta X_{\text{gt}}\| - \|\Delta X_{\text{pred}}\|)^2$。
   - **`PriorHead` 高斯 NLL 正交投影解耦与独立极坐标监督（[`MultiStreamRightBrain.compute_loss`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1844-L1872)）**：
     - 通过停梯度的频段正交投影 `mu_for_nll = from_bands(mu_unit_b.detach() * r_z1_b * cos_b)` 校准不确定度 $\sigma_{\text{band}}$，切断 `band_gaussian_nll` 压缩 $\mu$ 模长的梯度通路；
     - 同时对融合后的先验均值 `mu_v` 与 `PriorHead` 原始输出 `mu_head_v` 分别施加极坐标频段损失 + 空间槽位损失（`0.30 * (head_polar_loss + head_slot_loss)`），确保在无需回看上文的非抽取式推理题（如数学应用题 `qa#653766`）上 `PriorHead` 也能独立输出完整长句。

---

## 四、 因果上下文子句回看与 Straight-Through Top-1 整句选通 (`#038`–`#039`)

1. **长上文问答的 Mamba 因果记忆瓶颈与第 5 槽位 `<EOS>/<PAD>` 污染定律**：
   - 阅读理解样本将问题置于 15~18 个背景子句末尾，单向量 Mamba 在读前 14 句时不知问题为何，无法在提问步精准定位前文第 1~3 句，也无法在多句回答时顺延输出下一句。
   - **第 5 槽位 `<EOS>/<PAD>` 污染定律**：语料第 0 句通常为 5 字短标题（`背景资料：`、`叙事片段：`，`slot 0..4` 为汉字，`slot 5` 为 `<EOS>`，`slot 6..31` 为 `<PAD>`）。由于 HiPPO Legendre 变换具有严格线性性，一旦对多个不同长度的上下文子句做软注意力加权平均（$\sum_j \alpha_j z_j$），短句在 `slot 5..31` 完全同相的 `<EOS>/<PAD>` 向量会相长叠加，直接将 15 字长句在第 5 个槽位截断（产生 `勇士科尔：D`、`时间一菠三<三下，`、`目前东端：定`）。
2. **优化方案（[`CausalContextLookback`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1045-L1225) & [`MultiStreamRightBrain.predict_prior`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1715-L1737)）**：
   - **严格因果掩码（$j \le t - 1$）+ 顺延接力偏置（`succ_boost`）+ 防原地复读抑制（`repeat_pen`）**：
     - 严格屏蔽对角线 $j = t$，杜绝自拷贝当前输入子句；
     - 当当前输入子句 $z_{\text{in}}[t]$ 与前文子句 $\tau \le t - 2$ 匹配（$\text{sim} > 0.35$）时，顺延激活其后继子句 $j = \tau + 1 \le t - 1$（`succ_boost`），同时对 $\tau$ 本身施加 $-25 \cdot \text{ReLU}(\text{sim}_{\text{full}} - 0.65)$ 复读惩罚。
   - **Straight-Through Top-1 整句选通（`attn_copy`）**：
     - 采用 `0.5 * mean + 0.5 * amax` 聚合多头 Logits（防止单头命中被 8 头平均稀释）；
     - 构造 `attn_copy = (one_hot - probs_norm.detach() + probs_norm) * vm_col * has_prev`：**前向传播 100% 选通单一完整上下文子句 `one_hot`**（彻底杜绝不同长度子句混合导致的第 5 槽位 `<EOS>/<PAD>` 截断与跨头 Legendre 频段错位），**反向传播沿 `probs_norm` 传递稠密梯度**。
   - **极坐标频段插值融合（Polar Band Prior Interpolation）**：
     - 在 `predict_prior` 中按极坐标频段融合 `mu_head` 与 `z_lookback`（半径线性插值 $r_{\text{blend}} = (1 - g) r_{\text{mh}} + g r_{\text{lb}}$，方向单位化插值 $\hat{u}_{\text{blend}} = \text{Normalize}((1 - g)\hat{u}_{\text{mh}} + g\hat{u}_{\text{lb}})$），在任意门控权重 $g \in [0, 1]$ 下 100% 保持高频频段模长不衰减。

---

## 五、 双脑闭环评估管线修复 (`#038`–`#039`)

1. **`_ctx_last(ctx)` 完整保留回看状态（[`train_phase5_right_brain_stage1.py`](file:///Users/kael/workbench/HollyShit/training/train_phase5_right_brain_stage1.py#L500-L506)）**：
   - 将 `"z_lookback"` 与 `"gate_lb"` 纳入 `_ctx_last(ctx)` 保留键，确保评估首句 `c1` 与 `Diversity` 采样同 `c2..c8` 一样完整享受 `CausalContextLookback` 先验通路。
2. **自动白化余弦上下文吸引子与防自激污染（[`evaluate_stage1`](file:///Users/kael/workbench/HollyShit/training/train_phase5_right_brain_stage1.py#L548-L685)）**：
   - 默认启用 `--eval_attractors auto`：当未加载外部 `KnowledgeSelector` 时，自动使用白化子句余弦（`0.6 * sim_sem + 0.4 * sim_full >= 0.25`）从真实上文子句池 `0 .. ctx_len - 1` 召回 Top-$M$ 吸引子辅助左脑结晶器消除 32 维 PCA 截断误差；
   - **严禁将模型自生成的预测子句追加进吸引子池 `pool_z / pool_w`**，彻底杜绝闭环滚动时 `c2..c8` 命中 `c1` 噪声引发的自激复读死循环。

---

## 六、 反归一化后 `std` 强行缩放陷阱与 PCA Channel-0 句长包络正交监督 (`#039` 进阶修复)

1. **现象特征（Step 1,500–2,000 从头训练里程碑与残余句中截断）**：
   - 从头训练至 Step 1,500–2,000 时，模型首次在 18 句长上文阅读理解 `qa#405886` 上彻底摆脱首句复读，精准定位文末 3 句标准答案并在 `c3` 准确触发停止（`stop=0.832`）：
     - `c1`: `wht_cos=0.686, cos(GT)=0.412 | 这群人度` / `这群人饱`
     - `c2`: `wht_cos=0.981, cos(GT)=0.982 | 而是知道今天是江守、朝先宇、`
     - `c3`: `wht_cos=0.935, cos(GT)=0.648 | 静三个走出天化池的日子才刻意来迎接。`
   - 在 `qa#383582` 上同样精准在 `c3` 停止（`c1`: `wht_cos=0.988 | 目前东西决四个队主主练对轮换使用的态度：`，`c2`: `wht_cos=0.529, cos(GT)=-0.139 | 勇士科尔：敦`，`c3`: `wht_cos=0.970 | 手里这些人还能用的忙都赶跟再用用。`）。
   - **核心异常**：为什么 `wht_cos` 已达 `+0.529 ~ +0.961`，但物理空间 `cos(GT)` 却剧烈跌落至 `-0.139 ~ +0.464`，且在 `qa#405886 c1`（`这群人度`）、`qa#383582 c2`（`勇士科尔：敦`）和 `qa#653766`（`她将能制作0`）上发生 4~6 字截断？
2. **两大数学根因**：
   - **根因 A — `ThoughtFlowMatcher.sample()` 反归一化后强行除以 `z_out.std(dim=-1)` 注入 `<PAD>` 偏移**：
     - 在物理 HiPPO 空间中，`z_std[min/mean/max] = 0.078 / 0.338 / 6.381`（PCA Channel 0 的标准差高达 `6.381`，且均值 `z_mean` 承载平均 `<PAD>` 偏移；而其余 31 个词汇通道标准差仅 `~0.10`）。
     - 对于接近数据集平均长度（13~17 字）的子句，其白化空间 Channel 0 接近 $0$（即物理值接近 `z_mean`），因此真实物理子句向量 `z_gt` 的全维标准差天然为 `z_gt.std(dim=-1) ≈ 0.50 ~ 0.65`，**绝非 `1.0`**！
     - 旧版 `sample()` 在 `z_out = self.denormalize(z)`（`z * z_std + z_mean`）之后，又执行了 `z_out = z_out / z_out.std(dim=-1)`，相当于将整个物理向量连同 `z_mean` 强行乘以 $\frac{1}{0.55} \approx 1.82$ 倍：
       $$\tilde{z}_{\text{out}} = 1.82(z \cdot \sigma_z + \mu_z) = (1.82 z)\cdot \sigma_z + \underbrace{0.82 \mu_z}_{\text{巨幅 } \langle\text{PAD}\rangle \text{ 偏移污染！}}$$
       这不仅破坏了 `denormalize(normalize(z_gt)) == z_gt` 的恒等性（把精确真值扭曲并注入 $+0.82 \mu_z$ 的 `<PAD>` 能量），而且在自回归闭环滚动时经 `fm.normalize(z_out)` 反馈回右脑，直接把 `cos(GT)` 拉成负值并迫使左脑在第 4~5 字提前终止！
   - **根因 B — 白化空间中 PCA Channel 0（句长/`<EOS>` 包络通道）梯度权重被稀释至 $<3\%$**：
     - 在白化空间 `z_norm` 中，每个频段的 32 个通道方差均为 $1$，PCA Channel 0（`d=0`）仅占 $\frac{1}{32} = 3.125\%$ 的维度（在 `compute_spatial_slot_loss` 中因 `0.75 * lex_cos + 0.25 * full_cos` 更被稀释至 **$0.78\%$**）；
     - 但反归一化乘上 `z_std = 6.381` 后，PCA Channel 0 占据物理向量 `z_clause` **超过 $80\%$ 的能量**，并唯一决定左脑结晶器在 32 个槽位中何处放置 `<EOS>/<PAD>` 阶跃边界！
     - 此外，在 `predict_prior` 中若将 Channel 0 与第 $1..31$ 词汇通道混在同一个 32 维向量里做 `F.normalize` 极坐标插值，当词汇通道夹角较小（$\cos < 1$）时，归一化分母会无端放大 Channel 0 的幅度。
3. **根治方案（[`ThoughtFlowMatcher`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L560-L1005) & [`MultiStreamRightBrain.predict_prior`](file:///Users/kael/workbench/HollyShit/model/bicameral_right_brain.py#L1755-L1800)）**：
   - **废除 `sample()` 中破坏物理尺度的 `z_out / z_out.std(dim=-1)`**：
     - 在白化空间仅做温和的极值安全钳制 `z_rms.clamp(min=0.35, max=2.5)`（正常子句 100% 无损通过），随后直接返回 `self.denormalize(z)`，严格保证物理空间与白化空间的往返恒等性（实测各向异性 `z_gt.std=0.52` 下 `cos(GT)=1.0000, wht_cos=1.0000`）。
   - **径向解耦（$\frac{\partial}{\partial r_k} \equiv 0$）的 PCA Channel-0 句长包络显式监督**：
     - 在 `compute_polar_band_loss` 中，对去半径单位频段向量的第 0 号通道 `u_pred_0 = z_pred_b[..., 0] / r_pred` 显式施加方向 MSE + 余弦监督 `chan0_loss`；
     - 在 `compute_spatial_slot_loss` 中，使用径向解耦重构 `x_pred_iso = reconstruct_spatial_slots(from_bands((zp_b / rp) * rt.detach()))` 计算 `slot_cos_loss`、`slot_diff_cos_loss` 以及 32 槽位句长阶跃包络损失 `env_slot_loss = 1 - cos(x_pred_iso[..., 0], x_gt[..., 0])`，同时在 `compute_branch_loss` 赢家选择中加入 `0.5 * (1 - env_cos_k)`，在不产生任何高频半径塌缩的前提下精确锁定句尾 `<EOS>` 槽位。
   - **`predict_prior` 中 Channel-0 与词汇通道（`1..31`）分离极坐标插值**：
     - 对 `mh_b[..., :1]` 与 `lb_b[..., :1]` 沿 32 个频段（`dim=-2`）独立执行极坐标插值，对 `mh_b[..., 1:]` 与 `lb_b[..., 1:]` 沿频段内 31 个词汇通道（`dim=-1`）独立执行极坐标插值，彻底切断词汇夹角对句长包络通道的交叉干扰。
