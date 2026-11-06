# Knowledge Base Graveyard & Failures / 踩坑记录与反思

## 1. CNN 解码器 (Translator) 训练教训与中心字去噪陷阱 (Deblur Trap)
- **教训背景**：
  在 `translator_moss_s32_deblur` 中，为了提升鲁棒性，尝试在训练时向中心字符向量注入 30% 噪声（`deblur_weight=0.5`）。
- **引发的故障与负面影响**：
  1. `Conv1d(kernel_size=3)` 学会了“不信任中心点坐标”，转而严重依赖左右邻居上下文和语料中的 n-gram 词频先验去强行“猜词”。
  2. 导致专有名词和特定搭配发生扭曲篡改（如“密尔沃基”被脑补成“密尔尔基/密尔奋基”，“开创运用于”被脑补成“开创使用于”）。
- **规则与警示**：
  - **严禁向中心字符坐标注入破坏性噪声**。若需要增强上下文纠错能力，应扰动**邻居节点（Neighbor Perturbation）**而不是中心节点，中心节点必须作为无偏的“坐标锚点”（Anchor）。
  - 不能直接将 `<PAD>` 的惩罚简单粗暴地与内容字符交叉熵混在一起，否则会导致模型为了预测 `<PAD>` 而过度参考邻居环境；应当使用解耦的独立终止头（`fc_valid`）进行截断。

## 2. 旧版 Omni Translator 的小尾巴问题 (No Pad Loss / Ignore Index)
- **故障现象**：
  在 `<eos>` 截断之后吐出大量乱码字符（如 `消研研研/专专专`）。
- **根因**：
  训练时设置了 `ignore_index=pad`，模型从未学习过在 `<eos>` 之后输出什么，导致推理时在空白区域自由发散。
- **解决方案**：
  解耦的终止判断头（Valid Gate / Termination Head），让内容预测头保持坐标纯洁性，由终止头负责平滑切断 `<eos>` 后的尾巴。

## 3. 右脑 `z_clause` 标量归一化陷阱：PCA 子空间通道 600 倍方差各向异性 (#035)
- **故障现象**：
  Phase 5 右脑在 Colab 训练至 Step 4000 时，`ThoughtCos` 长期卡在 `~0.60`，`win_loss` 卡在 `~1.10`，且即便 Eval 中 `cos(GT) = 0.976`，交由左脑解码出的文本仍然是完全随机的乱码（如 `国居怎居b应惯色哪惯学宜惯。的立感，`）。
- **物理根因**：
  `z_clause` 维度为 `(K=32 Legendre 频带, C=32 PCA 子空间通道) = 1024`。由于左脑 `subspace_proj` 是对字符向量作无中心化 PCA 正交投影：
  1. **通道 0 (`c=0`)** 对齐了字符向量的全局均值方向（本质上是 `1..N_valid` 的阶跃函数，只编码**子句字数长度**），其跨频带 RMS 高达 `5.45`（方差 `~29.74`），独占了整个 `z_clause` **93.0% 的总能量**！
  2. **通道 1..31 (`c=1..31`)** 才真正承载全部字词与语义身份，但其每通道 RMS 仅为 `0.10 ~ 0.75`（去均值后标准差 `0.03 ~ 0.14`，平均方差 `~0.045`），比通道 0 小 **600 倍**！
  3. 当 `ThoughtFlowMatcher` 使用标量 `z_mean=0.0, z_std=1.0` 时：
     - **梯度饥饿**：93% 的 MSE 梯度与 K=4 分支竞胜距离被通道 0（字数长度）垄断，通道 8..31 完全未学到；
     - **先验噪声淹没**：`AdaptivePriorHead` 每个频带输出一个共享标量 $\sigma_k \approx 0.60$，注入通道 1..31 的先验噪声方差（`0.36`）比真实语义信号方差（`0.03`）大 **10 倍**；
     - **高频抖动串扰**：在未白化空间对 `d_sub=32` 通道做随机正交旋转 `jitter_high_bands`，会将通道 0 的巨幅能量直接泼洒进通道 1..31。
- **规则与解决方案**：
  - **严禁对 `z_clause` 使用标量均值/标准差归一化或直接注入各向同性高斯噪声**。
  - 必须在 `ThoughtFlowMatcher` 与 `KnowledgeSelector` 中使用 **1024 维逐维白化（Per-Dimension Whitening，`z_mean: (1024,)`, `z_std: (1024,)`）**，使全部 32 个 PCA 通道与 32 个 Legendre 频带在右脑内部处于等方差 $\mathcal{N}(0, I_{1024})$ 流形；Mamba 输入（`_normalize_clause_input`）与 `jitter_high_bands` 正交旋转均在白化空间进行，采样输出先 `denormalize()` 还原至物理坐标后再执行逐样本 `std=1` 球面投影。

