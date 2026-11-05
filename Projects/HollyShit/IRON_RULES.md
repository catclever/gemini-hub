## [Global]
- Project: HollyShit
- Dual-Architecture: PyTorch/CUDA (Latent Engine) and MLX (Physical Renderer)

## [Main Agent]
- Always query and maintain project knowledge via the project-manager skill.
- Do NOT store metadata inside the working directory.

## [Dev Agent]
- Maintain strict compatibility between the continuous latent space and discrete token spaces.
- Use PyTorch for Phase 4, MLX for Phase 2.

## [Jules Usage]
- Jules only sees code pushed to GitHub: push root repo (and Huntun) BEFORE dispatching; local uncommitted changes are invisible.
- One task = one repo. `training/core` is the separate repo `catclever/Huntun`: needs its own authorization/task; the root submodule pointer must be bumped separately (push Huntun first, then commit the pointer in root).
- `gemma_prosthesis` has no remote: it must get a GitHub remote before Jules can touch it.
- `dev_tests/` is gitignored (independent clones) and invisible to Jules.
- Cloud VM has no Apple Silicon/MLX and no CUDA GPU: use Jules only for refactor, docs, unit tests, static checks; never for training or perf validation (esp. Phase 2 MLX code).
- Avoid parallel tasks touching the same files (e.g. actively changing `model/`).
- Never commit secrets (`.env`) or checkpoints; keep them gitignored.
- `model/` and `training/` are real dirs in the workspace; Google Drive holds symlinks back to them, so git is the only backup of their code.
