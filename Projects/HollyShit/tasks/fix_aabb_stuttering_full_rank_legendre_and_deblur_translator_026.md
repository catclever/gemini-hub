---
id: fix_aabb_stuttering_full_rank_legendre_and_deblur_translator_026
title: Fix AABB Stuttering via K=32 Full-Rank Legendre Basis, Pauli Span Attractor
  & Deblurring CNN Translator
status: completed
priority: high
tags:
- phase4
- left-brain
- hippo
- translator
- aabb-fix
session: db682d63-e9e1-4409-9788-273b3cdf86f1
---

# Fix AABB Stuttering via K=32 Full-Rank Legendre Basis, Pauli Span Attractor & Deblurring CNN Translator

## 变更概述
1. Upgraded `HiPPOOracleCUDA` and `FlowMatching1DUnet` (`LeftBrainCrystallizer`) from warped `K=16, tau**0.65` Legendre basis to uniform full-rank `K=32, d_sub=32, tau=(l+0.5)/L` (`32 x 32 = 1024`) in float64 Gram-Schmidt, achieving exact `P = B^T B = I_32` (`diag=1.0000`, `neighbor_bleed=0.0000`) across all 32 positions of short punctuation clauses.
2. Added Diagonal Span Relay (`+0.25 * diag_relay`) and Pauli Adjacent Same-Key Exclusion (`-0.30 * same_key_competitor`) inside `OrthogonalAttractor.forward` in `model/flow_unet_cuda.py` to prevent two adjacent target positions from collapsing onto the same single source key index (`随随`, `过过`, `数数`, `法法`, `面面`, `哨兵兵`).
3. Upgraded `training/train_translator_cuda.py` to default to `omni_knowledge_corpus.jsonl` with `seq_len=32` punctuation-split clauses (`10-28` chars) and dual Clean + De-blurring/Denoising training (`synthesize_degraded_manifold_curve` simulating local neighbor bleed `alpha in [0.05, 0.30]` + Gaussian ODE landing jitter `sigma in [0.05, 0.30] * valid_std`), forcing the 1D CNN Translator (`Conv1d(kernel_size=3)`) to learn a sharpening inverse filter and wide Voronoi character basins.

## 验证结论
- [x] 核心逻辑已实现并通过验证

### Update
- Restored default `--data_path` in `training/train_translator_cuda.py` to `"data/Basic_ZH/moss_dialogues.jsonl"` (`ckpt_prefix="translator_conv1d"`, `prompt_seq_len=16`), keeping the CNN Translator as a pure knowledge-free text manifold vocoder trained on MOSS short clauses (`seq_len=32`) with Clean + De-blurring/Denoising (`synthesize_degraded_manifold_curve`).

### Update
- Renamed default checkpoint prefix in `training/train_translator_cuda.py` from generic `translator_conv1d` to unambiguous semantic name `translator_moss_s32_deblur`.
- Documented requirement to explicitly pass `--translator_ckpt` to Cell 6 to prevent automatic fallback to legacy `step_8106` checkpoint.

### Update
- Set default `--deblur_weight 0.0` and default `ckpt_prefix="translator_moss_s32_clean"` in `training/train_translator_cuda.py` so the CNN Translator defaults to 100% pure clean coordinate fidelity (avoiding MOSS 3-gram neighbor auto-correction bias on rare characters) while retaining `seq_len=32` short-clause alignment and `<PAD>` tail suppression.