## 4. 右脑 `ThoughtFlowMatcher` Oracle 线性桥泄漏与高频频带饥饿导致字词结巴 (#036)
- **故障现象**：
  在修复 1024-D 逐维白化（#035）后训练至 Step 43,000~47,000 时，`PriorHead`（$\mu$）在 `qa#383582` 上的白化余弦已达 `wht_cos = +0.665 / +0.576`（物理余弦 `+0.824 / +0.642`），但经过 `ThoughtFlowMatcher` 10 步 ODE 采样后：
  1. `wht_cos` 反而暴跌至 `+0.180 / +0.543 / +0.523`（流匹配器反向破坏了 `PriorHead` 学到的语义均值）；
  2. 4 条分支坍缩为同一点（`BranchDiv` 从 `1.70` 跌至 `0.85`，采样多样性 `mean pairwise cos = 0.976`）；
  3. 左脑解码出的中文出现严重的相邻字连击结巴（如 `勇士》（练比力力力力力，`、`手人人人们能能的全搞用搞知力，`、`Gggggg`、`我我我我我`）。
- **四大数学根因**：
  1. **Oracle 线性桥目标泄漏与呼吸式扩噪（`vel_loss`）**：
     旧版 `vel_loss` 在教师强制线性插值桥 $z_\tau = (1-\tau)z_0 + \tau z_1$ 上拟合 $v_{\text{target}} = z_1 - z_0 = (z_1 - \mu) - \sigma\epsilon$。由于 $\text{Var}(z_0 - \mu) \approx \text{Var}(z_1 - \mu)$ 且 $\mathbb{E}[z_1 - \mu \mid h_t] = 0$，给定 $(z_\tau, \tau)$ 的贝叶斯最优线性估计为 $v^*(z_\tau, \tau) = \frac{2\tau - 1}{(1-\tau)^2 + \tau^2}(z_\tau - \mu)$：在 $\tau < 0.5$ 时向 $\mu$ 收缩去噪，而在 $\tau > 0.5$ 时因为训练态 $z_\tau$ 含有 $\tau z_1$ 泄漏而把 $(z_\tau - \mu)$ **向外反向放大**！推理时 $z(\tau)$ 不含真值 $z_1$，导致 $\tau > 0.5$ 的积分步把残余噪声重新放大，10 步积分严重劣化。
  2. **$-14.5\text{ dB}$ 先验噪声淹没与 1024 维 Best-of-4 坍缩**：
     旧版 $z_0 = \mu + 1.0 \cdot \sigma\epsilon$ 中 $\|\mu\| \approx 6.0$，而 $\|\sigma\epsilon\| \approx 32.0$。在 $D=1024$ 维空间中，$K=4$ 个随机高斯向量与真实残差的最大期望余弦仅为 $\frac{1.029}{\sqrt{1024}} = 0.032$（$99.9\%$ 能量为正交噪声），迫使网络将对 $\epsilon$ 的敏感度压死到 $\alpha^* = 0.032$，导致多分支彻底坍缩（理论两两余弦 $\approx 0.973$，与实测 `0.9746` 完全吻合）。
  3. **高频 Legendre 频带（$k=6..31$）方向饥饿与无相能量虚胖**：
     `PriorHead` 仅受异方差高斯 NLL 监督，高频段 $\sigma_k \approx 0.95$ 导致梯度比低频小 5 倍且无方向余弦约束；而 `other_loss` 的 `energy = (x_hi_norm - z_hi_norm)^2` 强迫落选分支向高频 $k=6..31$ 注入无方向监督的随机模长。当高频展开系数缺失或相位混乱时，逆 Legendre 展开 $x(l) = \sum_k z_k P_k(l)$ 退化为低阶慢变多项式，相邻字符槽位 $l, l+1$ 坐标几乎重合，直接引发左脑解码结巴（`力力力力力`、`人人人们`）。
  4. **`sample()` 反白化前的模长偏差**：
     当白化空间预测向量 `z` 的标准差 $< 1.0$ 时，直接执行 `z * z_std + z_mean` 会使 `z_mean` 权重被放大 $1/\text{std}(z)$ 倍，向全局平均句偏移。
