---
title: Knowledge Management MCP Architecture
description: Dual-track cross-platform Knowledge Management MCP architecture (knowledge_mcp_server.py
  + agy_meta.py) for Mac, PVE, and Cloud Remote Agents.
date: '2026-11-06'
---

# Knowledge Management MCP Architecture (`knowledge-manager`)

## 1. Dual-Track Design Philosophy
To guarantee 100% zero-compile portability across local macOS, PVE Linux, and Google Cloud Remote Agent sandboxes (`catclever/gemini-hub`), knowledge governance operates on a dual-track architecture sharing the exact same underlying `~/.gemini/Projects/<project>/kb/` Markdown + YAML Frontmatter format:

1. **Antigravity Ecosystem (`config/scripts/knowledge_mcp_server.py`)**:
   - **Runtime**: Standalone PEP 723 Python script executed via `uv run`, homologous with `kanban_mcp_server.py`.
   - **Project Resolution**: Dynamically loads `agy_meta.py` via `PROJECTS_ROOT`, relative `../../Projects`, and `~/.gemini/Projects`, requiring an explicit `project` parameter (`<project_name>` or `$PWD`) on all tools.
   - **Zero-Compile Cloud Readiness**: Tracked directly inside `catclever/gemini-hub`, enabling instant execution on macOS (`arm64`), PVE (`Linux x86_64`), and Google Cloud Remote Agents without platform-specific Rust binaries.
2. **EnginEdge Headless Agent (`EnginEdge` Module K `src/knowledge.rs`)**:
   - Serves standalone headless runs (`enginedge run` / `enginedge bench` via Descartes Watchdog) where EnginEdge operates outside the Antigravity IDE host.

## 2. Standard MCP Tool Matrix (`knowledge-manager`)
- `kb_search(project, query="", scope="all", limit=5)`: Weighted search across `active` (`kb/*.md`) and `grave` (`kb/graveyard/*.md`), or full index overview when `query` is empty/`"*"`.
- `kb_read(project, path)`: Path-traversal-safe (`realpath`-confined) reader for knowledge and graveyard cards.
- `kb_record(project, title, summary, content, scope="active", filename="")`: Atomically writes YAML Frontmatter (`title`, `description`, `date`) + Markdown body and updates `kb/knowledge.md` or `kb/graveyard/grave.md` in place.
- `kb_audit(project, proposal)`: Pre-presentation gateway that checks technical proposals against `graveyard/` anti-patterns and active architectural constraints (supporting both English and CJK token/bigram matching).
