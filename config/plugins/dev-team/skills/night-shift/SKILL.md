---
name: night-shift
description: Standard Operating Procedures for transferring the agent to an autonomous PVE environment when the user goes off work.
---
# Night Shift & Autonomous Handoff Protocol

When the user indicates they are leaving work or explicitly triggers the "Night Shift" (e.g., "转到PVE", "我下班了"), you MUST execute this protocol to transition the current conversation into a fully autonomous, unattended run.

## Routing: Choose the Execution Engine

Select the overnight execution path based on the nature of the remaining tasks:
- **Path A (Well-Scoped Unattended Task Queue — No GitHub Required)**: Use the **Descartes Autonomous Pipeline (`descartes_watchdog.sh --auto-merge`)** for serial, single-module coding tasks with deterministic test verification.
- **Path B (Heavy / Multi-File GitHub Task Queue — Cloud Sandbox + PR Auto-Merge)**: Use the **Google Remote Agent Autonomous Pipeline (`remote_watchdog.sh --autonomous --auto-merge -a <account>`)** for heavier multi-file features or refactors on GitHub-backed projects (`catclever/<project>`), leveraging PVE `flock`-guarded multi-account rotation (`kaelina1029@gmail.com` / `saint.archangel.satan@gmail.com`).
- **Path C (Interactive / Complex Master Controller Handoff)**: Use the **Antiverse Zellij Protocol (`antiverse-run`)** for open-ended, multi-agent, or PVE-local service orchestration sessions on PVE.

---

## Path A: Descartes Autonomous Pipeline (`descartes_watchdog.sh --auto-merge`)

> [!TIP]
> **Complete Sleep / Lid-Close Immunity**: `descartes_watchdog.sh` runs directly on PVE in isolated git worktrees (`descartes/<Task_ID>`) without requiring Mac connectivity or GitHub round-trips.

### Step 1: Pre-Handoff Checkpoint & Sync (PVE)
Ensure all work is synced and committed on PVE (`/root/Projects/<project>`) so each worktree starts from a clean, up-to-date base branch:
```bash
ssh Antigravity "cd /root/Projects/<project> && git status --short && git add . && git commit -m 'chore(auto): Pre-handoff Night Shift checkpoint' || true"
```

### Step 2: Queue Remaining Tasks to Descartes with `--verify` and `--auto-merge`
Compile pending well-scoped tasks from `tasks/` into an automated serial pipeline on PVE.
> [!IMPORTANT]
> **Serial Execution & Mandatory Verification**: Because the Descartes Hub is shared, tasks MUST run serially at night (never in parallel) and include both `--verify "<test cmd>"` and `--auto-merge` (automatic squash merge into the base branch once verification passes).

Launch the unattended runner in background on PVE:
```bash
ssh Antigravity 'bash -s' << 'EOF'
cat > /tmp/descartes_night_runner.sh << 'RUNNER'
declare -A PROMPTS=(
  ["<task_a>"]="<Prompt A>"
  ["<task_b>"]="<Prompt B>"
)
for task in <task_a> <task_b>; do
  bash ~/.gemini/config/scripts/descartes_watchdog.sh \
    -t "$task" \
    -d "/root/Projects/<project>" \
    -p "${PROMPTS[$task]}" \
    --verify "<test cmd>" \
    --auto-merge
  if [ "$(grep -c DONE /tmp/${task}.signal)" -eq 0 ]; then
    echo "Task $task failed, stopping pipeline."
    break
  fi
done
RUNNER
nohup bash /tmp/descartes_night_runner.sh > /tmp/descartes_night_shift.log 2>&1 &
EOF
```

### Step 3: Inform Princess & Rollback Safety
Inform Princess that Night Shift is handed off to the Descartes autonomous pipeline with automated squash merging.
- **Next Morning**: Princess reviews `git log` on PVE (or via Mutagen sync on Mac) to inspect all merged commits.
- **Rollback Guarantee**: Each task is merged as a single squash commit (`feat(descartes): <Task_ID>`). Any suboptimal task can be 100% cleanly reverted via `git revert <commit_hash>`, and any failed task leaves its `descartes/<Task_ID>` branch intact for review.

---

## Path B: Google Remote Agent Autonomous Pipeline (`remote_watchdog.sh --autonomous --auto-merge -a <account>`)

> [!TIP]
> **Cloud-Scale Execution with Multi-Account Quota Isolation**: `remote_watchdog.sh` launches Google Antigravity Remote Agents (`agy --remote-agent`) from PVE, automatically injects `IRON_RULES.md`, guards `/usr/local/bin/agy-account switch` with a `flock` mutex, enforces Defenses 1–3 against stalls, and squash-merges PRs on GitHub.

### Step 1: Distill Context & Select Account
1. Query `kb_search` for the target project and synthesize architectural constraints into each task prompt.
2. Choose the PVE Google account (`-a kaelina1029@gmail.com` or `-a saint.archangel.satan@gmail.com`), or alternate accounts across tasks in the queue.

