---
name: pure-remote-init
description: "SOP for initializing the centralized knowledge & task management environment (Projects/<project_name>/) for a Pure-Remote Project (Mode B) backed by GitHub and Google Antigravity Remote Agents."
---
# Pure-Remote Project Knowledge Environment Initialization SOP

This skill defines the standard operating procedure for initializing the centralized knowledge and task management environment (`~/.gemini/Projects/<project_name>/`) for a **Pure-Remote Project (Mode B)** — a cloud-only project with zero local source code clones on Mac or PVE.

## 1. Responsibility Boundary (User vs. Agent)

- **User's Responsibility (Prerequisites)**:
  1. Create the GitHub repository (e.g., `catclever/<project_name>`).
  2. Create a **Remote Project** inside the Antigravity IDE and attach **both** repositories in Project Resources:
     - `catclever/<project_name>` (mounted at `/workspace/<project_name>` in the cloud sandbox)
     - `catclever/gemini-hub` (mounted at `/workspace/gemini-hub` in the cloud sandbox)
- **Agent's Responsibility (This Skill)**:
  1. Scaffold the centralized metadata directory `~/.gemini/Projects/<project_name>/`.
  2. Populate `IRON_RULES.md`, `git_status.md`, `kb/knowledge.md`, and `kb/graveyard/grave.md`.
  3. Commit and push `Projects/<project_name>/` to `catclever/gemini-hub` so the cloud Remote Agent sandbox immediately receives the project's governance files.

---

## 2. Step-by-Step Initialization Workflow

### Step 1: Scaffold Centralized Metadata Directory
Determine the canonical `<project_name>` (matching the GitHub repository basename in `catclever/<project_name>`) and create the full directory tree:

```bash
PROJECT_NAME="<project_name>"
META_DIR="$HOME/.gemini/Projects/${PROJECT_NAME}"

mkdir -p \
  "${META_DIR}/kb/graveyard" \
  "${META_DIR}/tasks" \
  "${META_DIR}/design/brainstorms" \
  "${META_DIR}/design/tentative" \
  "${META_DIR}/design/deprecated" \
  "${META_DIR}/docs" \
  "${META_DIR}/commands"
```

### Step 2: Generate `IRON_RULES.md` (Pure-Remote Template)
Create `${META_DIR}/IRON_RULES.md` with the strict 4-namespace structure required by `project-manager`:

```markdown
# Project Iron Rules: <project_name>

## [Global]
- **Project**: <project_name>
- **Project-Environment**: Pure-Remote
- **GitHub-Repo**: catclever/<project_name>
- **Local-Workspace**: None (Cloud-Only via Google Antigravity Remote Project `/workspace/<project_name>`)
- **Centralized Metadata**: `/workspace/gemini-hub/Projects/<project_name>` (or `~/.gemini/Projects/<project_name>`)
- **Single Source of Truth**: The GitHub repository (`catclever/<project_name>`) is the sole authoritative codebase. Do NOT create or expect local source clones on Mac or PVE unless explicitly migrating topology.

## [Main Agent]
- **Cloud-First Execution**: When running inside the Antigravity Remote Project (`/workspace/<project_name>`), execute tasks via the cloud sandbox or sub-agents and manage `kb/` and `tasks/` in `/workspace/gemini-hub/Projects/<project_name>`.
- **PVE Watchdog Dispatch (Optional)**: When dispatching unattended tasks from Mac/PVE via `remote_watchdog.sh`, pass `-r "catclever/<project_name>"` without `-d` (Pure-Remote mode) and specify `--account <account>`.
- **Metadata Sync**: Whenever `kb/`, `tasks/`, or `IRON_RULES.md` are updated inside `/workspace/gemini-hub`, commit and push `catclever/gemini-hub` so Mac, PVE, and future cloud sandboxes stay synchronized.

## [Dev Agent]
- **Workspace Path**: `/workspace/<project_name>`
- **Directory Hygiene**: Never write `.gemini/`, `kb/`, or `tasks/` inside `/workspace/<project_name>`. All metadata lives exclusively in `/workspace/gemini-hub/Projects/<project_name>/`.
- **Task Boundary**: You are STRICTLY FORBIDDEN from modifying task markdown files in `tasks/`.

## [Ops Agent]
- **Git & PR Delivery**: Commit all verified changes to feature/task branches and push directly to `origin` (`catclever/<project_name>`).
```

### Step 3: Initialize `git_status.md` & Knowledge Indexes
Create `${META_DIR}/git_status.md`, `${META_DIR}/kb/knowledge.md`, and `${META_DIR}/kb/graveyard/grave.md`:

1. **`${META_DIR}/git_status.md`**:
   ```markdown
   # Git Status & Workspace Topology: <project_name>

   - **Environment Topology**: `Pure-Remote` (Mode B)
   - **GitHub Repository**: `https://github.com/catclever/<project_name>`
   - **Cloud Sandbox Path**: `/workspace/<project_name>`
   - **Local Mac Path**: None (Pure-Remote)
   - **PVE Server Path**: None (Pure-Remote)
   ```
2. **`${META_DIR}/kb/knowledge.md`**:
   ```markdown
   # Knowledge Base Index
   ```
3. **`${META_DIR}/kb/graveyard/grave.md`**:
   ```markdown
   # The Graveyard (Negative Knowledge Index)

   *No recorded anti-patterns or failed post-mortems yet.*
   ```

---

## 3. How the Cloud Remote Project Accesses Knowledge & Tasks

When `catclever/gemini-hub` is attached alongside `catclever/<project_name>` in the Antigravity Remote Project:

1. **Zero-Config Multi-Environment Resolution (`agy_meta.py` & MCP Servers)**:
   - `agy_meta.py`, `kanban_mcp_server.py`, and `knowledge_mcp_server.py` automatically probe `/workspace/gemini-hub/Projects` and resolve queries by project name (`<project_name>`), GitHub slug (`catclever/<project_name>`), or cloud workspace path (`/workspace/<project_name>`).
2. **Optional 1-Line Cloud Sandbox Symlink Bootstrap**:
   - If the cloud container needs global `~/.gemini` symlinks for skills, commands, and MCP scripts during a session, run:
     ```bash
     mkdir -p ~/.gemini && ln -sfn /workspace/gemini-hub/Projects ~/.gemini/Projects && ln -sfn /workspace/gemini-hub/config ~/.gemini/config && ln -sfn /workspace/gemini-hub/GEMINI.md ~/.gemini/GEMINI.md
     ```

---

## 4. Commit & Push to `catclever/gemini-hub`

After scaffolding `Projects/<project_name>/`, commit and push to `catclever/gemini-hub` so the Remote Project sandbox can pull the new project metadata immediately:

```bash
cd ~/.gemini
git add "Projects/${PROJECT_NAME}"
git commit -m "feat(projects): init pure-remote knowledge env for ${PROJECT_NAME}"
git push origin HEAD
```
