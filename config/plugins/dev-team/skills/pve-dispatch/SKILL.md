---
name: pve-dispatch
description: "SOP for delegating tasks to REMOTE agents on the PVE server. Use this ONLY when the project is tagged as PVE-Native or requested by the user."
---
# PVE Remote Dispatch SOP

This skill defines how the Lead Architect (Main Agent) should orchestrate agents (like `dev` or `ops`) for projects running on a remote PVE server, while the Main Agent itself is running on the local Mac.

## When to use this skill
Use this skill whenever delegating tasks to remote compute resources (PVE or Google Jules).

## Dispatch Routing Strategy

Before dispatching, check if the current project has a GitHub remote repository (`git remote get-url origin` containing `github.com`):

### Mode A: Google Jules Dispatch (Priority 1: GitHub Projects)
> [!TIP]
> **Zero Mutagen Sync**: Jules runs in Google Cloud VMs directly connected to GitHub. You DO NOT need Mutagen sync for GitHub projects! PVE acts solely as an unattended 7x24h watchdog (fully immune to Mac sleep/lid-close).

1. **Pre-Flight Git Sync (Mac)**: Ensure local changes are committed and pushed to GitHub:
   ```bash
   git status  # If unpushed, git add . && git commit -m "chore: save before jules dispatch" && git push
   ```
2. **Dispatch via Jules Watchdog**:
   Run the Jules watchdog script on PVE in the background using SSH Stdin stream (`bash -s` with Heredoc). This avoids nested Shell escaping conflicts and completely eliminates disk temporary files:
   ```bash
   ssh Antigravity 'bash -s' << 'EOF'
   bash ~/.gemini/config/scripts/jules_watchdog.sh \
     -t "<Task_ID>" \
     -r "<owner/repo>" \
     -b "<branch>" \
     -p "<Prompt>" \
     -d "<project_dir>" \
     [--autonomous]  # Optional: Default OFF for daytime tasks. Append only if user requests zero-intervention.
   EOF
   ```
   *Mode Selection Rules*:
   - **Standard Mode (Default for Daytime)**: Omits `--autonomous`. Preserves human-in-the-loop plan reviews (`requirePlanApproval: true`). If Jules enters `AWAITING_PLAN_APPROVAL` or `AWAITING_USER_FEEDBACK`, it waits for user input.
   - **Autonomous Mode (`--autonomous`)**: Activates three lines of defense:
     1. *Defense 1*: Pre-suppresses plan stops (`requirePlanApproval: false`).
     2. *Defense 2*: Auto-approves plan via `:approvePlan` if `AWAITING_PLAN_APPROVAL` occurs.
     3. *Defense 3*: Auto-replies with best-practice directive via `:sendMessage` if `AWAITING_USER_FEEDBACK` occurs (max 3 retries).
   *Note: If `-d` is specified, the watchdog will automatically commit and push dirty files to remote before dispatching, aborting if synchronization fails.*
   *For Night Shift / Autonomous runs, append both `--autonomous` and `--auto-merge`.*
3. **Wait for System Wakeup**:
   Wait for `/tmp/<Task_ID>.signal` to output `DONE: PR Created: <PR_URL>`.
4. **Deliverables & Merge**:
   - Provide the PR URL to the user or record it in `tasks/<Task_ID>.md`.
   - Once merged on GitHub, Mac simply runs `git pull` to sync.

---

### Mode B: Bifrost PVE `agy` Dispatch (Priority 2: Private / Non-GitHub PVE Projects)
Use this mode ONLY if the project is NOT on GitHub and `IRON_RULES.md` contains `Project-Environment: PVE-Native`.

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
