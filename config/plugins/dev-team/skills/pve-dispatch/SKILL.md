---
name: pve-dispatch
description: "SOP for delegating tasks to REMOTE agents (PVE compute engines or Google Cloud Remote Agents). Use this for PVE-Native projects, or when dispatching any GitHub-backed project to Cloud Remote Agents (Mode B)."
---
# Remote & PVE Dispatch SOP

This skill defines how the Lead Architect (Main Agent) should orchestrate remote execution engines (`descartes_watchdog.sh`, `remote_watchdog.sh`, and `pve_watchdog.sh`) across Mac, PVE, and Google Cloud Remote Agents.

## When to use this skill
Use this skill whenever:
1. Delegating tasks to remote PVE compute resources (`Project-Environment: PVE-Native`), OR
2. Delegating heavy/autonomous coding tasks on **any GitHub-backed project** (`Local`, `PVE-Native`, or `Pure-Remote`) to Google Cloud Remote Agents (`Mode B`).

## Dispatch Routing Strategy

Before dispatching, evaluate the scope, GitHub backing, account requirements, and interactivity of the task across three execution modes:

| Mode | Watchdog Script | Engine | Best For |
| :--- | :--- | :--- | :--- |
| **Mode A** | `descartes_watchdog.sh` | Descartes + EnginEdge (`deepseek-v4.1-flash`) | Well-scoped, single-module tasks (≤50 turns) on PVE, worktree-isolated, **no GitHub needed** |
| **Mode B** | `remote_watchdog.sh` | Google Cloud Remote Agent (`agy --remote-agent`) | Heavy/multi-file tasks on **GitHub-backed** projects (supports **Option B1 Direct Mac-to-Cloud** & **Option B2 PVE Multi-Account/Lid-Close**) |
| **Mode C** | `pve_watchdog.sh` | Bifrost PVE Local `agy` (Zellij TUI) | Interactive/open-ended PVE-Native tasks requiring local PVE toolchains, databases, or services |

---

### Mode A: Descartes Unattended Watchdog (Well-Scoped, Single-Module Tasks)
> [!TIP]
> **Headless & Worktree-Isolated**: For well-scoped, single-module coding tasks that do not require interactive plan approval or arbitrary shell commands, delegate to the `descartes-dispatch` skill (`descartes_watchdog.sh`).

1. **When to Choose Mode A**:
   - The task targets a single module or concern and can be completed within ~30–50 ReAct turns.
   - An independent verification command (`--verify "<test cmd>"`) on the whitelist (`cargo`, `pytest`, `npm`, `go test`, etc.) can validate the outcome.
   - All relevant code is committed on the PVE project repository (`/root/Projects/<project>`).
2. **Execution**:
   - Read and follow the `descartes-dispatch` skill (`~/.gemini/config/plugins/dev-team/skills/descartes-dispatch/SKILL.md`) to dispatch `descartes_watchdog.sh` over SSH in an isolated git worktree (`descartes/<Task_ID>`).

---

### Mode B: Google Remote Agent Watchdog (`remote_watchdog.sh` — Heavy / Multi-File GitHub Tasks)
Use this mode for heavy coding or multi-file refactoring tasks on GitHub-backed projects. `remote_watchdog.sh` is a **Dual-Host** script that can run either directly on Mac (Option B1) or on PVE with `flock`-guarded multi-account switching (Option B2).

1. **Mandatory Pre-Dispatch Context Distillation Checklist**:
   Because the Cloud Remote Agent executes in an isolated cloud sandbox, you MUST prepare its context before dispatching:
   - [ ] Log the task in Kanban via `kanban-task-manager` MCP (`create_task` / `update_task_status`).
   - [ ] Query project knowledge via `kb_search(project="<project>", query="...")` and distill key architectural rules and caveats directly into `<Prompt>`.
   - [ ] `remote_watchdog.sh` automatically appends `[Global]` and `[Dev Agent]` from `~/.gemini/Projects/<project>/IRON_RULES.md` if not already present in `<Prompt>`.

