# Operations Command Log

Recorded real-world operational scripts, migrations, deployment commands, and Git operations.

## Commands

### 2026-10-20: Git Remote Repository Setup & Push to GitHub
- **Host**: `Antigravity`
- **Working Directory**: `/root/Projects/psy_garden`
- **Command**:
  ```bash
  ssh Antigravity "cd /root/Projects/psy_garden && git add -A && git commit -m 'feat: upgrade botanist studio workflows and reslice confirmed true-color plant assets' && (git remote add origin git@github.com:catclever/psy_garden.git 2>/dev/null || git remote set-url origin git@github.com:catclever/psy_garden.git) && git branch -M main && git push -u origin main"
  ```
- **Result**: Successfully committed commit `ee54c41` (120 files changed) and pushed to `origin/main` on `https://github.com/catclever/psy_garden`.

### 2026-10-23: Sync PR #4 Branch (`godot-migration-12455927248257946642`) to PVE & Checkout
- **Host**: Mac Relay -> `Antigravity` (`/root/Projects/psy_garden`)
- **Command**:
  ```bash
  git fetch https://github.com/catclever/psy_garden.git godot-migration-12455927248257946642:refs/heads/pr4-godot
  git push Antigravity:/root/Projects/psy_garden refs/heads/pr4-godot:refs/heads/godot-migration-12455927248257946642
  ssh Antigravity "cd /root/Projects/psy_garden && git checkout godot-migration-12455927248257946642"
  mutagen sync flush psy-garden
  ```
- **Result**: Synced PR #4 branch to PVE, checked out `godot-migration-12455927248257946642` on `Antigravity`, and flushed Mutagen sync session `psy-garden`.

### 2026-10-27: Batch Footprint & Botanical AI Generation
- **Host**: `Antigravity` (`/root/Projects/psy_garden`)
- **Command**:
  ```bash
  ssh Antigravity "cd /root/Projects/psy_garden && tools/.venv/bin/python tools/batch_generate_footprint_and_ai.py"
  ```
- **Result**: Successfully computed Alpha-based stem `root_width`, 2.5D isometric ground ellipse projection, and queried OpenAI-compatible gateway (`deepseek-v4.1-flash`) for all 46 asset variants, updating their `metadata.json`. Committed as `c807131` and pushed to GitHub PR #5.