- **规则与解决方案**：
  - **严禁在 `z0` 与 `z1` 方差同阶时使用暴露 $\tau z_1$ 的线性桥 `z_tau = (1-tau)*z0 + tau*z1` 训练流匹配速度场**：必须使用在轨轨迹残差速度匹配（On-Policy Residual Velocity Matching），对真实 Euler 轨迹点 $x_i^{\text{win}}$ 监督 $(1 - \tau_i) v_\theta(x_i^{\text{win}}, \tau_i, h_t) \approx z_1 - \text{sg}(x_i^{\text{win}})$。
  - **全频带等权方向监督**：在 `PriorHead` 与 `ThoughtFlowMatcher` 的 `win_loss` 中必须加入全部 32 个 Legendre 频带的逐频带余弦损失 `band_cos_loss = 1 - mean_b cos(z_b, z1_b)`，消除高频字序与相邻字跳变信号的饥饿。
  - **先验锥缩放与球面反白化**：先验扰动使用 `prior_noise_scale = 0.2`（保持先验信噪比 $> 0\text{ dB}$），并在 `sample()` 中先将白化空间向量归一化至单位标准差，再调用 `denormalize()`。

## 5. 纯频域 Legendre 损失的“两端聚光、句中相消”模糊与频带模长均衡冲突 (#037)
- **故障现象**：
  在修复 Flow-v2（#036）训练至 Step 13,000 时，`qa#383582` 的低频 `Band 0..5` 余弦已达 `0.88 ~ 0.92`，整句物理余弦达 `0.85 ~ 0.91`，但解码文本呈现出高度规律的**“句首 4~8 个字精准命中、句中后段变成 3 字连击平顶平台”**（如 `目前东西四四四友来孩授授授话话话的话话，`、`弄里这些人还能你的吞提真明me.`）。
- **物理根因**：
  1. **Legendre 基函数的边界集中与内部相消干涉**：
     高阶 Legendre 多项式 $P_k(t)$ 在区间两端 $t = \pm 1$（对应句首 `slot 0..3` 与句尾标点 `slot 31`）振幅恒为 $|P_k(\pm 1)| = 1$ 且相位同相；而在句子中段 $t = \cos\theta \in (-0.7, +0.7)$（对应 `slot 4..25`），渐近振幅按 $\sqrt{\frac{2}{\pi k \sin\theta}}$ 衰减（仅为两端的 $\frac{1}{5} \sim \frac{1}{7}$）且高速正负振荡。仅在频域独立监督 32 个频段（`band_cos_loss`）时，模型只需对齐两端 `slot 0..3` 与 `<pad>` 边界就能拿到 `~0.65` 的高频余弦奖励；而句中 `slot 4..25` 缺乏跨频段相位锁定（Cross-Band Phase Locking），微小的频段间相位误差在句中发生正负相消干涉，只剩下 4~5 阶低频慢变多项式包络（每 3~4 个槽位形成一个平顶平台，解码为 `四四四`、`授授授`）。
  2. **禁忌：严禁使用人为的“逐频带模长均衡（Per-Band Norm Equalization）”**：
     逆 Legendre 空间还原 $X(l) = \sum_{k=0}^{31} z_k P_k(t_l)$ 是 32 个频段的严格线性相干叠加。单句中哪些槽位发生字跳变、哪些槽位（如 `<eos>` 后的 `<PAD>` 区）相消归零，严格依赖于 32 个频段之间真实的**相对模长比例（频谱包络）**。若人为将每个频段强行拉平为相同模长，会直接破坏 $P^{-1}$ 线性叠加的相消与相长关系，并将相位尚未对齐的高频噪声强行放大为全句振铃。
- **规则与解决方案**：
  - **严禁人为篡改单句内各频段的相对模长比例**。
  - **时频双域联合监督（`compute_spatial_slot_loss`）**：通过与左乘逆 Legendre 正交矩阵 $B^\top$ 严格可交换的右乘逐通道 RMS 缩放 $D_{\text{chan}}^{-1}$ 还原 32 个空间字符槽位 $X_{\text{slot}} = B^\top (Z_{\text{phys}} D_{\text{chan}}^{-1})$，在有效字符槽位上直接施加**逐槽位词汇余弦损失（`slot_cos_loss`）**与**相邻槽位一阶跳变差分损失（`slot_diff_loss` on $\Delta X(l) = X(l+1) - X(l)$）**，用 $\Delta P_k(t) \propto k P_k(t)$ 的天然高通特性抵消句中 $1/\sqrt{k}$ 衰减并消灭多字平顶平台。

