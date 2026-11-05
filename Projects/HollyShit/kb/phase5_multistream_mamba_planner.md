# Phase 5 Multi-Stream Mamba Planner & Time-Warped Legendre Architecture

## 1. 核心物理图像与双脑分形对称 (Fractal Dual-Brain Symmetry)
Phase 5 旨在在**完全冻结** Phase 1 视网膜 (`TinyCharEncoderCUDA`)、Phase 4 右脑流匹配引擎 (`FlowMatching1DUnet`) 与解码透镜 (`ContinuousToTextTranslatorCUDA`) 的前提下，训练左脑规划器 (`MultiStreamMambaPlanner`) 从多路输入（对话上下文 `Context` + 多条外部知识流 `Knowledge[1..M]` + 全局控制场）直接预测目标回答的 **3D 动态因果势能轨迹 $\hat{H}_{\text{potential}} \in \mathbb{R}^{B \times L \times 1024}$**。

多路知识注入在左右脑之间形成严格的**分形对称**：
1. **左脑宏观层 (`MultiStreamMambaPlanner`)**：在推演未来 $K=32$ 个宏观构思节拍时，通过**正交内积共振 (`ReLU(X_beat @ K^T / sqrt(D))`) + 正交场叠加 (`OrthogonalFieldSuperposition`)** 按需吸取多路知识的段落级语义走向，规划出预留好语法槽位的 3D 势能曲线 $\hat{H}_{\text{potential}}$。
2. **右脑微观层 (`FlowMatching1DUnet`)**：在 10 步 Euler ODE 积分渲染时，将归一化后的 `[X_Context, X_K1, ..., X_KM]` 沿序列维拼接作为 `k_attractors`，利用内置的 `OrthogonalAttractor` 将专有名词、数字与精确事实吸附到轨迹上。

## 2. 弹性时间轴与详略控制机制 (Elastic Time-Warping & Horizon Control)
为解决固定画布长度 $L=512$ 下短句节拍浪费、局部详略死板及一问多解长度均值坍缩三大问题，采用**「全局有效篇幅控制 $\hat{\rho}$ + 局部节拍笔墨权重 $\Delta s_k$」**双层弹性时间轴：
1. **无 `<PAD>` 间隔的未来 32 节拍推演**：
   - 对 `x_context` 屏蔽 `<PAD>` 后提取有效状态，并在每个样本的真实有效末尾之后紧接 $K=32$ 个未来节拍探针 `beat_queries`，在每一层通过正交内积共振注入多路知识场 $X_K$，输出 32 个节拍控制向量 $C_{\text{pred}} \in \mathbb{R}^{B \times 32 \times 1024}$。
2. **局部快慢镜头 (`pacing_head`)**：
   - 每个节拍 $k \in \{1..32\}$ 预测正标量笔墨跨度 $\Delta s_k = \text{Softplus}(w_s^T C_k) + \epsilon$。$\Delta s_k$ 越大，该节拍在画布上占据的字数跨度越宽（详写）；$\Delta s_k$ 越小，跨度越窄（略写）。
3. **全局详略跨度 (`length_head` & `rho_override`)**：
   - 预测有效正文占总画布的比例 $\hat{\rho} \in (0.04, 0.99)$（有效长度 $L_{\text{eff}} = \hat{\rho} \cdot L$）。
   - **FP32 软限幅防饱和与梯度隔离**：`length_head` 强制在 `float32`（禁用 `bfloat16` autocast）下运行，采用直通泄漏软限幅 `soft_logit = 4.5 * tanh(z / 4.5)`（避免 `bfloat16` 下 $\sigma(z)$ 舍入为 `1.0` 导致梯度归零），且在未传入 `rho_override` 时对 `rho_used = rho_pred.detach()` 进行梯度截断，防止 `loss_potential` 通过 $L_{\text{eff}} = 512 \cdot \hat{\rho}$ 劫持长度预测头；同时 `h_summary_clean` 在注入 `verbosity_cond` 之前提取，彻底杜绝训练期提示泄露。
