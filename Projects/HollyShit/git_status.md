# Git topology (verified 2026-10-14)

| Path | Role | Remote | Branch / HEAD |
|---|---|---|---|
| `/` (HollyShit) | Root repo | `github.com/catclever/HollyShit` | main, ahead 3 of origin |
| `gemma_prosthesis/` | Submodule (url `./gemma_prosthesis`) | **NONE** (local only) | main @ 5ad8d44 (clean, matches gitlink) |
| `training/core/` | Submodule | `github.com/catclever/Huntun` | main @ faba866 (= origin/main, but dirty: args.py, checkpoint.py modified, dataloader.py deleted, `__init__.py` untracked) |
| `dev_tests/mamba-mlx-test/` | Independent clone (root `.gitignore`d, not submodule) | upstream `alxndrTL/mamba.py` | main @ 57dcd93 |
| `dev_tests/mlx-examples/` | Independent clone (ignored) | upstream `ml-explore/mlx-examples` | main @ e52c128 |

## Caveats
- `training` is a SYMLINK to Google Drive (`.../hollyshit/training`); git warns "training/core not to be a symbolic link" for submodule ops. Run submodule commands from inside `training/core` directly.
- Root working tree shows many `model/**` files as deleted (unstaged) - investigate before any commit/checkout.
- Previous git_status.md was stale (2026-09-20); this replaces it.
- `.git/fsmonitor--daemon.ipc` errors are harmless noise.
- `gemma_prosthesis` has no remote: its commits exist only locally; the root gitlink SHA cannot be fetched by others (Jules cannot see it).
