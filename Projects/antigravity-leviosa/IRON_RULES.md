---
description: 项目的双库物理隔离铁律，防止 dev 越权修改 Git 仓库代码。
globs: *
alwaysApply: true
---

## Project Structure and Strict Isolation

This project utilizes a dual-repository isolation pattern to separate the execution environment from the Git version control environment.

- **Execution Workspace (antigravity)**: `/Users/kael/Library/Services/taichi/apps/com.google.antigravity`
  This is the live, self-use script version of the project (split into `web` and `worker`).
  
- **Version Control Workspace (antigravity-leviosa)**: `/Users/kael/Projects/antigravity-leviosa`
  This is the Git-tracked version used exclusively for commits and version control.

### 🚫 Strict Development Rules (For `dev` Agents):
1. **Modify Local ONLY**: All code writing, modifications, debugging, and file reads/writes MUST be performed ONLY in the **Execution Workspace** (`/Users/kael/Library/Services/taichi/apps/com.google.antigravity`).
2. **NO Cross-Directory Writing**: You are ABSOLUTELY FORBIDDEN from modifying, merging, or touching any files inside the Version Control Workspace (`antigravity-leviosa`).
3. **Scope of Work**: Your job is only to write code and verify it locally. You are NOT responsible for syncing files across workspaces or pushing to Git. 
4. **UI Injection Debugging**: When fixing DOM manipulation or UI injection bugs (e.g., Gemini Web UI updates breaking our hooks), DO NOT rush to blindly rewrite selectors or logic. First, analyze the potential causes (e.g., CSS class changes, SVG path updates, structural shifts). Then, request the user to provide the latest HTML structure snippet (`div` structure) of the target component. Only proceed with code changes AFTER receiving and analyzing the new DOM structure.