2. **Choose Between Option B1 (Mac Direct) and Option B2 (PVE Routed)**:

   #### Option B1: Direct Mac-to-Cloud Dispatch (No PVE Hop — Default when using current Mac account)
   When running in a local Mac project conversation and using the currently logged-in Mac Google account (no `-a` account switch needed and Mac remains awake):
   ```bash
   nohup bash ~/.gemini/config/scripts/remote_watchdog.sh \
     -t "<Task_ID>" \
     -r "catclever/<project>" \
     -d "$PWD" \
     -b "main" \
     --tier "dev" \
     --autonomous \
     --auto-merge \
     -p "<Distilled Prompt + Acceptance Criteria>" \
     > /dev/null 2>&1 &
   ```
   - **How it works on Mac**: Performs Stage 0 Git sync in `$PWD`, spawns `agy --remote-agent` locally via a background PTY + FIFO (`/tmp/remote_<Task_ID>.stdin`) for autonomous Defenses 2 & 3, squash-merges the PR upon completion, and automatically runs `git -C "$PWD" pull --rebase origin main` so your local Mac workspace immediately receives the merged cloud commits!
   - **Monitor locally**: Check `/tmp/<Task_ID>.signal` and `/tmp/remote_<Task_ID>.log`.

   #### Option B2: PVE-Routed Multi-Account / Lid-Close Dispatch (`ssh Antigravity`)
   Use this option when switching Google accounts (`-a kaelina1029@gmail.com` or `-a saint.archangel.satan@gmail.com`), dispatching parallel multi-account queues, or running overnight with the Mac lid closed:
   ```bash
   ssh Antigravity 'bash -s' << 'EOF'
   nohup bash ~/.gemini/config/scripts/remote_watchdog.sh \
     -t "<Task_ID>" \
     -r "catclever/<project>" \
     -d "/root/Projects/<project>" \
     -b "main" \
     -a "kaelina1029@gmail.com" \
     --tier "dev" \
     --autonomous \
     --auto-merge \
     -p "<Distilled Prompt + Acceptance Criteria>" \
     > /dev/null 2>&1 &
   EOF
   ```
   - **Optional `-d` on PVE**: If the project does not have a `/root/Projects/<project>` clone on PVE (e.g., a Mac-local-only or Pure-Remote repo), simply omit `-d "/root/Projects/<project>"`. Once `/tmp/<Task_ID>.signal` on PVE reports `DONE: PR Merged`, run `git pull --rebase origin main` in your Mac workspace if applicable.
   - **Monitor on PVE**: Check `/tmp/<Task_ID>.signal`, `/tmp/remote_<Task_ID>.log`, or attach to the Zellij session `ssh Antigravity -t "zellij a '[<project>] remote-<Task_ID>'"`.

---

### Mode C: Bifrost PVE `agy` Dispatch (Interactive, Local-Service, or Open-Ended PVE Tasks)
Use this mode for exploratory debugging, tasks requiring PVE-local hardware/services/containers, or interactive sessions on PVE-Native projects.

1. **Prerequisite**: Tasks must be physically logged via `kanban-task-manager` MCP.
2. **Assign via Local Watchdog Script (Mac)**: 
   Run `mutagen sync list` to find the `Beta` URL path for this project to resolve the `<project_dir>`.
   Execute the local watchdog script on your Mac (runs locally, dispatches pure Antigravity TUI to PVE, and watches for completion):
   ```bash
   bash ~/.gemini/config/scripts/pve_watchdog.sh \
     -t "<Task_ID>" \
     -a "<dev|ops>" \
     -d "<project_dir>" \
     -p "<Prompt>" \
     [--tier "<dev|ops|pro>"]  # Default: 'dev' for -a dev; 'ops' for -a ops. Use 'pro' ONLY if Princess explicitly requested upgrade.
   ```
   *Architecture Guarantee: The watchdog runs LOCALLY on Mac. The remote task on PVE runs in its own dedicated, isolated Zellij session (`[<project>] <agent>-<task_id>`) with zero wrapper noise.*
   - **Real-Time Monitoring**: `ssh Antigravity -t 'antiverse attach <Task_ID>'` (or `zellij a '<session>'`).
   - **Instant Session Switching**: Inside any Zellij session, press `Alt + s` to open the floating Session Manager with live previews and switch between tasks with arrow keys + Enter.
   - **Session Lifecycle & 2-Hour Warm Period**: Tasks enter a 2-hour active warm period upon completion for instant `[Enter]` $\rightarrow$ `agy -c` revival. If unviewed after 2 hours, they automatically serialize into `(EXITED - attach to resurrect)` to free active RAM and server processes. Attach anytime via `antiverse attach <Task_ID>` to resurrect; clean all dead/exited sessions via `antiverse clean`.
3. **Wait for Native System Wakeup**:
   Wait for `/tmp/<Task_ID>.signal` completion.
4. **User Verification & Remote Merge**: 
   Verify with user, then run remote `merger` or merge locally.

---

## PVE Server Environment Knowledge (Antigravity)
- **Node.js & Ruby Management**: The Antigravity PVE server strictly uses `mise` for global and project-level environment version management (e.g., Node.js, Ruby). 
- **DEPRECATED Tools**: `fnm` and `nvm` have been entirely removed and are deprecated. DO NOT attempt to use `fnm` or `nvm` commands.
- **Commands**: 
  - Install a version: `mise install node@22`
  - Set global version: `mise use --global node@22`
  - Set project-level version: run `mise use node@22` in the project root to update `.mise.toml`.
  - List installed versions: `mise ls`
- **Gotchas**: When creating or maintaining remote PVE workspaces, ensure they rely on `mise` for their `$PATH` tools.
