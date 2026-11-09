---
title: Dual-Host Remote Watchdog & Strictly On-Demand PVE Test Environment Sync
description: Architecture and usage of Dual-Host remote_watchdog.sh (Mac Direct-to-Cloud
  Option B1 vs PVE Multi-Account Option B2) and strictly on-demand pve_test_sync.sh
  (including Git tag trigger pve-env-* for Cloud Remote Agent conversations).
date: '2026-11-09'
---

# Dual-Host Remote Watchdog & On-Demand PVE Test Environment Sync

## 1. Dual-Host Remote Watchdog (`config/scripts/remote_watchdog.sh`)

`remote_watchdog.sh` automatically detects the execution host via `command -v antiverse-run >/dev/null 2>&1`:

- **Option B1 — Mac Direct-to-Cloud Mode (`IS_PVE_HOST=false`)**:
  - Invoked directly from a Mac Local Project conversation without SSHing to PVE when using the current logged-in Mac account (no `-a` override).
  - If `-a|--account` is passed on Mac without `/usr/local/bin/agy-account`, fails fast with `FAILED: ACCOUNT_SWITCH_REQUIRES_PVE`.
  - Spawns `agy --remote-agent "<Remote_Project>" --mode agent --model "<Model>"` inside a local Python `pty.openpty()` wrapper with non-blocking FIFO stdin (`/tmp/remote_<Task_ID>.stdin`), streaming output to `/tmp/antiverse_remote_<Task_ID>.log` and tracking PID in `/tmp/remote_<Task_ID>.pid`.
  - Supports Autonomous Defenses 1, 2, and 3 (writing continuation prompts into `$STDIN_FIFO`) and automatically pulls merged PR changes (`git -C "$TARGET_GIT_DIR" pull --rebase origin "$BRANCH"`) into the Mac workspace when `--auto-merge` is set.

- **Option B2 — PVE Multi-Account / Lid-Close Mode (`IS_PVE_HOST=true`)**:
  - Uses `flock -w 120 200` on `/tmp/agy_account_switch.lock`, calls `/usr/local/bin/agy-account switch "$ACCOUNT"`, launches `antiverse-run --remote "<Remote_Project>"` in Zellij, and holds the lock for 8 seconds until OAuth token binding completes.
  - Does not require a `/root/Projects/<project>` clone on PVE if `-d` is omitted.

## 2. Strictly On-Demand PVE Test Environment Sync (`config/scripts/pve_test_sync.sh`)

Manages `/root/Projects/<project>` test environments across `Local`, `PVE-Native`, and `Pure-Remote` topologies:
- **Never Auto-Starts on Normal Pushes**: Routine `git push` to `main` never restarts or launches the dev server.
- **Supported Actions (`-a <action>`)**:
  - `sync` (default): Runs `git fetch && git pull --rebase` only (preserves hot-reload).
  - `start`: Runs `sync` + starts `[<project>] env` Zellij session if not running.
  - `restart`: Runs `sync` + force-restarts `[<project>] env`.
  - `stop`: Terminates `[<project>] env` Zellij session.
  - `status`: Prints HEAD commit, Zellij session status, and last 30 lines of `/tmp/antiverse_env_<project>.log`.
  - `watch`: Lightweight 15s tag poller (`git ls-remote --tags origin "refs/tags/pve-env-*"`) for Cloud Remote Project conversations. Consumes `pve-env-<sync|start|restart|stop|status>` tags, executes the action, and posts the 30-line server log to GitHub commit comments (`gh api repos/<repo>/commits/<sha>/comments`).
