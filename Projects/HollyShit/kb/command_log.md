
## 2026-10-31: Git Push Phase 4 Full-Rank K=32 Legendre Basis, Pauli Span Attractor & Deblurring Translator (#026)
- **Commit**: `284c73c` (`284c73c99b8a1be83e91049cb02aba265496b0ec`)
- **Branch**: `origin/main` (`catclever/HollyShit`)
- **Command**:
  ```bash
  git add model/flow_unet_cuda.py model/hippo_oracle.py training/train_phase4_hippo_flow_cuda.py training/train_translator_cuda.py
  git commit -m "fix(phase4): full-rank K=32 Legendre basis, Pauli span attractor, and deblurring translator (#026)"
  git push origin main
  ```
- **Files**:
  - `model/flow_unet_cuda.py`: Added diagonal span relay (+0.25) and adjacent same-key competitor suppression (-0.30) to `OrthogonalAttractor` against Pauli collapse / AABB stuttering; updated `FlowMatching1DUnet` to default `num_subbands=32` with float64 uniform Legendre basis ($B^T B = I_{32}$).
  - `model/hippo_oracle.py`: Upgraded `HiPPOOracleCUDA` to `num_subbands=32` with uniform float64 Gram-Schmidt basis guaranteeing full-rank coordinate lock ($B^T B = I_{32}$) at $seq\_len = 32$.
  - `training/train_phase4_hippo_flow_cuda.py`: Added `--num_subbands` argument (default 32) and wired to `HiPPOOracleCUDA` and `LeftBrainCrystallizer`.
  - `training/train_translator_cuda.py`: Added `synthesize_degraded_manifold_curve` (neighbor bleed + ODE Gaussian jitter), dual clean/de-blur loss with `--deblur_weight=0.5`, `<PAD>` class weight 0.25, and punctuation-clause defaults (`seq_len=32`).

## 2026-10-26: Git Push Phase 5 Backbone MRC Corpus & Self-Conditioned ODE Anti-Collapse Fix (#016)
- **Commit**: `d89550a`
- **Branch**: `origin/main` (`catclever/HollyShit`)
- **Command**:
  ```bash
  git add model/flow_mamba.py model/loss_mamba_cfm.py scripts/build_phase5_knowledge_corpus.py training/data/knowledge_dataset.py training/train_phase5_mamba_flow_cuda.py
  git commit -m "feat(phase5): upgrade backbone corpus to MRC and add self-conditioned prefix & sphere cosine loss (#016)"
  git push origin main
  ```
- **Files**:
  - `model/flow_mamba.py`: Added Stage 1 `macro_copy_pointer` and self-conditioned `x_t_prefix` in `forward` to prevent teacher-forced `H_target[:, l-1]` leakage.
  - `model/loss_mamba_cfm.py`: Replaced `3*t^2` with `0.5 + t`, raised `loss_macro` weight to `0.75`, added spherical cosine + radial norm preservation loss `loss_cos`, and normalized `per_sample_pot` strictly over valid target tokens.
  - `scripts/build_phase5_knowledge_corpus.py`: Upgraded `encyclopedia_rag` to true MRC (`cmrc2018`, `dureader_robust`, `squad`), added `try_split_structured_prompt` fallback for `BelleGroup/train_1M_CN`, and defaulted `--domains` to `"grounded_instruct,encyclopedia_rag"`.
  - `training/data/knowledge_dataset.py`: Allowed MRC substring containment (`len(tgt) < 0.85 * len(k)`), added `active_domains` filtering, and added on-the-fly legacy disjoint-split re-grounding.
  - `training/train_phase5_mamba_flow_cuda.py`: Added `--active_domains` flag, passed `x_0` for self-conditioned prefix, and logged `Cos` loss.

