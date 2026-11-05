# Graveyard Index (Anti-Patterns & Rejected Approaches)

- [AST-Rewriting WYSIWYG Editors](file:///Users/kael/.gemini/Projects/Qled/kb/graveyard/ast_rewriting_wysiwyg.md): Do NOT use AST-first block editors (BlockNote, ProseMirror, Milkdown) that parse Markdown into an internal tree and re-serialize on save, as this mutates user formatting and violates the "zero format conversion on save" requirement.
