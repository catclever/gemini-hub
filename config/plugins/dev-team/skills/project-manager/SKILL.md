---
name: project-manager
description: >-
  Strict guidelines and workflows for managing project directories, git status, and tasks.
  Use this skill whenever initializing a project, managing design brainstorms, or moving tasks.
---

# Project Manager Skill

This skill enforces strict rules for managing project metadata, knowledge, and tasks in a centralized location.

## 1. Centralized Management Directory
All project metadata MUST be stored in `~/.gemini/Projects/<project_name>/`.
Do NOT store `.agent/`, `task.md`, or metadata inside the project's individual working directories.

### Directory Structure
```text
~/.gemini/Projects/<project_name>/
├── IRON_RULES.md         # Absolute project ironclad rules (injected into all Sub-Agents)
├── git_status.md         # Git status for all working directories
├── docs/                 # External information, reference documents, and third-party specs
├── kb/                   # Single Source of Truth (Active schemas, architectures, gotchas)
│   └── graveyard/        # Negative Knowledge (Anti-patterns, failed solutions, and post-mortems)
├── tasks/                # Data-driven Kanban (All tasks in one flat folder)
├── design/               # Brainstorms, tentative conclusions, deprecated ideas (Date-stamped)
└── commands/             # Manually injected prompts and quick-actions (User-managed)
```

## 2. Workflows & Lifecycles

### Git Status Management (`git_status.md`)
- Whenever a new working directory is introduced, check for a `.git` repository (or parent).
- If no Git repository is found, STOP and check if the project is a PVE-Native project. If not, ask the user how to handle it.
- Record the final decision for each working directory in `git_status.md`.

### Ironclad Rules (`IRON_RULES.md`)
- This file contains absolute, non-negotiable rules for the project.
- **PVE-Native Initialization**: If the user mentions the project is synced to a PVE server or is a remote project, you MUST inject the following exact block into the `## [Global]` section of `IRON_RULES.md`:
  > **Environment**: **PVE-Native**. All heavy development tasks MUST be delegated to PVE remote agents using the `pve-dispatch` skill.
  > **Thin-Client Git**: The local Mac is a "Dumb Editor" mirrored to the PVE. Do NOT force initialize `git init` locally. All Git operations (status, commit, history) MUST be delegated exclusively to the remote PVE sub-agents.
- **Namespace Architecture**: To prevent context pollution and role confusion, `IRON_RULES.md` MUST be divided into specific headings:
  - `## [Global]`: Project-wide context (e.g., dual-repo setup, language versions).
  - `## [Main Agent]`: Orchestration rules (e.g., "After local verification, you must trigger ops to sync").
  - `## [Dev Agent]`: Strict coding and directory constraints (e.g., "Only write code to the local folder, use Swift 5").
  - `## [Ops Agent]`: Execution commands (e.g., "Use `xcodebuild`, run `git push`").
- **Injection Mandate**: You must NEVER inject the entire file into a sub-agent. You must slice the document and inject ONLY the `[Global]` section plus the specific section that matches the target agent.

### Knowledge Base (`kb/`)
- Only store **finalized, active** technical details here (e.g., active DB schemas, API specs, environment setup).
- When extracting knowledge from conversations, trigger the `extract-knowledge` skill.
- Use `kb/knowledge.md` as the primary index map for active knowledge (for legacy compatibility, check if `kb/index.md` exists and rename to `knowledge.md`).
- **The Graveyard (`kb/graveyard/`)**: This is the Negative Knowledge Base. 
  - Store post-mortems, failed approaches, and anti-patterns here. 
  - Each markdown file should describe the context, what was tried, why it failed, and what NOT to do.
  - Maintain an index at `kb/graveyard/grave.md` containing a one-sentence summary of each anti-pattern (check and migrate legacy `index.md` if present).
- **Consumption & Verification Workflow**:
  - **Design Pre-Presentation Audit**: Before presenting ANY proposal, architecture, or plan to the user, verify against `kb/knowledge.md` and `kb/graveyard/grave.md`. Redesign internally if any conflict or anti-pattern is detected.
  - **Sub-Agent Task Synthesis**: Before dispatching tasks, synthesize relevant knowledge into concrete requirements (do NOT blindly paste raw markdown files into the prompt), and explicitly instruct the sub-agent which `kb/` documents it can read.