## 2026-10-26: Git Push Phase 5 CopyPointerHead, t^2-Weighted Potential Loss, Entity-Overlap & Observability
- **Commit**: `9eaa337a505b22b647fc04be20dbec945fb481fa` (short: `9eaa337`)
- **Branch**: `origin/main` (`catclever/HollyShit`)
- **Command**:
  ```bash
  git add model/flow_mamba.py model/loss_mamba_cfm.py training/data/knowledge_dataset.py scripts/build_phase5_knowledge_corpus.py training/train_phase5_mamba_flow_cuda.py
  git commit -m "feat(phase5): low-rank CopyPointerHead, t^2-weighted potential loss, entity-overlap relaxation and training observability"
  git push origin main
  ```
- **Files**:
  - `model/flow_mamba.py`: Low-rank `CopyPointerHead` ($d_{\text{ptr}}=64$, DWConv3 local context, learnable sink slot with $\log(L_{\text{active}})$ scaling, identity value transport without $v_{\text{proj}}$).
  - `model/loss_mamba_cfm.py`: $t^2$-weighted potential loss ($3.0 \cdot \max(t, 0.1)^2$), unweighted raw potential loss, $t$-bucketed MSE metrics, copy probability, and per-sample loss tensors.
  - `training/data/knowledge_dataset.py`: `is_non_cheating_knowledge` allowing entity/number/equation overlap while forbidding whole-clause verbatim copying, plus optional `return_domain_id=True` 4-tuple support.
  - `scripts/build_phase5_knowledge_corpus.py`: Relaxed clause-disjoint filtering, preserved math CoT equations, code API input entities, and multi-sentence narrative prompt context.
  - `training/train_phase5_mamba_flow_cuda.py`: Linear warmup + cosine decay LR scheduler, 50-step EMA + $t$-bucket + domain loss logging, deterministic fixed benchmark evaluation, and `--attractor_mode` / `--run_attractor_ablation` CLI support.

## 2026-10-26: Git Push Phase 5 Checkpointer Emergency Step & Auto-Resume Validation Fix
- **Commit**: `95c9981403f8106030651949bc97654afa34e319` (short: `95c9981`)
- **Branch**: `origin/main` (`catclever/HollyShit`)
- **Submodule `training/core` Commit**: `ff2af18` (`catclever/Huntun`)
- **Command**:
  ```bash
  git -C training/core commit -m "fix(checkpoint): update current_step on save and provide set_step helper"
  git -C training/core push origin main
  git add training/core training/train_phase5_mamba_flow_cuda.py
  git commit -m "fix(checkpoint): sync global_step dynamically for emergency saves and validate architecture compatibility on auto-resume"
  git push origin main
  ```
- **Files**:
  - `training/core/checkpoint.py`: Added `set_step(step)` and updated `self.current_step = step` in `save()`.
  - `training/train_phase5_mamba_flow_cuda.py`: Synced `checkpointer.set_step(global_step)` in training loop and implemented descending strict architecture compatibility verification (`find_compatible_mamba_ckpt`).

## 2026-10-25: Git Push Phase 5 Architecture & Streaming Corpus Builder
- **Commit**: `2474adf1151bb641ae1a0e04d5c16fda391ba4af` (short: `2474adf`)
- **Branch**: `origin/main` (`catclever/HollyShit`)
- **Command**:
  ```bash
  git add model/flow_mamba.py model/loss_mamba_cfm.py training/train_phase5_mamba_flow_cuda.py training/data/knowledge_dataset.py scripts/build_phase5_knowledge_corpus.py
  git commit -m "feat(phase5): MultiStreamMambaPlanner with Orthogonal Resonance and 6-Domain Non-Cheating Streaming Corpus Builder"
  git push origin main
  ```
- **Files**:
  - `model/flow_mamba.py`: MultiStreamMambaPlanner with OrthogonalKnowledgeResonance and TimeWarpedLegendreExpander.
  - `model/loss_mamba_cfm.py`: Multi-stream mamba CFM loss with 11.81x manifold normalization and verbosity hint conditioning.
  - `training/train_phase5_mamba_flow_cuda.py`: Multi-stream training loop with batched knowledge encoder and dual-brain evaluation.
  - `training/data/knowledge_dataset.py`: MultiStreamKnowledgeDataset supporting non-cheating zero-overlap multi-stream loading.
  - `scripts/build_phase5_knowledge_corpus.py`: 6-domain HuggingFace streaming multi-stream knowledge corpus builder without artificial tags.


