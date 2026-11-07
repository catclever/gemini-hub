---
name: descartes-dispatch
description: "SOP for handing heavy, well-scoped coding tasks on PVE projects (/root/Projects/<project>) to the Descartes + EnginEdge watchdog (descartes_watchdog.sh), async/unattended. Do NOT use for vague/exploratory work, cross-repo or large refactors, tasks needing human plan approval, or Mac-local projects."
---
# Descartes Dispatch SOP

How the Lead Architect (Main Agent, on Mac) delegates a task to `descartes_watchdog.sh` on PVE. The watchdog creates an isolated git worktree, runs the EnginEdge cloud agent (`enginedge run`), optionally verifies, commits to branch `descartes/<Task_ID>`, and signals the result. **No GitHub needed** (no push/pull).

## Engine Selection

| Engine | Where / Model | Best for | Limits |
| :--- | :--- | :--- | :--- |
| **Descartes** (this skill / `pve-dispatch` Mode A) | PVE only; cloud `deepseek-v4.1-flash`, ≤50 ReAct turns | Small/medium single-module tasks, async or night queue, non-GitHub projects | Lighter model, no plan approval, whitelisted tools, shared Hub |
| **PVE Remote Agent** (`pve-dispatch` Mode B / `remote_watchdog.sh`) | PVE launcher $\rightarrow$ Google Cloud Sandbox (`agy --remote-agent`, `gemini-3.8-flash` / `3.1-pro`) | Heavy/multi-file tasks on GitHub-backed projects, multi-account rotation (`agy-account switch` + `flock`), PR auto-merge | Requires GitHub repo & Remote Project resource mounting |
| **PVE agy** (`pve-dispatch` Mode C / `pve_watchdog.sh`) | PVE Zellij, Antigravity TUI | Interactive/large/exploratory work needing PVE-local services or hardware | Heavier, needs Mutagen |
| **Local dev subagent** (`dev-manager`) | Mac, full toolset | Exploration, multi-file refactors, anything needing a local Mac shell | Occupies Mac session |

**Rule of thumb**: well-scoped + unattended (no GitHub required) → Descartes; heavy multi-file unattended on GitHub-backed repo → PVE Remote Agent (`remote_watchdog.sh`); interactive PVE-local service work → PVE agy (`pve_watchdog.sh`); Mac-local work → `dev-manager`.
> [!NOTE]
> Descartes currently runs on **PVE only**. Mac-local mode is deferred.

## Prerequisites Checklist (PVE)
- [ ] **`enginedge` installed at `~/.cargo/bin/enginedge`** (override: `ENGINEDGE_BIN`). **MUST be verified before first use**: `ssh Antigravity 'command -v enginedge'` (empty output → STOP and tell Princess; do not dispatch).
- [ ] `~/.config/descartes/env` exists with `HUB_AUTH_TOKEN` and `DESCARTES_WS_URL` (sourced automatically). Never print its contents.
- [ ] Project at `/root/Projects/<project>` and is a git repo with the base branch committed.
- [ ] Mutagen sync active (`mutagen sync list`) so Mac edits reach PVE.
- [ ] **Fresh-checkout caveat**: the worktree has no untracked/ignored artifacts (`node_modules`, `target/`, `.venv`, bundler cache). Make `--verify` self-contained (e.g. `uv run pytest`, `cargo test`, `bundle exec rspec`), expect the first run to rebuild dependencies, and raise `--timeout` for heavy builds.
- [ ] **Commit first**: the worktree contains committed content only; uncommitted changes are invisible to the agent (watchdog only logs a warning). Commit on the PVE side or let Mutagen sync, then confirm with `ssh Antigravity 'cd <project_dir> && git status --short'`.

