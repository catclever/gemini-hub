---
id: fix_phase5_rho_saturation_and_beat_bottleneck_012
title: Fix Phase 5 Rho Saturation, 32-Beat Low-Pass Bottleneck, and Causal Fallback
  Articulation
status: completed
priority: high
tags:
- phase5
- mamba
- bugfix
- flow_matching
session: f89929c4-1b39-4cf5-b9cd-979e32cfc68f
---

## Technical Blueprint (`fix_phase5_rho_saturation_and_beat_bottleneck_012`)

### 1. Fix `rho_pred = 1.00` Permanent Saturation in `TimeWarpedLegendreExpander` (`model/flow_mamba.py`) & `model/loss_mamba_cfm.py`
- **Root Cause**:
  1. `self.length_head(h_summary)` + `torch.sigmoid(...)` executed inside `bfloat16` autocast where $\sigma(z)$ rounds to exact `1.0` for $z > 5.54$, making `SigmoidBackward0` ($y(1-y)$) and `.clamp(max=1.0)` strictly `0.0` forever.
  2. When `rho_override is None`, `rho_used = rho_pred` was not detached before `l_eff = rho_used * 512`, causing `loss_potential` gradients through `horizon_gate` to push `rho_pred -> 1.0` with a $512\times$ multiplier.
- **Exact Fix**:
  1. Execute `self.length_head` and `torch.sigmoid` under `with torch.amp.autocast(device_type=h_summary.device.type, enabled=False):` in `float32`.
  2. Do NOT use `.clamp(min=0.04, max=1.0)` on the post-sigmoid output (which kills gradients at boundary); instead apply smooth affine scaling `rho_pred = 0.04 + 0.96 * torch.sigmoid(logits_fp32.clamp(min=-8.0, max=8.0))` in `float32`, guaranteeing non-zero backward derivative everywhere!
  3. Always detach `rho_pred` when constructing `rho_used` (`rho_used = rho_pred.detach()` when `rho_override is None`), so `length_head` is supervised purely by `loss_len` (`F.smooth_l1_loss(rho_pred.float(), rho_true.float(), beta=0.05)`) without gradient hijacking from `horizon_gate`.
  4. In `mamba_cfm_loss` (`model/loss_mamba_cfm.py`), pass `rho_override=rho_true` during training (or `verbosity_hint_prob=0.85` for `verbosity_cond`, while always passing `rho_override=rho_true` or `rho_pred.detach()`), so the 32 macro-beats are aligned to the true valid target horizon during training while `rho_pred` learns accurately from `h_summary` (computed strictly BEFORE `verbosity_cond` is added, avoiding any label leakage from `verbosity_cond` into `length_head`!).

### 2. Break the 32-Beat Low-Pass Bottleneck with Full-Resolution $L=512$ Causal Articulation (`model/flow_mamba.py`)
- **Root Cause**:
  - `HiPPOOracleCUDA` has diagonal impulse response $K_{t,t} \approx 1.0$, so `h_target(t)` is a full-resolution 512-token sequence with sharp token-to-token variations.
  - Expanding $K=32$ beats onto $L=512$ via `b_warped @ c_beats` creates a rank-32 temporal low-pass curve (16 tokens per beat), causing `Pot Loss` to plateau at intra-beat variance (`~0.55`) and `unet` to decode 16-char repeats (`，，，，，`, `rrrrrr`).
- **Exact Fix**:
  1. **Distinct Beat Queries**: Initialize `beat_queries` with orthogonal / sinusoidal beat index encodings + normal std `0.25` (instead of `0.02`), and separate `proj_legendre` and `proj_gauss` linear projections in `TimeWarpedLegendreExpander` so polynomial spectral degree $k$ and Gaussian beat window $k$ have independent channels.
  2. **Two-Stage Macro-Beat + Micro-Canvas Articulation**:
     - Split the $N$ layers (`num_layers`, default 6) of `MultiStreamMambaPlanner` into:
       - **Macro Planner Layers (`n_macro = num_layers // 2`, e.g. 3 layers)**: Process valid `x_context` (with positional encoding and strict `<PAD>` masking) and evolve the $K=32$ `beats` with `beat_ctx_resonance` and `beat_know_resonance`.
       - **Time-Warped Legendre Expansion (`expander`)**: Expand the 32 macro-beats `c_beats` onto the $L=512$ canvas to form the macroscopic scaffold $H_{\text{macro}}(t) \in \mathbb{R}^{B \times L \times D}$ (with sinusoidal canvas `pos_emb`).
       - **Micro Canvas Causal Articulation Layers (`n_micro = num_layers - n_macro`, e.g. 3 layers)**: Run full-resolution Causal Mamba SSM (or Causal Fallback) layers across the $L=512$ sequence $H(t)$, interleaved at every layer with token-level **Orthogonal Context Resonance** (`canvas_ctx_resonance` attending to `h_ctx` with `context_mask`) and **Orthogonal Multi-Stream Knowledge Resonance** (`canvas_know_resonance` attending to `h_know` with `knowledge_mask`), followed by an output projection + gate!
     - Because the micro canvas layers run causally at full $L=512$ token resolution with per-position sinusoidal embeddings and token-level cross-resonance to `x_context` and `x_knowledge`, every position $t \in [0, 511]$ can articulate sharp, distinct token-level potential vectors!

### 3. Replace Broken `nn.TransformerEncoderLayer` Fallback with `CausalMambaFallbackBlock` (`model/flow_mamba.py`)
- **Root Cause**:
  - When `mamba_ssm` is not installed, `nn.TransformerEncoderLayer` had no causal mask (`is_causal=True`), no positional encoding, no `<PAD>` mask, and double-residual Post-LN.
- **Exact Fix**:
  - Implement `CausalMambaFallbackBlock(d_model)` in pure PyTorch/CUDA:
    - Causal depthwise `nn.Conv1d(d_model, d_model, kernel_size=4, padding=3, groups=d_model)` (sliced to `[:, :, :L]`) + `F.silu` (matching Mamba's local causal conv!).
    - Causal Self-Attention via `F.scaled_dot_product_attention(q, k, v, is_causal=True)` (uses FlashAttention-2 on CUDA automatically!) with gated SwiGLU/SiLU output projection.
  - Also in `MultiStreamMambaPlanner.forward`, add sinusoidal positional encoding to `x_context` before context layers, strictly mask `<PAD>` tokens (`h_ctx = h_ctx * valid_mask.unsqueeze(-1)`), and compute `h_summary` via masked mean + last-non-EOS token pooling so `h_summary` captures the full prompt semantics rather than just `<EOS>`.

### 4. Fix Phase 1 Encoder Masking & `sample_euler_ode` Attractor Scaling (`training/train_phase5_mamba_flow_cuda.py`)
- Pass attention mask (or zero out `<PAD>` embeddings if encoder uses unmasked self-attention, wait: check how Phase 4 called `encode_tokens` so we stay 100% manifold-consistent with Phase 4 `unet`!).
  - Wait: In Phase 4 (`train_phase4_hippo_flow_cuda.py`), `encode_tokens` called `layer(h, None)`. So to stay 100% distribution-compatible with the frozen Phase 4 `unet` and `manifold_mean/std`, keep `encode_tokens` identical to Phase 4!
  - In `sample_euler_ode` (`train_phase5_mamba_flow_cuda.py:450-467`), construct `k_attractors_norm` with fixed length `seq_len` (512) or scale by matching token density so `FlowMatching1DUnet.OrthogonalAttractor` receives the exact attractor scale it was trained with in Phase 4.