- **2026-11-01 21:38** | `git push origin main` | Commit `a0eb919`
  - `feat(bicameral): implement Stage 2 & Stage 3 Right-Brain training, KnowledgeSelector and dual-brain rollout pipeline (#027)`
  - Pushed:
    - `model/bicameral_right_brain.py` (MultiStreamRightBrain, KnowledgeSelector, ThoughtFlowMatcher auto-calibration)
    - `training/data/knowledge_dataset.py` (BicameralClauseChainDataset with grounded prompt/knowledge parser & non-cheating candidate pool)
    - `training/train_phase5_mamba_flow_cuda.py` (Stage 2/3 MultiStreamRightBrain training & closed-loop dual-brain rollout pipeline)
    - `training/train_translator_cuda.py` (clean 100% vector default, deblur_weight=0.0, translator_moss_s32_clean prefix)

## 2026-11-07: Git Push Phase 5 Clean Lookback Source, gate_lb Anti-Saturation BCE & Radially Decoupled anti_stag (#041)
- **Commit**: `b79fdad` (`b79fdad0429c3cfd226825435e0a6b0325bd0f39`)
- **Branch**: `origin/main` (`catclever/HollyShit`)
- **Command**:
  ```bash
  rm -f /Users/kael/workbench/HollyShit/model/bicameral_right_brain.bak.py
  git add model/bicameral_right_brain.py
  git commit -m "fix(phase5): decouple clean lookback source, add gate_lb anti-saturation BCE, and radially decouple anti_stag (#041)"
  git push origin main
  ```
- **Files**:
  - `model/bicameral_right_brain.py`: Decoupled clean lookback source (`Z_lookback_source`), added `gate_lb` anti-saturation BCE supervision (`loss_gate_lb`), and radially decoupled `loss_anti_stag` on normalized direction (`v_pred_dir`).

## 2026-11-07: Git Remote Backup Phase 5 Right-Brain v2 Polar + Lookback (#041)
- **Commit**: `b79fdad` (`b79fdad0429c3cfd226825435e0a6b0325bd0f39`)
- **Remote Branch**: `origin/phase5-right-brain-v2-polar` (`refs/heads/phase5-right-brain-v2-polar`, no local backup branch created)
- **Command**:
  ```bash
  git push origin HEAD:refs/heads/phase5-right-brain-v2-polar
  ```

## 2026-11-07: Git Push Phase 5 Right-Brain v3 32x32 Spatial-Slot Flow & Rolling Continuation Stream (#042, #043)
- **Commit**: `42662d8` (`42662d8ce5469ce0caf26babcc8e50146b93accc`)
- **Branch**: `origin/main` (`catclever/HollyShit`)
- **Verification**:
  - `PYTHONPATH=. .venv/bin/python3 model/bicameral_right_brain.py`: `[Self-Test PASS] flow_version=3 iso_err=(2.41e-06, 1.79e-06) loss=15.2280 z_hat=(2, 1024)`
  - `import training.train_phase5_right_brain_stage1` & `import training.data.clause_stream_dataset`: `IMPORTS_OK`
- **Command**:
  ```bash
  rm -f model/bicameral_right_brain.bak.py training/data/clause_stream_dataset.bak.py
  git add model/bicameral_right_brain.py training/data/clause_stream_dataset.py
  git commit -m "feat(phase5): refactor Right-Brain v3 to 32x32 spatial-slot flow and restore rolling continuation stream (#042, #043)"
  git push origin main
  ```
- **Files**:
  - `model/bicameral_right_brain.py`: Refactored Right-Brain v3 to 32x32 spatial-slot flow with Legendre isometric transform (`flow_version=3`).
  - `training/data/clause_stream_dataset.py`: Restored rolling continuation stream and multi-domain balance.