4. **任意画布长度 $L$ 的双基底 Legendre/Gaussian + 正交 Nyquist 槽位调制与两阶段闭环流匹配 (`encode_macro` + `forward_canvas(X_t, t)`)**：
   - **第一阶段（宏观骨架推演 `encode_macro`，每轮对话仅执行 1 次）**：32 个节拍 100% 分布在有效正文区间 $[0, L_{\text{eff}}]$ 内，分别经 `leg_proj` 与 `gauss_proj` 映射宏观骨架 $H_{\text{macro}}(t)$，并结合高频正交 Nyquist 槽位载波 `_get_slot_carrier`（满足相邻位置内积 $\langle \text{slot}[t], \text{slot}[t+1] \rangle \equiv 0$）生成宏观参考画布 $H_{\text{canvas\_macro}}$。
   - **第二阶段（微观因果流画布 `forward_canvas(X_t, t, macro_state)`，自条件防偷懒与球面方向保持）**：
     - **消除 Teacher-Forced 伪自回归捷径（Self-Conditioned Prefix）**：在训练期若直接将含真实答案的 $X_t = t H_{\text{target}} + (1-t) X_0$ 右移作为 `x_t_prev`，模型会利用相邻字符的 `HiPPO` 强相关性走捷径（单步 MSE 虚低至 `0.17`，而 Stage 1 `Macro MSE` 停滞在 `0.64`，导致 10 步并行 ODE 推理因缺乏真值前缀而坍缩为原点附近静止字符 `' '` 与 `'έ'`）。因此在训练期构造 `x_t_prev` 时，采用 Stage 1 自身预测 `h_macro_potential.detach()` 构造自条件轨迹 $X_t^{\text{self}} = t \cdot \text{stop\_grad}(H_{\text{macro}}) + (1-t) X_0$，使训练期与 10 步 Euler ODE 推理期的画布前缀分布 100% 对齐，彻底斩断逐字自回归偷懒捷径。
     - **温和时间步加权 ($w_{\text{pot}}(t) = 0.5 + t$) 与球面余弦防坍缩损失 (`loss_cos`)**：将势能时间权重由极端的 $3t^2$（81:1 饿死 $t < 0.3$ 起步段）拉平为温和线性权重 $w_{\text{pot}}(t) = 0.5 + t$（均值 `1.0`），将 `loss_macro` 权重提升至 `0.75`，并在有效字符位置引入球面余弦方向与模长保持损失 $\mathcal{L}_{\text{cos}} = 1 - \cos(\hat{H}_{\text{potential}}, H_{\text{target}})$，防止 L2 均值回归向球心原点 $\vec{0}$（对应解码器 `' '` / `'έ'` 死区）坍缩；同时 `per_sample_pot` 严格仅在 `target_mask` 有效字符上归一化（剔除 `<PAD>` 分母稀释）。
     - **宏观 + 画布双阶低秩复制指针头 (`CopyPointerHead`)**：
       - 在宏观展开后与画布精修层均配备低秩复制指针头 **`CopyPointerHead`**（低秩寻址维度 $d_{\text{ptr}} = 64$，Key 端带 `DWConv1d(k=3)` 局部 n-gram 上下文感知 + 可学习 `sink_logit` 空槽 + 零参数 Identity Value 直接搬运归一化知识流 token 向量），使 $t=0$ 起步阶段与后续 ODE 步均能直接从知识流搬运实体、年份与关键事实。

## 3. 通用主干训练语料规范（纯阅读理解 `cmrc2018`/`dureader` + 带材料问答 `grounded_instruct`）
- **聚焦通用主干、剥离盲猜噪声（专项领域留给后续 Post-Training）**：
  - 废除原先对无背景纯长文（维基词条、知乎回答、网文小说）做“切前句当知识、盲猜后三句”的伪知识构造（该做法导致后文事实无据可依，引发人为的一句多解均值坍缩）；
  - **主干训练核心配方**：专注于 100% 有背景事实支撑的自然语言阅读理解与带材料指令问答：
    1. **精准事实阅读理解（`encyclopedia_rag` 升级为 `cmrc2018` + `dureader_robust` + 少量英文 `squad`）**：以阅读理解原文段落切分出的自然子句作为 `Knowledge` ($K^+$)，以具体提问 `question` 作为 `Prompt`，以基于原文的完整回答作为 `Target`（对过短的词组型抽取答案，自动提取原文中含该答案的完整结论分句或拼合问题主干补全为通顺句子）；
    2. **完整表达带材料问答（`grounded_instruct`：`Belle` + `Alpaca-GPT4-CN` 带非空 `input` 子集）**：以 `input` 材料作为 `Knowledge` ($K^+$)，`instruction` 作为 `Prompt`，`output` 作为 `Target`；
  - **放宽阅读理解子串包含限制**：在 `is_non_cheating_knowledge(k, target)` 中，允许 `target`（如阅读理解的回答短句）作为子串出现在更长的参考背景段落 `k` 中（只要 `k_clean != tgt_clean` 且背景子句包含额外上下文信息），确保阅读理解黄金证据句不被误杀。
- **训练调度与多维可观测性**：
  - 学习率采用线性 Warmup + Cosine Decay 调度（注册进 `Checkpointer` 支持断点续训）；
  - 日志输出 EMA 平滑损失、按领域（6 大 domain）分列统计、按流时间 $t \in \{[0,0.3), [0.3,0.7), [0.7,1.0]\}$ 分桶统计 `loss_potential` 以及复制指针非空激活率 `copy_prob = 1 - p_sink`，并使用固定跨领域评测样本进行 ODE 生成对比。
- **Phase 5（开卷路由）与 Phase 6（闭卷内化自蒸馏）分工**：
  - Phase 5 专注于训练多路外部知识的正交共振筛选、低秩指针精确复制与详略控制；
  - 若需将特定核心知识内化进模型参数，可在下一阶段采用「开卷 $\to$ 闭卷 势能自蒸馏」：用带外部知识的 $\text{Mamba}_{\text{teacher}}(C, K_{\text{gold}})$ 监督无外部知识的 $\text{Mamba}_{\text{student}}(C, \emptyset)$。
