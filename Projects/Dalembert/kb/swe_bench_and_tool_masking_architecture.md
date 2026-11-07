---
title: Frontend-Driven Tool Filtering & SWE-bench 3-Stage State Machine Architecture
description: Architecture spec for frontend-controlled cloud tool filtering, temporal
  leakage prevention, and the 3-stage SWE-bench state machine (:locate -> :reproduce
  -> :patch_and_verify).
date: '2026-11-07'
---

# Frontend-Driven Tool Filtering & SWE-bench 3-Stage State Machine Architecture

## 1. Core Architectural Principles
1. **Frontend Capability Manifest (Control Plane at Edge)**:
   - Cloud (`Dalembert` + `descartes-produit`) MUST NOT unconditionally inject all 5 OSINT tools (`GithubRepoSurvey`, `GithubCodeSearch`, `DocFetcher`, `SpecInspector`, `KnowledgeStoreTool`) into every session.
   - The `init` payload from the frontend (`EnginEdge`) governs tool mounting via:
     - `tools`: Array of edge tool schemas injected as `RemoteTool` classes.
     - `cloud_tools`: Optional array of cloud tool names to enable (whitelist). Passing `[]` disables all cloud OSINT tools. If `nil` in `architect`/`default` mode, all 5 cloud tools are enabled by default; in `swe_bench` mode, `github_repo_survey` and `github_code_search` are disabled by default to prevent temporal leakage.
     - `disabled_tools`: Optional array of tool names (or aliases like `search_code_examples`, `survey_architecture`) to explicitly mask out.
     - `mode`: Execution workflow mode (`"architect"` / `"default"` vs `"swe_bench"` / `"bug_hunter"`).

2. **Capability Tagging for Phase-based Tool Masking**:
   - Tools are classified into capability buckets:
     - `:read_local`: Read-only inspection tools (`read_file`, `grep`, `ripgrep`, `search`, `get_outline`, `list_dir`, `find_by_name`, `view_*`, etc.).
     - `:exec_sandbox`: Execution/verification tools (`bash`, `run_command`, `execute_command`, `run_test`, `pytest`, `rspec`, etc.).
     - `:write_local`: Mutation tools (`write_file`, `edit_file`, `replace_file_content`, `apply_patch`, `ast_replace`, `delete_file`, etc.).
     - `:cloud_osint`: Cloud intelligence tools (`github_repo_survey`, `github_code_search`, `doc_fetcher`, `spec_inspector`, `knowledge_store`).

3. **3-Stage SWE-bench State Machine (`Dalembert::Workflows::SweBenchWorkflow`)**:
   - **Stage 1 (`:locate` — Bug Localization Funnel)**:
     - **Allowed Tools**: `:read_local` only (strictly masks out `:write_local` and GitHub search tools).
     - **Output**: Structured `localization_report` written to context (suspect files, AST symbols, line ranges, root cause hypothesis).
   - **Stage 2 (`:reproduce` — Minimal Reproduction Verification)**:
     - **Allowed Tools**: `:read_local` + `:exec_sandbox` (plus controlled reproduction script writing if needed, while forbidding business logic edits in prompt & tool policy).
     - **Output**: `reproduction_report` confirming the bug was reproduced (Red Light observed).
   - **Stage 3 (`:patch_and_verify` — Surgical Patch & Regression Gate)**:
     - **Allowed Tools**: `:read_local` + `:write_local` + `:exec_sandbox`.
     - **Output**: Verified fix (Green Light on reproduction + existing test suite) and clean patch summary.
