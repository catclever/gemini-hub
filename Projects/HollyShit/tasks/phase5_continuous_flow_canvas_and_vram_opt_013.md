---
id: phase5_continuous_flow_canvas_and_vram_opt_013
title: Phase 5 Pure Continuous OT-CFM Flow Canvas & VRAM Optimization
status: completed
priority: high
tags:
- phase5
- ot-cfm
- mamba
- vram-optimization
session: f89929c4-1b39-4cf5-b9cd-979e32cfc68f
---

## Architectural Blueprint (#013)

### 1. Root Cause of `Pot Loss ≈ 0.45` Plateau & Higher VRAM
1. **Static Non-Autoregressive L2 Centroid Collapse**:
   - In Phase 4, `HiPPOOracleCUDA` had `K_{t,t} = 0.99999243`, so `unet.pt` was trained with `h_potential ≈ X_1` and learned `v_unet(X_t, t, h_potential) ≈ (h_potential - X_t) / (1 - t)`.
   - In Phase 5, `MultiStreamMambaPlanner` previously only saw `(Context, Knowledge)` and did NOT see the flow state `(X_t, t)`. Under static L2 regression across all 512 tokens simultaneously, `mamba` converged to the conditional expectation $\mathbb{E}[X_1 \mid \text{Context}, \text{Knowledge}]$, which sits at the interior centroid of plausible characters (`Pot Loss ≈ 0.45`, decoding to high-frequency centroid characters `"得得来，，着着"`).
2. **VRAM Overhead in #012**:
   - Adding `q_proj, k_proj, v_proj` (`3 x 1024 x 1024`) to all 24 `OrthogonalKnowledgeResonance` modules added 75.5M parameters and ~3.5 GB of saved activation tensors, plus `harmonic_proj = Linear(512, 16384)` in `TimeWarpedLegendreExpander`.

### 2. Pure Continuous Two-Stage Macro-Once + Micro-Flow `(X_t, t)` Architecture (Zero Discrete CE Tricks)
1. **VRAM Optimization (`model/flow_mamba_013.py`)**:
   - Remove `q_proj`, `k_proj`, `v_proj` from `OrthogonalKnowledgeResonance` (restoring parameter-free `LayerNorm` + orthogonal inner-product resonance with `relu(scores - 0.25)` threshold, matching `FlowMatching1DUnet.OrthogonalAttractor`).
   - Replace the heavy `512 -> 16384` `harmonic_proj` in `TimeWarpedLegendreExpander` with a compact factorized spectral-slot modulation (`d_model -> d_model`) on the orthonormal Nyquist `_get_slot_carrier` basis.
2. **Two-Stage `MultiStreamMambaPlanner` (`model/flow_mamba_013.py`)**:
   - **Stage 1: `encode_macro(x_context, valid_mask, x_knowledge, knowledge_mask, target_len, rho_override) -> macro_state`**:
     - Runs 1x per batch (training) and 1x before the 10-step Euler ODE loop (inference).
     - Preserves the verified FP32 Leaky-STE `length_head` + `rho_pred.detach()` (`Len Loss ≈ 0.03`).
     - Rolls out the $K=32$ narrative beats and expands the macroscopic scaffold `h_canvas_macro` and `h_macro_potential`.
   - **Stage 2: `forward_canvas(x_t, t, macro_state, return_velocity=False)`**:
     - Embeds flow time $t \in [0, 1]$ via sinusoidal `TimestepEmbedder(d_model)`.
     - Constructs the **strictly causal 1-step right-shifted trajectory** `x_t_prev = F.pad(x_t[:, :-1, :], (0, 0, 1, 0))` (masked by `horizon_gate`), injecting `canvas_prev_proj(x_t_prev)` + `t_emb` FiLM modulation into `h_canvas_macro`.
     - Runs the $L=512$ causal `canvas_layers` (with per-layer `t_emb` FiLM modulation + `canvas_ctx_resonance` + `canvas_know_resonance`) so position $l$ attends over the entire emerging prefix $X_t(0 \dots l-1)$ without EVER seeing same-position $X_t(l)$ (physically preventing same-position identity copying!).
     - Outputs:
       - `h_potential`: Causal-prefix-conditioned endpoint trajectory $\hat{H}_1(X_t(<l), t)$.
       - `v_mamba = (h_potential - x_t) + t_expand * vel_proj(h_normed + vel_xt_proj(x_t))`: Direct OT-CFM velocity field prediction targeting $V_{\text{target}} = H_{\text{target}} - X_0$.
3. **Pure Continuous OT-CFM Velocity + Causal Potential Loss (`model/loss_mamba_cfm_013.py`)**:
   - Samples flow time $t \in [0, 1]$ and Gaussian noise $X_0 \sim \mathcal{N}(0, I)$, constructing $X_t = t H_{\text{target}} + (1 - t) X_0$ and $V_{\text{target}} = H_{\text{target}} - X_0$.
   - Computes mask-weighted:
     - `loss_potential`: $\| h_{\text{potential}}(X_t, t) - H_{\text{target}} \|_W^2$ (causal flow endpoint loss)
     - `loss_cfm`: $\| v_{\text{mamba}}(X_t, t) - V_{\text{target}} \|_W^2$ (direct OT-CFM velocity loss)
     - `loss_macro`: $\| h_{\text{macro\_potential}} - H_{\text{target}} \|_W^2$ ($t=0$ macroscopic scaffold anchor loss)
     - `loss_len` & `loss_pacing`: FP32 global horizon & beat pacing losses.
4. **Closed-Loop 10-Step Dual-Brain Euler ODE Integration (`training/train_phase5_mamba_flow_cuda_013.py`)**:
   - Initializes `mamba.expander.pad_tail_emb` from the normalized `<PAD>` token vector at startup so `<eos>` tails are clean from Step 50.
   - In `sample_euler_ode`: runs `macro_state = mamba.encode_macro(...)` **once** before the 10-step loop, and inside each Euler step $i \in \{0 \dots 9\}$, calls `h_potential, v_mamba = mamba.forward_canvas(x, t_tensor, macro_state, return_velocity=True)` and `v_unet = unet(x, t_tensor, h_potential=h_potential, k_attractors=k_attractors_norm)`, integrating with Dual-Brain velocity `v_pred = 0.8 * v_unet + 0.2 * v_mamba`.
