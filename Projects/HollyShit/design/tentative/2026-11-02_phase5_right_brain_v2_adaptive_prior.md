---
date: 2026-11-02
status: tentative (approved by user, under implementation)
supersedes: Phase 5 Right-Brain #027 fixed-3-stream + single-point ThoughtFlowMatcher
---

# Phase 5 Right-Brain v2：1+N 动态多流 + 32 频带自适应先验锥 + K 路软竞争流匹配

## 0. 设计意图（用户确认）
- Mamba 输出的是**可容纳多种解释的隐状态**；Flow Matching 在该隐状态限定的范围内**随机尝试**，训练时只要有一路命中真值即算对，其余分支应保持"合法句向量"（意思不离谱、频谱饱满→左脑可结晶为通顺句）。
- 随机范围由输入决定：信息明确（无论来自主干流还是伴飞流）→ 语义层范围小、只剩语法差异；信息模糊 → 范围大。
- 流数量与身份不预设：1 条主干流 + N≥0 条同构伴飞流。

## 1. 句向量频带布局（来自 HiPPOOracleCUDA，已核对代码）
- `z_clause = reshape(z_sub (K=32 Legendre 阶, d_sub=32 PCA 通道))` → 第 b 频带 = 维度 `[b*32 : (b+1)*32]`。
- `ThoughtFlowMatcher.normalize` 是标量 mean/std，不破坏布局。
- **假设（需观测验证，不是定论）**：低阶 b < `sem_bands`(默认 6) 偏语义/内容（b=0 ≈ 字符袋），高阶偏字序/句式。`sem_bands` 必须是可配置参数，并按频带记录 σ 以验证。

## 2. 模块设计
### 2.1 1+N 动态多流 Mamba
- `main_stream`：ClauseMambaStream（4 层）沿话语子句序列推进 → `h0[t]`。
- `aux_stream`：共享 ClauseMambaStream（2 层），输入 `aux (B, N, S, D)` + `aux_valid (B, N, S)`，按 (B·N) 批处理，取每条流**最后一个有效位置**状态 `h_aux (B, N, D)`；`stream_valid = aux_valid.any(-1)`。N=0 或全无效 → 纯单流。
- 无流类型嵌入（流身份不预设）。
- 逐步动态门控：`g[t,i] = sigmoid(<q(h0[t]), k(h_aux_i)>/sqrt(d) + b)`（无效流置 0）。
- 正交合力：`F_aux[t] = Σ_i g[t,i] · OrthProj(v(h_aux_i), h0[t])`；`h[t] = h0[t] + tanh(α_aux)·F_aux[t]`，α_aux 初始化使 tanh≈0.1。
- 保留旧接口兼容：`z_knowledge_seq` / `z_goal_seq` 自动打包为 aux 流。

### 2.2 32 频带自适应先验（PriorHead）
- 输入 `[h0[t], F_aux[t], max_i g, Σ_i g]` → `μ (B,1024)`（归一化 z 空间）与 `σ_band (B,32)`，`σ = σ_min + (σ_max-σ_min)·sigmoid(·)`，默认 σ_min=0.05, σ_max=1.0，广播到 1024 维。
- **σ 的监督：频带异方差高斯 NLL（修正：此前口头推导"仅靠 65/35 自动校准 σ"不严谨——流网络可补偿任意起点，σ 梯度弱且不稳定）**：
  `L_prior = mean_b [ ||z1_b − μ_b||² / (2·d_sub·σ_b²) + log σ_b ]`
  最优解 `σ_b² = E[||z1_b − μ_b||²/d_sub | h]`：任何来源（主干或伴飞）的信息只要让 μ 变准，σ 就自动变小。
- 流匹配路径中使用 `μ.detach()`、`σ.detach()`（先验头只由 L_prior 训练，避免与竞争损失互相拉扯）。