## 6. 笛卡尔欧氏 MSE 的高频 $\cos\theta_k$ 模长塌缩定理、Mamba 因果回看瓶颈与无吸引子解码失真 (#038)
- **故障现象**：
  在基于 #037 从零重训至 Step 5,560 时，日志呈现三大反常现象：
  1. 尽管没有任何人为频带模长均衡，句中后段与句尾依然出现多字连击平顶平台（如 `四四`、`给给给`、`话话`、`士士`、`很很`）；
  2. 长上文（15~18 个子句）问答样本（如 `qa#405886`、`qa#653766`、`qa#383582` 的 `c1`）由于问题出现在全文最后一句，单向量 Mamba 无法回看前文第 1~3 句，导致 `c1` 偏离目标且无法顺延接力 `c2 -> c3`；
  3. 当 `qa#383582` 的 `c3`（真值：`手里能用的牌已经很少了。`）预测的 `cos(GT) = 0.917, wht_cos = 0.825` 已极高时，左脑解码却输出近义音形近似字（`办事这些人还希供的安尽很很悔责。`）。
- **物理与数学根因**：
  1. **笛卡尔欧氏 MSE 的高频 $\cos\theta_k$ 模长塌缩定理（High-Frequency Radial Shrinkage Theorem）**：
     对任意频段 $k \in \{0,\dots,31\}$，设真实频段向量为 $z_{1,k}$，预测向量为 $x_{1,k} = r_k \hat{u}_k$，两者夹角余弦为 $\cos\theta_k = \langle \hat{u}_k, \hat{z}_{1,k}\rangle$。笛卡尔欧氏平方误差恒等展开为：
     $$\|x_{1,k} - z_{1,k}\|^2 = (r_k - \|z_{1,k}\|\cos\theta_k)^2 + \|z_{1,k}\|^2(1 - \cos^2\theta_k)$$
     求偏导 $\frac{\partial}{\partial r_k}\|x_{1,k} - z_{1,k}\|^2 = 0$ 得唯一径向极小值点：
     $$r_k^* = \|z_{1,k}\| \cdot \cos\theta_k$$
     当低频 $k=0..3$ 方向较准（$\cos\theta_k \approx 0.85$）而高频 $k=10..31$ 方向尚有误差（$\cos\theta_k \approx 0.30$）时，所有包含笛卡尔欧氏差的项（`vel_loss`、`end_mse`、`band_gaussian_nll` 对 $\mu$ 的二次项、以及空间一阶差分的欧氏项 $\|\Delta X_{\text{pred}} - \Delta X_{\text{gt}}\|^2$）都会在数学上强制把高频频段模长压扁到真实模长的 $30\%$（能量仅剩 $\cos^2\theta_k \approx 9\%$）！这就构成了一个天然的低通滤波器，抹平了相邻槽位间的一阶跳变步长 $\|\Delta X(l)\|$，制造出 `四四`、`给给给` 的平顶结巴。
  2. **单向量 Mamba 的长程因果回看瓶颈**：
     `omni_knowledge_corpus.jsonl` 的阅读理解样本将问题放在 15~18 个背景子句的末尾。纯 4 层 Mamba 在读前 14 句时不知问题为何，无法在问题到达的第 $t$ 步动态回看前文任意子句 $j \in \{0,\dots,t-1\}$，也无法在多句回答时沿着前文轨迹执行因果顺延接力（$\tau \le t-2 \implies j = \tau + 1 \le t-1$）。
  3. **Phase 5 Stage-1 评估缺失上下文吸引子（`--eval_attractors none`）**：
     左脑结晶器在 Phase 4 训练时以 `attractor_prob = 0.90` 挂载 `OrthogonalAttractor`，依靠上下文候选字吸引子将 $32$ 维 PCA 近似坐标吸附回精确的 $1024$ 维字符嵌入；裸跑 `--eval_attractors none` 会使 $32$ 维截断误差直接暴露为近义字漂移。
