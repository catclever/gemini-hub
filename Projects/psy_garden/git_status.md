# Git Status & Repository Configuration

## Project: psy_garden

- **Architecture Mode**: `PVE-Native` (Thin-Client Git)
- **Git Source of Truth**: Remote PVE Server (`Antigravity:/root/Projects/psy_garden`)
- **Remote Repository (GitHub)**: [https://github.com/catclever/psy_garden](https://github.com/catclever/psy_garden)
- **Remote Push URL**: `git@github.com:catclever/psy_garden.git`
- **Canonical Branch**: `main`
- **Upstream Tracking**: `origin/main` (Fully Synchronized)
- **Latest Commit**: `ee54c41 feat: upgrade botanist studio workflows and reslice confirmed true-color plant assets`
- **Working Tree Status**: Clean
- **Local Workspace**: `/Users/kael/Projects/psy_garden`
  - **Role**: Thin-Client / Local Editor
  - **Synchronization**: Bidirectional Mutagen sync (`mode: two-way-resolved`, `ignore-vcs: true`)
  - **Local `.git`**: Local git repository will not be synced to PVE. All canonical Git commits, branches, and push operations are executed remotely on PVE.
- **Remote Host**: `Antigravity` (configured in `~/.ssh/config`)
- **Remote Working Path**: `/root/Projects/psy_garden`
- **Recorded Date**: 2026-10-20

## Git Operation Directives

1. **Remote Execution Only**: All commits, branches, and push/pull operations must be performed on `Antigravity` within `/root/Projects/psy_garden`.
2. **GitHub Deployment Commands**:
   ```bash
   ssh Antigravity "cd /root/Projects/psy_garden && git add -A && git commit -m 'feat: ...' && git push origin main"
   ```
