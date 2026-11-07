---
name: local-to-remote-migration
description: "5-stage SOP for migrating an existing local repository on Mac into a Pure-Remote Project (Mode B), preserving metadata/theme colors in gemini-hub, terminating Mutagen sync, and safely deleting the local source directory."
---
# Local-to-Remote Project Migration SOP (`Local` $\rightarrow$ `Pure-Remote`)

This skill defines the strict, zero-data-loss 5-stage procedure for converting an existing local repository on Mac into a **Pure-Remote Project (Mode B)** and safely reclaiming local disk space.

> [!CAUTION]
> **Zero Data Loss Gate**: Never execute Stage 5 (`rm -rf <local_project_dir>`) unless Stage 1 (Git Cleanliness & Remote Push Audit) and Stage 3 (Metadata Sync to `catclever/gemini-hub`) have both succeeded with zero errors.

---

## Stage 1: Git Cleanliness & Remote Push Audit (Blocking Gate)

Before touching any metadata or deleting files, verify that 100% of the local source repository is pushed to GitHub (`catclever/<project_name>`):

1. **Verify Git Remote `origin`**:
   ```bash
   cd "<local_project_dir>"
   git remote -v
   ```
   - If no GitHub remote exists, STOP and ask the user whether to create `catclever/<project_name>` via `gh repo create "catclever/<project_name>" --private --source=. --push`.
2. **Verify Working Tree Cleanliness**:
   ```bash
   git status --porcelain
   ```
   - Must be completely empty. If untracked or modified files exist, inspect them with the user, commit them, or explicitly confirm they are disposable build artifacts.
3. **Verify Zero Stashes & Zero Unpushed Commits**:
   ```bash
   git stash list
   git fetch origin
   git status -sb
   git log --branches --not --remotes --oneline
   ```
   - Both `git stash list` and `git log --branches --not --remotes --oneline` MUST produce empty output. If any local branch has unpushed commits, push them (`git push origin --all && git push origin --tags`) before proceeding.

---

## Stage 2: Centralize Metadata & Harvest Theme Color

Ensure all project knowledge, tasks, and IDE identity settings are preserved in `~/.gemini/Projects/<project_name>/`:

1. **Resolve Centralized Metadata Directory**:
   ```bash
   META_DIR=$(python3 ~/.gemini/Projects/agy_meta.py "<local_project_dir>")
   echo "Resolved META_DIR: $META_DIR"
   ```
2. **Migrate Any Legacy `.agent/` Metadata**:
   - If `<local_project_dir>/.agent/` exists, migrate any `.agent/kb/` or `.agent/docs/` files into `$META_DIR/kb/` and `$META_DIR/docs/`, then remove `<local_project_dir>/.agent/`.
3. **Harvest Peacock / Window Theme Color (`.vscode/settings.json`)**:
   - If `<local_project_dir>/.vscode/settings.json` exists, copy it into `$META_DIR/.vscode/settings.json` and record the theme color hex code (e.g., `peacock.color` or `workbench.colorCustomizations`) inside `$META_DIR/IRON_RULES.md` so the project's visual identity is preserved.
4. **Update `IRON_RULES.md` & `git_status.md` to `Pure-Remote`**:
   - Update `$META_DIR/IRON_RULES.md` under `## [Global]` to set:
     - `Project-Environment: Pure-Remote`
     - `GitHub-Repo: catclever/<project_name>`
     - `Local-Workspace: None (Migrated to Cloud-Only /workspace/<project_name>)`
   - Update `$META_DIR/git_status.md` to record the migration date, the GitHub repository URL, and `Local-Workspace: Deleted (Pure-Remote)`.

---

## Stage 3: Sync Metadata to `catclever/gemini-hub`

Commit and push the updated project metadata directory inside `~/.gemini` so the Google Cloud Remote Agent sandbox can immediately read all historical `kb/` cards, `tasks/`, and `IRON_RULES.md`:

```bash
cd ~/.gemini
git add "Projects/<project_name>"
git commit -m "chore(projects): migrate <project_name> metadata to Pure-Remote"
git push origin HEAD
```

---

## Stage 4: Terminate Mutagen Sync (If Any)

Check whether an active or paused Mutagen sync session exists for `<project_name>` and terminate it cleanly:

```bash
mutagen sync list
# If a session matching <project_name> exists:
mutagen sync terminate "<session_name>"
```
*(If the project also had a `/root/Projects/<project_name>` clone on PVE and the user wants Pure-Remote only, ask whether to keep or remove the PVE clone as well.)*

---

## Stage 5: Delete Local Source Directory & Clean Local Project Pointer

1. **Remove the Local Source Code Directory**:
   ```bash
   rm -rf "<local_project_dir>"
   ```
2. **Clean Stale Local `file://` Entry in `~/.gemini/config/projects/*.json`**:
   - Inspect `~/.gemini/config/projects/*.json` for any file whose `projectResources` points to the deleted `file://<local_project_dir>` path.
   - Ensure `~/.gemini/Projects/<project_name>/.project_id` retains the project ID (if needed for history), and remove or update the stale local `file://` resource pointer so `agy_meta.py` resolves `<project_name>` directly via `Projects/<project_name>/`.
3. **Final Handover Reminder to User**:
   - Remind Princess to open the Remote Project in Antigravity IDE and attach **both** repositories under Project Resources:
     - `catclever/<project_name>`
     - `catclever/gemini-hub`
