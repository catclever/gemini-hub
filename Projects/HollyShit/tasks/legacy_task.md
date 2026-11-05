---
id: legacy_task
title: Sequence Flow Matcher (Phase1 DiT) Implementation
status: completed
priority: medium
tags: []
---
# Sequence Flow Matcher (Phase1 DiT) Implementation

- [x] **1. Implement Sequence Flow Matcher Core Networks**
  - [x] Implement PyTorch version `model/phase1_dit_cuda.py` with AdaLN and time/condition embedding.
  - [x] Implement MLX version `model/phase1_dit.py` matching the PyTorch architecture.
- [x] **2. Implement Training Script**
  - [x] Create `training/train_phase1_dit_cuda.py` (PyTorch CUDA) utilizing `training.core` package.
  - [x] Load frozen `TinyCharEncoderCUDA` to extract $Z_{macro}$ and target embedding $X_1$.
  - [x] Implement flow path interpolation and flow matching MSE loss (with padding masked).
- [x] **3. Implement Inference & Decoding Script**
  - [x] Create `infer/phase1_dit_mlx.py` (supporting MLX) and `infer/phase1_dit_cuda.py` (supporting PyTorch).
  - [x] Implement Euler ODE solver starting from $X_0 \sim \mathcal{N}(0, I)$ to $X_1$.
  - [x] Implement vocabulary projection (pointwise dot product with frozen `tok_emb` weights) and text reconstruction.
- [x] **4. Verification**
  - [x] Relocate files to `model/`, `training/`, and `infer/` directories and update all import paths.
  - [x] Add PyTorch CUDA inference script `infer/phase1_dit_cuda.py` and rename scripts to reflect `_cuda` and `_mlx` postfix.
  - [x] Run `dev_tests/test_flow_pipeline.py` to verify the pipeline compiles and executes correctly.
- [x] **5. Auto-Load Model Configurations**
  - [x] Modify `infer/phase1_dit_cuda.py` to auto-extract config variables from checkpoint companion `training_args.json`.
  - [x] Modify `infer/phase1_dit_mlx.py` to auto-extract config variables.
  - [x] Run compilation checks on modified inference files.
