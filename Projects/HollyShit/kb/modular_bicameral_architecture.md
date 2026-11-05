# 模块化双脑协同架构设计文档 (Modular Bicameral Architecture Blueprint)

> **核心设计哲学**：锚定两端已冻结的「感官编码器 (`TinyCharEncoderCUDA`)」与「纯翻译声带 (`ContinuousToTextTranslatorCUDA`)」，将中间系统解耦为 **可按任务重训/微调的「右脑认知群（Mamba + Flow Matching 成对协同 + 独立知识采择器）」** 与 **训透一次即永久固定的「全能左脑结晶器（统一支持自然语言与代码生成）」**。

---

## 一、 架构全景与两端固定基石

整个系统由 **3 个永久固定的通用基座** 与 **2 个可按任务联合训练/重组的认知组件** 构成。所有组件之间统一通过冻结 [`TinyCharEncoderCUDA`](file:///Users/kael/workbench/HollyShit/model/phase1_charencoder_cuda.py) 的 **`1024` 维标准流形空间** 进行通信：

1. **输入端编码器 ([`TinyCharEncoderCUDA`](file:///Users/kael/workbench/HollyShit/model/phase1_charencoder_cuda.py)，Frozen)**：
   - 将一切离散文本（用户提问、多句历史、外部百科知识、API 文档、代码上下文）映射到统一的 `1024` 维连续字符流形 `(B, L, 1024)`。
2. **输出端翻译器 ([`ContinuousToTextTranslatorCUDA`](file:///Users/kael/workbench/HollyShit/model/continuous_translator_cuda.py)，Frozen)**：
   - 纯粹的 `Conv1d(kernel_size=3) + LayerNorm + Linear` 字典翻译器，不承担任何推理任务，吃入对齐到每个字符位置的 $\hat{X} \in \mathbb{R}^{B \times L \times 1024}$ 后 1 步直接翻译成汉字或代码。

---

## 二、 右脑设计：Mamba 与 Flow Matching 的成对协同与多流演进

右脑负责 **「职责 1：从上一句向下一句的长程推理」** 与 **「职责 2：一句多解的生成建模」**。

1. **完整多流框架 + 单流起步训练（Multi-Stream Framework, Single-Stream First Curriculum）**：
   - 代码框架一次性搭建完整的三流 Mamba（**Stream 1 主干对话流** + **Stream 2 知识伴飞流** + **Stream 3 全局目标/AST 大纲流**），其中伴飞流与目标流通过**零初始化正交门控（$\alpha_k=0, \alpha_g=0$）**汇入主干流，再驱动 `ThoughtFlowMatcher`；
   - **训练策略**：第一阶段先仅开启单流（Stream 1 + Flow Matcher）快速训稳跨句推进与一句多解；第二阶段再解锁 Stream 2 & 3（因门控初始为 0，与单流模型零抖动无缝衔接）。
2. **标点自然切分粒度（Punctuation-Driven Clause Granularity）**：
   - 摒弃机械的定长 4～6 字硬切（避免劈开完整词汇或代码标识符），改为**按标点符号（含逗号 `，`、顿号 `、`**、分号 `；`、冒号 `：`、句号 `。！？`、括号与代码分隔符**）切分为自然短分句**（每个标点短分句长度约 $6 \sim 20$ 字）；
   - 每个变长标点短分句利用 [`HiPPOOracle`](file:///Users/kael/workbench/HollyShit/model/hippo_oracle.py)（$K=16$ 阶正交多项式）进行弹性长度打包与解包，既保证了语义完整性，又使每个分句内部阶数与字数达到 $\approx 1:1$ 的满秩清晰度。

---

## 三、 独立模块：知识与符号采择器 (`KnowledgeSelector`)

- 挂载在右脑输出端之后：以右脑刚生成的本句词块意图 $Z_{\text{thought}}$ 为检索探针，同时扫描 **外部知识/API 文档库 $K$** 与 **上文已生成文本/代码符号池 $S_{\le t}$**（含前文定义的变量名、函数名），筛出本句所需的 **活跃原始字符编码池 $A_{\text{active}} \in \mathbb{R}^{B \times L_{\text{act}} \times 1024}$**。
- 可随右脑针对不同任务联合微调或重训。

---

## 四、 全能且固定的左脑：通用语言与代码结晶器 (`LeftBrainCrystallizer`)

- 训透一次后**永久冻结**，同时支持自然语言成句与严格代码编写：
  1. **词块级满秩解包器 (`ChunkUnpacker`)**：将 $M$ 个词块向量（每词块 4～6 字，自由度 1:1 满秩）无损展开为草稿字符序列；
  2. **全句结构与语法协调层 (`StructuralSyntaxWeaver`)**：全局协调中文主谓宾句式与代码括号 `()/{}` 闭合、缩进对齐；
  3. **连续片段原字嫁接器 (`ExactSpanPointer`)**：通过锐化跨注意力指针，直接从 $A_{\text{active}}$ 中整段吸取专有名词、变量名、API 名的 `TinyBERT` 原始字符编码，合成精准的 $\hat{X} \in \mathbb{R}^{B \times L \times 1024}$ 交给底部 CNN 翻译器。


---

## 5. Stage 2 & Stage 3 右脑训练与双脑闭环推演管线 (`#027`)

- **多子句链与正负知识池数据集**：[`BicameralClauseChainDataset`](file:///Users/kael/workbench/HollyShit/training/data/knowledge_dataset.py#L1018-L1493)
  - `w_goal`: `(B, G=4, L=32)` 提问目标子句序列；
  - `w_cand` + `cand_pos_mask`: `(B, C=8, L=32)` 混合正样本知识子句 $K^+$ (`1.0`) 与跨样本负干扰子句 $K^-$ (`0.0`)；
  - `w_discourse`: `(B, T=8, L=32)` 以提问末句为第 `0` 步起点的渐进标点回答子句链 (`1 Mamba step = 1 标点短句`)。
- **训练与双脑闭环推演入口**：[`training/train_phase5_mamba_flow_cuda.py`](file:///Users/kael/workbench/HollyShit/training/train_phase5_mamba_flow_cuda.py)
  - **Stage 2A（单流话语推演热身）**：
    ```bash
    python3 training/train_phase5_mamba_flow_cuda.py \
      --active_streams discourse \
      --left_brain_ckpt_prefix left_brain_s32_fullrank \
      --ckpt_prefix right_brain_s32_stage2a
    ```
  - **Stage 2B / Stage 3（三流协同 + 知识选择器联合训练 + 双脑闭环多子句自回归推演）**：
    ```bash
    python3 training/train_phase5_mamba_flow_cuda.py \
      --active_streams discourse,knowledge,goal \
      --left_brain_ckpt_prefix left_brain_s32_fullrank \
      --ckpt_prefix right_brain_s32_full \
      --closed_loop_reencode
    ```
