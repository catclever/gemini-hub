# Next-Gen Continuous-to-Text Translator Blueprint: Gated Residual Anchor & Decoupled Termination

## 1. 架构目标
融合旧版 `omni_translator`（点对点坐标识别强、罕见专有名词准确率高）与新版 `s32_clean`（零乱码尾巴、英文代码语法纠错好）的双重优势。

## 2. 核心架构设计 (解耦多头与门控残差)
- **主锚点头 (`fc_anchor`)**：
  - 输入：`x_norm = norm(x)` (1024D)
  - 职责：跳过所有时域卷积，实现 100% 纯坐标查表（Pure Coordinate Lookup）。
  - 损失：标准交叉熵 `loss_anchor` (`ignore_index=pad`)。
- **卷积残差头 (`fc_ctx` + 门控残差)**：
  - 输入：`conv(x)` (`Conv1d kernel_size=3`)
  - 职责：提供局部 3-gram 上下文先验，纠正易混淆字符/大小写（如 `inxex -> index`, `ranK -> rank`）。
  - 融合方式：`logits = logits_anchor + torch.tanh(gate) * logits_ctx`，其中可学习标量门控 `gate` 初始化为 `0.0`。
- **解耦终止头 (`fc_valid`)**：
  - 职责：二分类判断当前位置是否为有效字符（非 PAD）。
  - 损失：BCE 损失 `loss_valid`。
  - 解码机制：推理时取首个 `valid_prob < 0.5` 的位置直接截断，彻底抹除 `<eos>` 后的多余小尾巴，同时不干扰内容头的单字坐标分布。

## 3. 训练策略与防踩坑规则
1. **邻居扰动 (Neighbor Perturbation)**：
   - 保持中心字符向量 100% 干净，随机对左右邻居向量施加 15% 随机遮盖或微弱噪声，强迫模型仅在必要时参考上下文，杜绝“用邻居猜中心”的脑补倾向。
2. **混合语料 (MOSS + Omni)**：
   - 以 7:3 混合日常对话与包含代码、百科、新闻全域实体的语料，确保罕见专有名词覆盖度。
3. **旧权重热启动**：
   - `fc_anchor` 权重可使用已验证的 `omni_translator_step_8106` 进行热初始化，加速收敛。