## Dispatch
Tasks must first be logged in Kanban via MCP (Task_ID = Kanban task name). Run in the background over SSH stdin (`bash -s` heredoc avoids nested quoting):
```bash
ssh Antigravity 'bash -s' << 'EOF'
nohup bash ~/.gemini/config/scripts/descartes_watchdog.sh \
  -t "<Task_ID>" \
  -d "/root/Projects/<project>" \
  -p "<Prompt>" \
  --verify "<test cmd>" \
  > /dev/null 2>&1 &
EOF
```
| Flag | Meaning |
| :--- | :--- |
| `-t` / `-d` / `-p` | Required: Task_ID, project dir, prompt |
| `-b <branch>` | Base branch (default: project dir's current branch) |
| `--verify "<cmd>"` | Independent check run in the worktree; **always pass it** (don't trust the agent's "done") |
| `--auto-merge` | Squash-merge into base automatically (night mode only; default stops at the branch) |
| `--profile <p>` / `--hub-url <u>` | LLM profile / Hub URL override |
| `--max-turns <N>` | Maximum reasoning turns on Hub (default 50 in EnginEdge; can raise to 60-100 for heavy tasks) |
| `--timeout <s>` | Default 3600 |
| `--keep-worktree` | Keep `/tmp/descartes_worktrees/<project>/<Task_ID>` for debugging |

Then **wait for `/tmp/<Task_ID>.signal`** (poll: `ssh Antigravity 'cat /tmp/<Task_ID>.signal'`).

## Signal Contract & Logs
- Signal file `/tmp/<Task_ID>.signal` starts with `IN_PROGRESS` / `DONE` / `FAILED` (loops use `grep -c DONE`).
- `DONE: BRANCH_READY descartes/<Task_ID> (<commits>, <diffstat>)` — default; also `(auto-merge skipped: <reason>)`.
- `DONE: MERGED <task> <sha>` — `--auto-merge` succeeded. `DONE: NO_CHANGES` — agent changed nothing (branch/worktree cleaned).
- Log: `ssh Antigravity 'tail -n 80 /tmp/descartes_<Task_ID>.log'` (live: `tail -f`).

## Failure Codes
| Code | Meaning → Action |
| :--- | :--- |
| `BAD_ARGS` | Missing/invalid flags → fix the command, re-dispatch |
| `ENGINEDGE_NOT_FOUND` | Binary missing → verify prerequisites, ask Princess to install; do not retry |
| `NOT_A_GIT_REPO` | `-d` is not a git repo → check path / `git init` + commit with Princess's OK |
| `BRANCH_EXISTS` | `descartes/<Task_ID>` already there → review it, or delete it (`git branch -D`) / use a new Task_ID |
| `WORKTREE_FAILED` | `git worktree add` failed → check base branch, `git worktree prune`, disk space |
| `ENGINEDGE_EXIT_<n>` | Agent/Hub error (worktree kept) → read log; fix prompt or Hub/token; retry max 2 |
| `TIMEOUT` | Exceeded `--timeout` → task too big: split it, then retry |
| `VERIFY_FAILED` | Tests failed (worktree + branch kept) → inspect diff/log, re-prompt narrower or take over via dev subagent |
| `COMMIT_FAILED` | Commit in worktree failed → inspect worktree (git identity, hooks) |
| `MERGE_CONFLICT` | `--auto-merge` rolled back, branch kept → resolve manually during acceptance |
| `UNEXPECTED_EXIT` | Trap fired → read log tail; check PVE disk/process state; then retry |

Same task failing 3 times → stop retrying, mark `failed_needs_human` and escalate (reroute to PVE Remote Agent / PVE agy via `pve-dispatch` or local dev via `dev-manager`).

## Acceptance Flow (Main Agent; run git on PVE inside `<project_dir>`)
1. Read the log: `ssh Antigravity 'tail -n 100 /tmp/descartes_<Task_ID>.log'`.
2. Review: `ssh Antigravity 'cd <project_dir> && git diff <base>...descartes/<Task_ID>'` (check scope creep and absence of secrets).
3. Run project tests (on PVE or after sync on Mac).
4. Merge: `git merge --squash descartes/<Task_ID> && git commit -m "feat: <Task_ID>"` (or note the `--auto-merge` outcome `DONE: MERGED`).
5. Cleanup: `git worktree prune && git branch -D descartes/<Task_ID>` (skip branch deletion if rejected but needed for reference).
6. **Update Kanban via MCP** (`update_task_status`). Only the Main Agent does this; the executing agent never touches task files.

## Night Shift Example (serial, stop on first non-DONE)
Mirrors `night-shift` Path A using Descartes with `--auto-merge`. The Hub is shared, so **never run in parallel at night**.
```bash
ssh Antigravity 'bash -s' << 'EOF'
cat > /tmp/descartes_night_runner.sh << 'RUNNER'
declare -A PROMPTS=( ["<task_a>"]="<Prompt A>" ["<task_b>"]="<Prompt B>" )
for task in <task_a> <task_b>; do
  bash ~/.gemini/config/scripts/descartes_watchdog.sh \
    -t "$task" -d "/root/Projects/<project>" -p "${PROMPTS[$task]}" \
    --verify "<test cmd>" --auto-merge
  if [ "$(grep -c DONE /tmp/${task}.signal)" -eq 0 ]; then
    echo "Task $task failed, stopping pipeline."
    break
  fi
done
RUNNER
nohup bash /tmp/descartes_night_runner.sh > /tmp/descartes_night_shift.log 2>&1 &
EOF
```
Morning: Princess syncs and reviews `git log`; each task is one squash commit, revertable with `git revert <sha>`. Failed/skipped tasks leave a `descartes/<Task_ID>` branch for review.

## Capability Limits (Be Honest With Princess)
- Model: cloud `deepseek-v4.1-flash` — **lighter than frontier Pro-tier models (`PVE Remote Agent` / `PVE agy` / `local dev`)**. Default **50 ReAct turns** per run (customizable via `--max-turns`). **No human plan-approval step.**
- Agent tools: `list_files`, `read_file`, `grep_search`, `write_file`, `append_file`, `get_outline`, `read_symbol`, `replace_symbol`, `run_verification`. Cloud intelligence: `github_repo_survey`, `github_code_search`, `doc_fetcher`, `spec_inspector`, `knowledge_store`. No arbitrary shell.
- Large files / test suites: for files >3KB, avoid single massive `write_file` calls (which risk LLM token output truncation). Write initial skeleton then chunk with `append_file` or `replace_symbol`.
- `run_verification` whitelist: `cargo`, `npm|pnpm|yarn|bun`, `pytest`, `python -m`, `bundle exec`, `go test|vet`, `make test|check`; forbids `& | ; > < \ ` $` and newlines.
- Blocked files (unreadable/unwritable): `.env*`, `*.pem`, `*.key`, `id_rsa*`, `.ssh`, `.aws`.
- Shared Hub instance: throttle parallel dispatches; serialize at night.

## Task Sizing Checklist
- [ ] One module / one concern; completable in ≲30 tool turns.
- [ ] Relevant files listed explicitly (paths, key symbols).
- [ ] Acceptance command given (also passed as `--verify`) and is on the whitelist.
- [ ] Out-of-scope stated ("do not touch X").
- [ ] Single repo; no big-bang refactor; no secrets/config files needed.
- [ ] Anything failing the above → split it, or use PVE Remote Agent / PVE agy (`pve-dispatch`) or local dev (`dev-manager`).

**Bad**: "Refactor the auth system and make it cleaner, update everything that uses it."
**Good**: "In `src/auth/token.py`, add `refresh_token(token: str) -> str` that reuses `decode()` and `encode()` in the same file; add 3 pytest cases in `tests/test_token.py` (valid, expired, malformed). Do NOT modify other modules or `pyproject.toml`. Done when `pytest tests/test_token.py` passes."