### 2.3 ThoughtFlowMatcher v2
- **移除** `v_pred = (h_t − z_tau) + ...` 硬残差（它把 h_t 锁成单点均值）。
- 起点 `z0 = μ + σ⊙ε`；条件为 `h[t]`（AdaLN）。
- 训练：每个有效子句步并发 K 路（默认 4）：
  1. 盲推演端点：`x̂1^(k) = EulerODE_S(z0^(k), h)`，S=`train_ode_steps`(默认 3)，带梯度，无真值泄露。
  2. 胜者 `k* = argmin_k ||x̂1^(k) − z1||²`（选择不回传梯度）。
  3. **胜者 65%**：k* 噪声上的标准 CFM 速度 MSE（随机 τ）+ 端点 MSE + 0.25·(1−cos)。
  4. **其余 35%**（softmax 权重 w_k 按 −(低频马氏距离 + 能量偏差)，温度可调，detach）：
     - 低频 b<sem_bands：马氏距离 `||x̂1_b − z1_b||² / σ_b².detach()`（确定时偏离重罚，模糊时轻罚）+ 低频余弦；
     - 高频 b≥sem_bands：只约束每频带 L2 能量 `(||x̂1_b|| − ||z1_b||)²`，不约束方向（允许换句式，防模糊均值）。
  5. `L_flow = 0.65·L_win + 0.35·Σ w_k L_other^(k)`；`win_weight` 可配置。
- 推理：抽 1 次 ε，`z0 = μ + temperature·σ⊙ε`，积分 ODE（保留现有 denormalize 流程）。

### 2.4 停笔门控 stop_head
- `stop_head: Linear(1024,1)` on `h[t]`：预测"本步生成的目标子句是否为回答最后一句"。
- 标签来自数据集新增 `discourse_stop_mask`：仅当回答**未被截断**时最后一个有效回答子句为 1。BCE（pos_weight 平衡）。
- Rollout：生成子句后 `sigmoid(stop) > stop_threshold(0.5)` 即停，最少 1 句、最多 `num_rollout_clauses`。

### 2.5 KnowledgeSelector 归位（右脑之后、逐子句检索）
- 推理：每步以 `z_thought[t]`（+ goal 均值）为探针，从候选池动态选 top-M 子句作为当前子句的左脑吸引子 `w_attractors`。
- 训练：数据集新增逐子句伪标签 `cand_clause_rel (T, C)` = `cand_pos_mask × 字符 bigram 重叠率(目标子句, 候选子句)`（阈值化/软标签）；探针用真值目标子句向量 + 小高斯噪声。保留样本级损失（goal 探针）作为 0.5 权重辅助。

### 2.6 暴露偏差鲁棒化
- 主干输入 `z_in` 高频带（b≥sem_bands）以概率 p_band_jitter(0.3) 做**保模长随机正交旋转**（每频带 32 维内）。
- 计划采样：以 p_self（0→0.25 线性爬坡）把 `z_in[t≥1]` 替换为上一位置的自采样端点（no_grad 第一遍 teacher-forced 得到，第二遍混合输入），反归一化回 z_clause 空间。

### 2.7 训练期流掩码（Stream Dropout）
- 伴飞流构成：stream 0 = goal 子句序列；stream 1..C = 每条有效候选子句（K+ 与 K− 都放入，长度 1，由门控学会忽略干扰）。
- 每 batch 样本级：60% 全部伴飞流 / 20% 仅 goal / 20% N=0。

## 3. 可观测性（验证"确定性收放"的关键证据）
- 按流条件（full / goal_only / none）分组记录 `σ_sem`、`σ_syn` 均值，预期 `σ_sem(full) < σ_sem(goal) < σ_sem(none)`。
- 每频带 σ 曲线、L_prior、胜者分支分布、K 路低频两两距离（多样性）、stop 准确率、逐子句 selector 准确率、门控 g 分布（K+ vs K−）。

## 4. 已知风险
- 频带语义/语法划分是假设；若 σ 曲线不呈现分化，需调整 sem_bands 或改为可学习频带掩码。
- 逐子句 selector 标签是 bigram 重叠伪标签，对改写型回答召回偏低。
- 新架构与 #027 checkpoint 不兼容，需新 ckpt_prefix（`bicameral_right_brain_v2`），resume 兼容检查会自动跳过旧 ckpt。
- 训练 K 路 × S 步 ODE 使 flow 部分前向成本约 K·S 倍（MLP 很小，预计可接受，需记录显存）。