### Task Management (`tasks/`)
- **MCP ENFORCEMENT**: You are STRICTLY FORBIDDEN from using raw file editing tools (`write_to_file`, `replace_file_content`, etc.) to create or update task markdown files. You MUST exclusively use the `kanban-task-manager` MCP tools (`list_tasks`, `create_task`, `update_task_status`, `update_task_content`).
- **Project Identifier Resolution**: The `project` parameter in the MCP tools accepts either the canonical project name (e.g. `Finnegan`) or the workspace path (e.g. `$PWD`). The MCP server internally and strictly validates it through `agy_meta.py` to locate `~/.gemini/Projects/<project_name>/tasks/`.
- Do NOT use a single `task.md` file. All tasks are managed via the MCP tools which store them in the centralized absolute path `~/.gemini/Projects/<project_name>/tasks/`.
- **Task ID (Semantic Slug Only)**: The `task_id` MUST be a pure descriptive snake_case semantic slug (e.g., `card_capture_bugu`, `auth_oauth_login`, `fix_settings_button`). 
  - **FORBIDDEN (Manual Numbering)**: You MUST NOT write sequence numbers (e.g., `_001`, `_042`, `task_1`, `01_`) in `task_id`.
  - **Automated Numbering**: All task sequence numbers are exclusively managed and assigned incrementally by the `kanban-task-manager` MCP server (e.g. `card_capture_bugu_001`). If an agent passes numbers, the MCP server will automatically strip them before assigning the canonical sequential ID.
  - **Resilient Querying**: When updating status with `update_task_status`, you may use the full assigned ID (e.g., `card_capture_bugu_001`), the bare slug (`card_capture_bugu`), or the bare task sequence number (`001` or `1`).
- **Rich Task Body & Scaffolding**: 
  - When calling `create_task`, always provide a concise, meaningful `description` summarizing the task objective, key technical solutions, or change summary.
  - The MCP server automatically scaffolds `# {title}` and status-aware sections (`## 变更概述` / `## 任务目标与背景` + checkboxes) for optimal readability when previewed or edited in Qled.
  - To log progress or append findings during execution, call `update_task_content` with `mode: 'append'`.
- **Session Tracking Lifecycle**: 
  - When creating a task using `create_task`, you MUST record the **Main User Conversation ID** in the `session` field using the format `conversation://<uuid>` if it enters the `active` status. 这能在 Antigravity 中生成可点击的链接，方便直接跳转回主对话。
  - **Sub-Agent Restriction**: Sub-agents MUST NOT update tasks directly if it involves session tracking. The Main Agent handles task updates to track its own `session` (if applicable) or passes its Conversation ID to sub-agents to pass into the MCP tool.
  - If the task is `completed`, KEEP the `session` field permanently to record which session delivered the final result.
- To update progress, simply use the `update_task_status` MCP tool. Do not move files between folders.
- **Atomic Task Logging (Quick Fixes & Detail Optimizations - Type 1)**: 
  - Quick fixes and detail optimizations (Type 1 tasks) MUST generate a task record to ensure global visibility. Do NOT leave task logging as a disconnected afterthought.
  - **Atomic Batching**: Execute the change and invoke the `create_task` MCP tool (with `status: completed`, a clear `description` summary, and current `session`) within the same tool execution sequence.
  - **Partially Addressed / Located**: If an issue is located or an optimization is partially implemented but not completed, use the `create_task` tool with `status: backlog` detailing the context/root cause in `description`.
- **Definition of Done (DoD Gatekeeper)**: Before outputting the final user-facing response, the Main Agent MUST verify: *Did any tool in this turn modify project files or system configurations? If yes, has the corresponding task card been registered in Kanban via MCP?* Any turn that modifies files without an associated Kanban task is strictly considered non-compliant.

### External Documentation (`docs/`)
- Store all external reference materials, API documentation from third parties, and collected information here.
- This separates "external inputs" from "internal designs/knowledge".

### Design & Brainstorms (`design/`)
- **Date Requirement**: Because designs change frequently, EVERY document in the `design/` folder MUST include a date identifier (e.g., in the filename like `2026-09-17_auth_idea.md` or via YAML frontmatter).
- `brainstorms/`: Use for early ideas and conceptual discussions.
- `tentative/`: Record temporary conclusions for ideas that have not yet been fully thought through (还没有完全想好的暂时性结论). This captures snapshots of the thought process before reaching a final decision.
- `deprecated/`: Archive old or superseded designs here. Use dates for archival rather than version numbers. Never delete them completely.
- When a brainstorm or tentative conclusion becomes a finalized technical requirement, distill its concrete technical specifications into a new file in `kb/`.

## 3. Legacy Migration (Initialization)
When creating a new `~/.gemini/Projects/<project_name>` directory for the first time:
- **Programmatic Naming Standard**: You MUST NEVER guess or string-manipulate the project name yourself. To find the correct centralized metadata directory for your current working directory, you MUST execute the following command:
  ```bash
  META_DIR=$(python3 ~/.gemini/Projects/agy_meta.py "$PWD")
  ```
- **Proactive Permission Authorization**: Immediately after resolving `$META_DIR`, you MUST proactively trigger the IDE's directory-level permission prompt. To do this, execute a directory listing command explicitly on the directory root (e.g., `ls -la "$META_DIR"`). Do NOT target specific files for this step. You must force the IDE to request global read/write access for the entire `$META_DIR` directory.
- Use this exact `$META_DIR` path for all your task, knowledge, and config file operations.
1. Scan all known working directories for the project.
2. If any legacy `.agent/kb/` directories are found, migrate their contents to `$META_DIR/kb/`.
3. Fully delete the legacy `.agent/` directories from the working directories.
