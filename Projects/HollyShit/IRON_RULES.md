## [Global]
- Project: HollyShit
- Dual-Architecture: PyTorch/CUDA (Latent Engine) and MLX (Physical Renderer)

## [Main Agent]
- Always query and maintain project knowledge via the project-manager skill.
- Do NOT store metadata inside the working directory.

## [Dev Agent]
- Maintain strict compatibility between the continuous latent space and discrete token spaces.
- Use PyTorch for Phase 4, MLX for Phase 2.

## [Workspace & Git Hygiene]
- `training/core` is the separate repo `catclever/Huntun`: commits and changes inside `training/core` must be pushed to `catclever/Huntun` first, and the root submodule pointer bumped and committed separately.
- Never commit secrets (`.env`) or checkpoints; keep them gitignored.
- `model/` and `training/` are real dirs in the workspace; Google Drive holds symlinks back to them, so git is the only backup of their code.
