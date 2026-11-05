---
name: github-fork-clone
description: >-
  Use this skill whenever the user asks to fork a GitHub repository, clone a GitHub repository, or do both.
  This skill guides the agent to use the GitHub CLI (gh) to check authentication, fork the repo to the user's account, and/or clone it locally based on the user's request.
---

# GitHub Fork and/or Clone Skill

This skill automates the process of forking and/or cloning a GitHub repository using the GitHub CLI (`gh`). It can execute a fork only, a clone only, or both together.

## Prerequisites

- The `gh` CLI must be installed on the user's system.
- The user must be authenticated with GitHub via `gh`.

## Execution Steps

1. **Verify Authentication**
   Before attempting to interact with GitHub, verify that the user is logged in by running the following command. **CRITICAL**: You MUST run this (and all other `gh` commands) with `BypassSandbox: true` so it can access the macOS Keychain where the credentials are stored.
   ```bash
   gh auth status
   ```
   * If the output indicates the user is logged in, proceed to step 2.
   * If the output shows the user is NOT logged in or the token is invalid, instruct the user to run `gh auth login` in their terminal. **Wait for the user's confirmation** before proceeding.

2. **Determine Operation Mode**
   Identify what the user wants to achieve:
   * **Fork only**: The user only wants to create a fork in their GitHub account, without cloning it locally.
   * **Clone only**: The user only wants to clone an existing repository to their local machine.
   * **Fork and Clone**: The user wants to fork the repository AND clone their fork locally.

3. **Determine Target Directory (If Cloning)**
   If the operation involves cloning, determine where the repository should be cloned based on the following rules:
   * **User Specified:** If the user explicitly provided a target path, use it.
   * **Unspecified (Workspace Check):** If no path was provided, check the user's active workspaces.
     * If there is exactly 1 active workspace directory, use it as the target.
     * If there are multiple active workspace directories, use the `ask_question` tool to prompt the user to select which directory they want to clone into.

4. **Execute the Requested Operation**
   Remember to use `BypassSandbox: true` for the `run_command` tool when running `gh`. Replace `<owner>/<repo>` with the target repository provided by the user.

   * **For Fork Only**:
     ```bash
     gh repo fork <owner>/<repo>
     ```
   * **For Clone Only**:
     Change your tool's working directory (`Cwd`) to the determined target directory.
     ```bash
     gh repo clone <owner>/<repo>
     ```
   * **For Fork and Clone**:
     Change your tool's working directory (`Cwd`) to the determined target directory.
     ```bash
     gh repo fork <owner>/<repo> --clone
     ```

5. **Verify Success**
   * If cloning was involved, confirm it was successful by checking that the repository folder exists locally in the target directory (e.g., using `list_dir` or `ls -la`).
   * Inform the user that the requested operation (fork, clone, or both) has been successfully completed.
