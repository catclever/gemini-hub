# Sequence Flow Matcher (条件序列流匹配器)

## 1. 核心设计与数学抽象
Sequence Flow Matcher 是我们“三段式物理引擎”中的**微观轨迹引擎 (Motor Cortex / 右脑)**，旨在将单句（按标点切分，长度 $\le 128$）的 **2D 宏观句子向量 $Z_{\text{sent}} \in \mathbb{R}^{B \times 1024}$** 结合上下文/知识引力场 `k_attractors` 还原为微观的连续字符序列特征 $X_1 \in \mathbb{R}^{B \times L \times 1024}$。

* **信息瓶颈与 2D 句子向量 $Z_{\text{sent}} \in \mathbb{R}^{B \times 1024}$ (`HiPPOOracleCUDA`)**：
  - 若向 `FlowMatching1DUnet` 传入满秩 3D 序列 `(B, L, 1024)`，右脑会退化为 1:1 逐字传声筒并忽略 `OrthogonalAttractor` 与 1D 卷积，进而迫使 Phase 5 左脑承担不可能的非自回归逐字对齐任务。
  - 因此，`HiPPOOracleCUDA` 在提取句子势能时默认输出压缩后的 **2D 句子向量 $Z_{\text{sent}} \in \mathbb{R}^{B \times 1024}$**（`return_sequence=False`）：严格在 `valid_mask` 有效字符区间 $[0, L_{\text{eff}})$ 内计算多阶移位 Legendre 正交矩（将 16 阶时间多项式矩 $P_0(s) \dots P_{15}(s)$ 映射到 1024 维的子频带并编码有效长度占比 $\rho = L_{\text{eff}} / L$，归一化为单位方差 $\text{Std}(Z_{\text{sent}}) = 1.0$）。
  - 右脑 `AdaLN` 接收 2D 向量 `(B, 1024)` 并在序列维广播，迫使右脑必须动用 **位置编码 + 6 层膨胀 1D 卷积 + `OrthogonalAttractor(x, k_attractors)`** 从 `[Prompt, Knowledge]` 中主动吸附专有名词与实词并组织局部语法。
* **按标点切分单句数据链与去伪负例 (`GenericPairDataset`, `seq_len = 128`)**：
  - 训练与推理以自然标点子句/单句为单位（默认 `seq_len = 128`）；
  - 读取包含 `knowledge` 字段的数据集（如 `omni_knowledge_corpus.jsonl`）时，自动滤除与 `prompt/target` 无关的伪负例 $K^-$，将真实背景材料 $K^+$ 与 `prompt` 合并为完整的上下文引力场 `k_attractors`；
  - 对多句长回答按句末标点（`。！？；\n`）切分为递进的单句样本链（前句自动合入下一句的 `Context`）。
* **高比例开启 `k_attractors` 引力场 (`p_attractor = 0.90`)**：在 Phase 4 训练期间以 `90%` 的高概率开启 `use_knowledge_attractor=True`，确保右脑充分训练从 `k_attractors` 吸词完形的能力。

## 2. 核心文件
* **PyTorch 模型 (CUDA 训练用)**: [phase1_dit_cuda.py](file:///Users/kael/workbench/HollyShit/model/phase1_dit_cuda.py)
* **MLX 模型 (本地推理用)**: [phase1_dit.py](file:///Users/kael/workbench/HollyShit/model/phase1_dit.py)
* **训练脚本 (CUDA 训练用)**: [train_phase1_dit_cuda.py](file:///Users/kael/workbench/HollyShit/training/train_phase1_dit_cuda.py)
* **推理脚本 (MLX 本地推理)**: [phase1_dit_mlx.py](file:///Users/kael/workbench/HollyShit/infer/phase1_dit_mlx.py)
* **推理脚本 (CUDA 服务器推理)**: [phase1_dit_cuda.py](file:///Users/kael/workbench/HollyShit/infer/phase1_dit_cuda.py)

## 3. Euler 积分与反向投影
生成时采用 Euler ODE 积分：
$$X_{t+\Delta t} = X_t + v_\theta(X_t, t, Z_{macro}) \times \Delta t$$
在终点 $t=1$ 时，计算 $X_1$ 各位置向量与词表权重矩阵的乘积点积（Cosine Similarity），取 `argmax` 并依照 `<EOS>` 截断。

## 4. Common Gotchas & Caveats (常见错误与陷阱)
### Scale Mismatch 尺度失配危机
* **问题描述**: 训练 Flow Matcher 时，如果我们设定的目标 $X_1$ (如词嵌入) 的方差极小 (例如 `std = 0.032`)，而初始噪声 $X_0 \sim \mathcal{N}(0, 1)$，此时模型的目标速度场 $U_t = X_1 - X_0$ 将被 $X_0$ 绝对统治。网络会只学习如何消除噪声，导致 Loss 早期停滞，评估生成的文本完全是随机噪声（Char Accuracy 接近 0）。
* **解决方案**: 必须在训练输入前，利用词表的标准差算出一个放大因子 `scale_factor` 并作用于 $X_1$，使其方差被强行拉升至 1.0 左右。这个 `scale_factor` 需要被固化保存在 `training_args.json` 中。
* **推理与评估阶段注意**: 同样，在进行解码生成之前，从 $X_0$ 积分得到的 $X_{pred}$ 必须先**除以 `scale_factor`**，缩放回原始微小尺度，然后再与原始的 `tok_emb.weight` 进行点积解码。

## 5. Phase 4 HiPPO + 1D-Unet 显存与数值优化经验
* **正交吸引子 (Orthogonal Attractor) 显存峰值**:
  随着 Curriculum 调度中 `p_attractor` 从 0 逐步增加，网络从无条件流匹配平滑过渡到有条件的正交知识引力场。由于 6 层 Unet 中每一层都包含双向维度激活内积（`torch.bmm`）并保存激活图用于反向求导，若在 FP32 下使用大 Batch（如 128），反向图峰值会迅速挤满显存。
* **BF16 混合精度与段扩展 (Expandable Segments)**:
  1. 统一启用 `torch.amp.autocast(dtype=torch.bfloat16)`：激活图显存直接减半，并在支持原生 BF16 的现代 GPU（如 NVIDIA L4、A100、H100、RTX 4090）上获得 2~3 倍吞吐。
  2. 导入 PyTorch 前配置 `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`：彻底杜绝 ODE 积分测试（Batch=1）与训练（Batch=64）交替所产生的显存碎片化。
  3. 支持梯度累积 `--accum_steps`：将物理 batch 设为 64 或 32，配合累积步数实现等效大 batch，峰值显存降至 6GB 左右。
  4. 周期性评估与 Checkpoint 存档后执行 `torch.cuda.empty_cache()`，配合 `optimizer.zero_grad(set_to_none=True)` 释放梯度缓存。