### Step 2: Launch Overnight Remote Agent Pipeline on PVE
```bash
ssh Antigravity 'bash -s' << 'EOF'
cat > /tmp/remote_night_runner.sh << 'RUNNER'
declare -A PROMPTS=(
  ["<task_a>"]="<Distilled Prompt A>"
  ["<task_b>"]="<Distilled Prompt B>"
)
declare -A ACCOUNTS=(
  ["<task_a>"]="kaelina1029@gmail.com"
  ["<task_b>"]="saint.archangel.satan@gmail.com"
)
for task in <task_a> <task_b>; do
  bash ~/.gemini/config/scripts/remote_watchdog.sh \
    -t "$task" \
    -r "catclever/<project>" \
    -d "/root/Projects/<project>" \
    -b "main" \
    -a "${ACCOUNTS[$task]}" \
    --tier "dev" \
    --autonomous \
    --auto-merge \
    -p "${PROMPTS[$task]}"
  if [ "$(grep -c DONE /tmp/${task}.signal)" -eq 0 ]; then
    echo "Remote Task $task failed, stopping pipeline."
    break
  fi
done
RUNNER
nohup bash /tmp/remote_night_runner.sh > /tmp/remote_night_shift.log 2>&1 &
EOF
```
*(Omit `-d "/root/Projects/<project>"` when running against a Pure-Remote repository.)*

### Step 3: Inform Princess & Rollback Safety
Inform Princess that the overnight Remote Agent pipeline is active on PVE. Each completed task produces a GitHub PR (`remote/<Task_ID>`) that is squash-merged into `main` and synced back to PVE (`git pull --rebase`).

---

## Path C: Antiverse Zellij Protocol (`antiverse-run`)

**THE PVE NEXUS ARCHITECTURE:** 
All overnight tasks, master controllers, and dispatched subagents are launched as **dedicated, isolated Zellij sessions** via `antiverse-run` (e.g., `[<project_name>] night`, `[<project_name>] dev-<task_id>`). Each workload is completely sandboxed, and Princess or the overnight controller can inspect or switch between them effortlessly via `antiverse a <target>` or pressing `Alt + s` (Zellij Session Manager).

### Phase 1: Context Gathering & Clean Up (Executed on Mac)

1. **Stop Local Watchdogs**: Kill any local "Watchdog / Dispatcher" subagents monitoring PVE tasks.
2. **Identify Running PVE Agents**: Note down the `Task ID`s of any `dev`/`ops` agents currently running on PVE.
3. **Pre-Handoff Git Checkpoint (CRITICAL)**: Because Git is authoritative on PVE, run:
   `ssh Antigravity "cd <project_dir> && git add . && git commit -m 'chore(auto): Pre-handoff Night Shift checkpoint'"`
4. **Compile Remaining Tasks**: Gather all pending tasks from `tasks/`, unrecorded tasks, and context.

### Phase 2: The Handoff (Executed on Mac)

Spawn a dedicated interactive master session `[<project_name>] night` via `antiverse-run`. 

**Important Execution Rule**: Multiline prompts over SSH are extremely prone to quoting errors and silent session crashes. You MUST write the prompt to a file first and use `sleep` as a fallback.

1. Write the following prompt to `~/.gemini/Projects/<project_name>/commands/night_shift.txt` on your local Mac:

   ```text
   /goal 宿主已下班。立刻接管对话，进入【夜间狂暴模式】。

   ### 1. 正在运行的干活小弟 (PVE本地)
   [列出当前正在 PVE 后台执行的 Task ID]
   你需要：监控这些任务对应的 tasks/<Task_ID>.md 文件。

   ### 2. 尚未执行的剩余任务与上下文
   [详细列出剩余的 Task 列表及中间产物]

   ### 3. 行动准则
   - 接力完成剩余任务。遇到报错自主重试。在应用代码前执行 git 提交！
   - 无需任何用户确认，彻夜工作！
   ```

### Tier Selection & Escalation Protocol (算力梯队与升档准则)
- **Default Tier (`--tier dev`)**: By default, Night Shift ALWAYS runs on the **`dev`** tier (`gemini-3.8-flash` with `effort: high`). This provides excellent reasoning depth, high speed, and optimal token efficiency for unattended tasks.
- **Explicit Escalation (`--tier pro`)**: Switch to **`pro`** tier (`gemini-3.1-pro` with `effort: high`) **ONLY** if Princess explicitly requests an upgrade (e.g., "用 pro 档跑", "算力拉满", "用深思档重构"). Never assume pro tier by default.

2. Execute the following local command to launch it on PVE via the standardized `antiverse-run` task runner:

   ```bash
   # Default: Dev tier (gemini-3.8-flash, effort: high)
   ssh Antigravity "antiverse-run --name '[<project_name>] night' --tier dev --cwd '<project_dir>' --force --agy -i ~/.gemini/Projects/<project_name>/commands/night_shift.txt"
   
   # If Princess explicitly requested pro tier upgrade:
   # ssh Antigravity "antiverse-run --name '[<project_name>] night' --tier pro --cwd '<project_dir>' --force --agy -i ~/.gemini/Projects/<project_name>/commands/night_shift.txt"
   ```

Once dispatched, inform Princess that the Night Shift is now running in dedicated session `[<project_name>] night` on PVE (monitor via `ssh Antigravity -t 'antiverse a night'` or `Alt + s`).

## Phase 3: Autonomous SOPs (Executed on PVE)

When the new PVE agent wakes up:
1. **The Git Checkpoint Rule**: Commit before merging (`git add . && git commit -m "chore(auto): Night Shift checkpoint"`).
2. **Infinite Loop Prevention**: If a task fails 3 consecutive times, mark it as `status: failed_needs_human`, kill the dev agent, and move on.
