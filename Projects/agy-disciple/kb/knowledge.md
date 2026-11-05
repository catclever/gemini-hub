---
description: 'Primary active knowledge index for agy-disciple'
---

# agy-disciple Knowledge Base

This document is the Single Source of Truth (SSOT) for active specifications, architectural standards, and operational guidelines for `agy-disciple`.

---

## 🎨 Visual Identity & Theme Color

* **Primary Theme Color**: `#6366F1` (**Celestial Indigo / 凌霄靛蓝**)
* **RGB**: `rgb(99, 102, 241)`
* **HSL**: `hsl(239, 84%, 67%)`
* **Design Philosophy**:
  - 融合了深空引力（Antigravity）的深邃与工程严谨（Engineering Blueprint）的秩序感；
  - 象征着主架构师全局掌控的深邃智慧，以及研发门徒严谨规范、草稿隔离、绝不越界的执行力。

---

## 📚 Active Knowledge Index

| Document | Description | Scope |
| :--- | :--- | :--- |
| [kb/upstream_sync_guide.md](file:///Users/kael/.gemini/Projects/agy-disciple/kb/upstream_sync_guide.md) | 本地私有 `dev-team` 上游改动差异比对、脱敏与开源同步 SOP 及 Meta-Prompt | 维护与持续集成 |

---

## 🏛️ Core Architecture Schemas

* **Draft Suffix Rule**: `dev` outputs `<basename>_task_<task_id>.<ext>`, `merger` renames original to `<basename>.bak.<ext>`.
* **Dual-Topology Modes**:
  - `standalone` (Default): Local-First, In-Repo metadata.
  - `server-centralized`: Remote SSH/PVE compute, Centralized metadata in `~/.gemini/Projects/<name>`.
* **Switching Entrypoint**: `configure.py` (with `--doctor` health check).