- **规则与解决方案**：
  - **极坐标径向—角向解耦监督（`compute_polar_band_loss` + `slot_diff_norm_loss` + `mu_for_nll` 正交解耦）**：
    - 严禁让笛卡尔欧氏 MSE 主导高频频段模长或空间跳变差分；必须将每频段误差拆解为仅依赖径向模长的 `band_norm_loss`（极小值恒为 $r_k^* = \|z_{1,k}\|$，与 $\cos\theta_k$ 完全解耦）与仅依赖单位方向角向的 `band_dir_loss`。
    - 在 `PriorHead` 的高斯 NLL 中，必须通过停梯度的正交投影 `mu_for_nll = mu_b * (r_z1 * cos_mu / r_mu).detach()` 校准方差 $\sigma_k$，严禁让 `band_gaussian_nll` 的欧氏分子把 $\mu$ 的高频模长压扁为 $\cos\theta_k$。
    - 在 `compute_spatial_slot_loss` 中，将一阶跳变差分拆解为方向项 `slot_diff_cos_loss`、幅度项 `slot_diff_norm_loss` 与防驻留铰链惩罚 `anti_stag`。
  - **因果上下文子句回看与顺延接力（`CausalContextLookback`）**：
    - 仅在严格前序子句 $j \le t - 1$（配合长度不变空槽 `sink_logit + log(n_prev)`）上执行因果多头回看，禁止对角线 $j = t$ 自拷贝当前输入子句；当 $z_{\text{in}}[t]$ 命中前序子句 $\tau \le t - 2$ 时，通过带阈值 `F.relu(sim - 0.35) / 0.65` 的顺延偏置激活其后继子句 $j = \tau + 1 \le t - 1$ 并抑制对 $\tau$ 的原地复读。
    - **严禁跨注意力头切分频段或对不同长度子句做软加权拷贝（Straight-Through Top-1 整句拷贝）**：语料首句通常为 5 字短标题（如 `背景资料：`、`叙事片段：`，第 5 槽位为 `<EOS>`，第 6..31 槽位为 `<PAD>`）。由于 HiPPO Legendre 变换满足严格线性性，一旦对多个不同长度的上下文子句进行软注意力平均（$\sum_j \alpha_j z_j$），所有短子句在第 5..31 槽位完全相同的 `<PAD>`/`<EOS>` 嵌入会相长叠加，直接把 15 字长句在第 5 个槽位截断（制造出 `勇士科尔：D`、`目前东端：定`、`时间一菠三<三下，`）！必须采用 `0.5 * mean + 0.5 * amax` 聚合多头 Logits，并通过 **Straight-Through Top-1（前向 `one_hot` 拷贝单一完整子句，反向传播 `probs_norm` 稠密梯度）**生成 `z_copy_unit`。
    - **极坐标频段插值与 `mu_head` 独立极坐标监督**：在 `predict_prior` 中必须按极坐标频段（线性插值半径 `r_blend` + 单位化插值方向 `u_blend`）融合 `mu_head` 与 `z_lookback`，并在 `compute_loss` 中对 `mu_head` 单独施加 `0.30 * (head_polar_loss + head_slot_loss)` 监督，防止 `PriorHead` 在抽取式 QA 上偷懒依赖 `z_lookback` 而在非抽取式数学推理题（`qa#653766`）上退化为 3 字残桩。
  - **Stage-1 评估默认开启自动上下文吸引子（`--eval_attractors auto`）与防自反馈污染 (#039)**：
    - `_ctx_last(ctx)` 必须完整保留 `"z_lookback"` 与 `"gate_lb"`，严禁在评估首句 `c1` 与 Diversity 采样时剥离回看状态；
    - 评估闭环滚动时，候选吸引子池 `pool_z / pool_w` 必须严格锁定为真实上文子句 `0 .. ctx_len - 1`，**严禁将模型自身刚生成的预测子句 `z_next / ids[0]` 追加进吸引子池**（否则 `c2..c8` 会以 $\cos \approx 0.99$ 命中 `c1` 的自生成噪声并陷入自激复读死循环）。
  - **严禁对反归一化后的物理子句向量执行 `z_out / z_out.std(dim=-1)` 强行缩放 & 必须显式监督 PCA Channel-0 句长包络 (#039)**：
    - 物理 HiPPO 空间具有高达 60 倍的标准差各向异性（PCA Channel 0 的 `z_std = 6.381` 且 `z_mean` 非零，而第 1..31 词汇通道 `z_std ≈ 0.10`）；中等长度子句（13~17 字）在物理空间的真实全维标准差天然为 `z_gt.std(dim=-1) ≈ 0.55`。若在 `self.denormalize(z)` 之后除以 `z_out.std(dim=-1)`，会将 `self.z_mean`（Channel 0 上的 `<PAD>` 偏移）连带放大 $\approx 1.82$ 倍，注入 $+0.82 \mu_z$ 的虚假 `<PAD>` 能量，直接导致物理空间 `cos(GT)` 跌至负值并迫使左脑在第 4~5 字提前截断（如 `这群人度`、`勇士科尔：敦`）！
    - 在 `compute_polar_band_loss`、`compute_spatial_slot_loss` 与 `compute_branch_loss` 中，必须对径向解耦后的单位频段向量 `u_pred_b = z_pred_b / r_pred` 显式监督第 0 号通道（`chan0_loss` 与 32 槽位阶跃包络 `env_slot_loss`），并在 `predict_prior` 中将 Channel 0（`[..., :1]`）与词汇通道（`[..., 1:]`）分离做极坐标插值，严禁跨频段角度余弦直接对频段半径 $r_k$ 求导或让词汇夹角污染句长包络。
