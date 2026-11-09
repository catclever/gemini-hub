---
name: dev-server
description: "SOP for strictly on-demand management of project dev servers, preview environments, and PVE test environments across Mac, PVE, and Cloud Remote Project conversations."
---
# Dev Server & PVE Test Environment Protocol (Strictly On-Demand)

This skill defines the standard operating procedure for syncing, starting, restarting, inspecting, or stopping dev servers and PVE test environments across all three conversation contexts (**Local Mac**, **PVE**, and **Google Cloud Remote Project**).

> [!IMPORTANT]
> **Strict On-Demand Principle**: Never automatically start or restart a dev server after every routine coding task or Git commit! Only sync or manage the test environment when the user explicitly requests it (e.g., *"同步到 PVE 测试环境"*, *"启动测试服务"*, *"重启预览服务"*, *"关闭测试环境"*), or during an explicit `night-shift` handoff.

---

## 1. On Mac (Local Dev Server)
- **Rule**: **Manual / On-Demand Start Only**. Do NOT automatically start a local dev server during normal coding tasks.
- **Action**: Wait for the user to explicitly request starting the local server. Otherwise, assume the user runs it in their own terminal.

---

## 2. From Mac or PVE Conversation $\rightarrow$ Controlling the PVE Test Environment (`pve_test_sync.sh`)

When a project has a test clone on PVE (`/root/Projects/<project_name>`) and the user asks in a Mac or PVE conversation to sync code or control the PVE preview service, use `pve_test_sync.sh` (via `ssh Antigravity` from Mac, or directly if already on PVE):

### Supported On-Demand Actions (`-a <action>`)

| Action | Command Example (from Mac) | Behavior & Best Use Case |
| :--- | :--- | :--- |
| **`sync`** *(Default & Recommended)* | `ssh Antigravity "bash ~/.gemini/config/scripts/pve_test_sync.sh -p <project_name> -a sync"` | Runs `git fetch && git pull --rebase` in `/root/Projects/<project_name>` **without restarting the process**. Preferred whenever the dev server (e.g. Vite, Next.js, Uvicorn `--reload`) is already running and supports hot-reload! |
| **`start`** | `ssh Antigravity "bash ~/.gemini/config/scripts/pve_test_sync.sh -p <project_name> -a start"` | Runs `sync`, then starts Zellij session `[<project_name>] env` **only if not already running**, and outputs the 30-line server log tail. |
| **`restart`** | `ssh Antigravity "bash ~/.gemini/config/scripts/pve_test_sync.sh -p <project_name> -a restart"` | Runs `sync`, then unconditionally restarts `[<project_name>] env` (use when `.env`, dependencies, or backend configs changed). |
| **`stop`** | `ssh Antigravity "bash ~/.gemini/config/scripts/pve_test_sync.sh -p <project_name> -a stop"` | Cleanly kills and deletes the `[<project_name>] env` Zellij session to free PVE memory/ports. |
| **`status`** | `ssh Antigravity "bash ~/.gemini/config/scripts/pve_test_sync.sh -p <project_name> -a status"` | Prints current PVE `HEAD` commit, whether `[<project_name>] env` is running, and the last 30 lines of server logs. |

- **CRITICAL Network Binding (`0.0.0.0`)**: Any dev server command on PVE (configured via `PVE-Dev-Server-Cmd:` in `~/.gemini/Projects/<project_name>/IRON_RULES.md` or passed via `-c "<cmd>"`) **MUST** bind to `0.0.0.0` (e.g. `--host 0.0.0.0`, `--bind 0.0.0.0`) so Princess can access the preview from her Mac browser.

---

## 3. From a Cloud Remote Project Conversation $\rightarrow$ Controlling the PVE Test Environment On-Demand (Zero Public Port)

Because Google Cloud Remote Project sandboxes (`/workspace/<project_name>`) run on Google's cloud infrastructure and cannot SSH directly into the private LAN PVE server:

1. **Lightweight On-Demand Tag Watcher on PVE**:
   - On PVE, a lightweight watcher (`pve_test_sync.sh -p <project_name> -a watch`) polls `refs/tags/pve-env-*` every 15 seconds.
   - **Normal `git push origin main` commits are completely ignored** by the watcher — PVE never wastes resources or interrupts running services during routine coding commits.
2. **How the Cloud Agent Triggers PVE On-Demand**:
   - **ONLY** when the user explicitly commands inside the Cloud Remote conversation (e.g., *"把代码同步到 PVE 测试环境"*, *"启动 PVE 测试环境"*, *"重启 PVE 服务"*, *"查看 PVE 测试环境日志"*, *"停止 PVE 测试服务"*):
   - **Step 1**: Ensure current changes are committed and pushed to `origin main`.
   - **Step 2**: Push the corresponding on-demand trigger tag (`pve-env-sync`, `pve-env-start`, `pve-env-restart`, `pve-env-stop`, or `pve-env-status`):
     ```bash
     ACTION="sync" # or: start | restart | stop | status
     git tag -f "pve-env-${ACTION}"
     git push -f origin "refs/tags/pve-env-${ACTION}"
     ```
   - **Step 3**: Wait ~15–20 seconds for PVE to consume/delete the tag, execute the action, and post the status + 30-line server log to the current HEAD commit on GitHub. Then read it back directly in the Cloud sandbox:
     ```bash
     sleep 18
     gh api "repos/catclever/<project_name>/commits/$(git rev-parse HEAD)/comments" \
       --jq '.[-1].body // "No PVE status comment posted yet."'
     ```

---

## 4. Starting the PVE On-Demand Watcher (One-Time Setup on PVE)

For any project where Princess wants to control the PVE test environment from inside a Cloud Remote Project conversation, launch the lightweight tag watcher in a dedicated PVE Zellij session:

```bash
ssh Antigravity "antiverse-run --name '[<project_name>] pve-sync-watch' --cwd /root/Projects/<project_name> --force -- bash ~/.gemini/config/scripts/pve_test_sync.sh -p <project_name> -a watch"
```
