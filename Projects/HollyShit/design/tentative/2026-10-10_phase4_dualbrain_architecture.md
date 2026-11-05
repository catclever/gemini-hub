---
title: "Phase 4 & 5: Dual-Brain Continuous Reasoning Architecture"
status: tentative
date: "2026-10-10"
---

# Dual-Brain Continuous Reasoning Architecture

This document records the currently implemented, tentative design for the Phase 4 and Phase 5 Latent Engine. It represents the transition from a concatenative paradigm to a purely physical dynamical system based on Hilbert space projection and Optimal Transport Flow Matching.

## 1. Core Physics & Paradigm Shift
* **Previous Flawed Approach**: Used 1D Interpolation, Channel Concatenation, and Step-function Chunker to fuse discrete context, target concepts, and conditions.
* **New Mathematical Foundation**:
  - The model operates in an infinite-dimensional orthogonal polynomial measure space (Hilbert Space).
  - **Left Brain (Mamba/HiPPO)**: The "Planner". Operates purely in the abstract logical space, computing the dynamic integration (Potential Energy $\Delta h$) required to step from Context $A$ to Future $B$.
  - **Right Brain (Flow Match 1D-Unet)**: The "Renderer". Operates purely as a physical sculptor, translating the abstract Potential Energy into a highly specific continuous curve (Phase 1 text manifold).

## 2. Orthogonal Knowledge Attractor
* **Problem**: How to prevent the model from hallucinating exact facts without forcing it to memorize them in the abstract potential energy?
* **Solution**: The `OrthogonalAttractor`.
* **Mechanism**: 
  - Instead of channel concatenation, the Unet uses a purely geometric projection (similar to Linear Attention without Softmax).
  - It computes the inner product (Activation: $X^T K$) between its current trajectory $X$ and the external knowledge vectors $K$.
  - If a dimension matches, it applies an Orthogonal Pull ($K \cdot (X^T K)$) forcing the trajectory to sharply snap to the exact coordinates of the factual knowledge without disrupting the underlying grammatical inertia.

## 3. The HiPPO Oracle & Decoupled Curriculum Training
To prevent the catastrophic VRAM bloat and instability of joint backpropagation through ODEs, and to preserve the strict Hilbert space physics, the training pipeline is heavily decoupled into two phases using a mathematically rigorous Oracle.

### The "HiPPO Oracle"
We implemented an exact, parameter-free HiPPO-LegS projector (`model/hippo_oracle.py`). It rigorously integrates a Phase 1 continuous wave into $N$ Legendre polynomial coefficients ($h_{hilbert}$). 
* **Crucial Insight**: A simple "Mean Pooling" of the target sequence degrades the manifold into a flat Euclidean point, destroying the temporal integration physics. The HiPPO Oracle preserves the time-measure dynamics.

### Phase 4: Training the Renderer (Curriculum Learning)
* **Goal**: Teach the Flow Match Unet to draw smooth grammar curves and snap to facts.
* **Input**: The HiPPO Oracle's exact polynomial coefficients of the *target sentence*.
* **Curriculum / CFG**: During training, the Knowledge Attractor vectors are randomly dropped out (CFG). 
  - *When dropped*: The Unet is forced to rely solely on the polynomial momentum to draw perfectly smooth but generic grammar curves. (Prevents the "Lazy Network" collapse).
  - *When provided*: The Unet learns to elegantly route the grammatical curve through the exact factual coordinates.

### Phase 5: Training the Planner
* **Goal**: Teach Mamba to predict the future abstract logic.
* **Mechanism**: The Unet is completely bypassed. Mamba reads the Context + Knowledge and tries to directly predict the polynomial coefficients ($h_{hilbert}$) of the upcoming target sentence.
* **Loss**: Pure, extremely fast Mean Squared Error (MSE).

## 4. Required Training Data Topology
For this architecture to function, traditional `[Prompt] -> [Response]` data fails. The data MUST be structured as a Tripartite Physical Experiment:
1. **Context ($C$)**: The dialogue history.
2. **Knowledge ($K$)**: Explicitly retrieved facts (e.g., from Wiki) appended to the context so the Orthogonal Attractor has a source of gravity.
3. **Target Chunk ($T$)**: The response MUST be heavily chunked (e.g., split by punctuation like commas or periods). This ensures the required Potential Energy ($\Delta h$) is a constant, singular force field, preventing "schizophrenic" wind vectors.
