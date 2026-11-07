---
name: pve-dispatch
description: "SOP for delegating tasks to REMOTE agents on the PVE server. Use this ONLY when the project is tagged as PVE-Native or requested by the user."
---
# PVE Remote Dispatch SOP

This skill defines how the Lead Architect (Main Agent) should orchestrate agents (like `dev` or `ops`) for projects running on the remote PVE server, while the Main Agent itself is running on the local Mac.

## When to use this skill
Use this skill whenever delegating tasks to remote PVE compute resources (`Project-Environment: PVE-Native` or explicitly requested by the user).

## Dispatch Routing Strategy

Before dispatching, evaluate the scope, GitHub backing, and interactivity requirements of the task across three execution modes:

| Mode | Watchdog Script | Engine | Best For |
| :--- | :--- | :--- | :--- |
| **Mode A** | `descartes_watchdog.sh` | Descartes + EnginEdge (`deepseek-v4.1-flash`) | Well-scoped, single-module tasks (≤50 turns), worktree-isolated, **no GitHub needed** |
| **Mode B** | `remote_watchdog.sh` | Google Cloud Remote Agent (`agy --remote-agent`) | Heavy/multi-file tasks on **GitHub-backed** projects with `flock` multi-account rotation & PR delivery |
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
Use this mode for heavy coding or multi-file refactoring tasks on GitHub-backed projects where PVE dispatches an isolated Google Cloud Remote Agent (`agy --remote-agent`) using `flock`-guarded account switching (`agy-account switch`).

1. **Mandatory Pre-Dispatch Context Distillation Checklist**:
   Because the Cloud Remote Agent executes in an isolated cloud sandbox, you MUST prepare its context before dispatching:
   - [ ] Log the task in Kanban via `kanban-task-manager` MCP (`create_task` / `update_task_status`).
   - [ ] Query project knowledge via `kb_search(project="<project>", query="...")` and distill key architectural rules and caveats directly into `<Prompt>`.
   - [ ] `remote_watchdog.sh` automatically appends `[Global]` and `[Dev Agent]` from `~/.gemini/Projects/<project>/IRON_RULES.md` on PVE if not already present in `<Prompt>`.
2. **Account Selection (`--account`)**:
   - PVE supports multi-account token switching via `/usr/local/bin/agy-account switch <account>`, protected by `/tmp/agy_account_switch.lock` (`flock` mutex with 8-second OAuth token binding hold):
     - `kaelina1029@gmail.com` (or substring `kaelina1029`)
     - `saint.archangel.satan@gmail.com` (or substring `saint.archangel`)
3. **Dispatch on PVE via SSH**:
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
   - Omit `-d` if dispatching a Pure-Remote repository that has no `/root/Projects/<project>` clone on PVE.
   - Monitor progress via `/tmp/<Task_ID>.signal`, `/tmp/remote_<Task_ID>.log`, or attach to the Zellij session `ssh Antigravity -t "zellij a '[<project>] remote-<Task_ID>'"`.

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
