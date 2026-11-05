---
id: right_brain_flow_v2_residual_fix_036
title: 修复右脑 ThoughtFlowMatcher 线性桥泄漏、高频频带饥饿与 v1->v2 无缝热续训升级
status: completed
priority: high
tags:
- phase5
- right-brain
- flow-matching
- bugfix
session: bbb61e5a-3f2d-42a0-87e1-63d289f3e410
---

### 背景与根因
在完成 1024-D 逐维白化（#035）并训练至 Step 43,000~47,000 后，诊断发现：
- `PriorHead` ($\mu$) 在白化空间已学到强语义对齐（`qa#383582` 上 `wht_cos = +0.665 / +0.576`，物理 `raw_cos = +0.824 / +0.642`）；
- 但 `ThoughtFlowMatcher` 的 10 步 ODE 积分反而将 `wht_cos` 破坏至 `+0.180 / +0.543 / +0.523`，分支多样性坍缩（`BranchDiv = 0.85`，`pairwise cos = 0.9746`），左脑解码出现连字结巴（`力力力力力`、`人人人们`）。

数学根因：
1. **Oracle 线性桥目标泄漏 (`vel_loss`)**：$z_\tau = (1-\tau)z_0 + \tau z_1$ 在 $\tau > 0.5$ 时因暴露 $\tau z_1$ 诱使网络学成 $v^*(z_\tau, \tau) = \frac{2\tau - 1}{(1-\tau)^2 + \tau^2}(z_\tau - \mu)$，推理时无 $z_1$ 注入，导致 $\tau > 0.5$ 将残差噪声反向放大；
2. **$-14.5\text{ dB}$ 先验噪声淹没**：$\|\mu\| \approx 6$ 被 $\|\sigma\epsilon\| \approx 32$ 淹没，1024 维下 $K=4$ 随机高斯与目标残差最大余弦仅 $0.032$，导致多分支坍缩；
3. **高频 Legendre 频带 ($k=6..31$) 方向饥饿与无相能量虚胖**：缺乏逐频带方向余弦监督，高频展开系数缺失导致逆 Legendre 多项式在相邻字符槽位变化过慢而结巴；
4. **`sample()` 反白化前模长偏差**：`z` 标准差 $<1$ 时直接 `denormalize(z)` 导致 `z_mean` 权重被放大。

### 核心修复
- `model/bicameral_right_brain.py`:
  1. 在轨残差速度匹配 (`_euler_integrate_with_trajectory`)：对真实 Euler 轨迹点监督 $(1 - \tau_i) v_\theta(x_i^{\text{win}}, \tau_i, h_t) \approx z_1 - \text{sg}(x_i^{\text{win}})$，彻底根除 Oracle 线性桥泄漏；
  2. 全频带 32-Band 逐频带余弦监督：在 `PriorHead` 与 `ThoughtFlowMatcher` (`win_loss`) 中同步加入 `band_cos_loss`；
  3. 先验扰动缩放 `prior_noise_scale = 0.2` + 非胜出分支先验椭球锚定与两两排斥项 (`F.relu(sim - 0.25)`)；
  4. `sample()` 在白化空间先做单位标准差归一化再调用 `denormalize()`；
  5. 引入 `flow_version = 2` 缓冲区与状态字典升级钩子：加载旧版 v1 Checkpoint 时无缝保留已训练 4.7 万步的 `main_stream`、`prior_head`、`stop_head` 及白化统计量 `z_mean/z_std`，仅重置 `flow_matcher` MLP 权重。
- `training/train_phase5_right_brain_stage1.py`:
  - `resume_training` 自动检测 `_upgraded_from_v1`，自动归档旧版 v1 Checkpoint、重置优化器与余弦退火调度器至 Step 0 并立即保存 v2 `step_0`，无需用户改动命令行即可直接 `--continue` 续训。
