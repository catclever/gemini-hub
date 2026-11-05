# Anti-Pattern: AST-Rewriting WYSIWYG Editors

## Context
During early brainstorming for supporting rich Typora/Notion-like typography in Qled, AST-based editors like Milkdown (ProseMirror) and BlockNote were considered.

## Why It Was Rejected
- AST-based editors parse raw `.md` files into an internal document tree and serialize the tree back to Markdown upon saving.
- This round-trip conversion inevitably alters whitespace, list bullet styles, blank lines, or strips custom/unrecognized syntax.
- The user explicitly requires **reading experience like Typora + editing experience of raw `.md` + ZERO format conversion on save**.

## What To Do Instead
- Always use a **Source-First Buffer + Decoration Layer** architecture (CodeMirror 6 `StateField` / `ViewPlugin` Decorations).
- The raw text buffer is the single source of truth and is written directly to disk on save without any format conversion.
