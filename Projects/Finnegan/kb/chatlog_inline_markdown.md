---
title: ChatLog Card Inline Markdown & Safe Link Handling
description: Documenting the inline-only Markdown parsing mechanism, participant-aware
  turn isolation, non-speaker filtering, and LLM malformed bold healing in ChatLog
  cards.
date: '2026-11-07'
---

# ChatLog Card Inline Markdown & Safe Link Handling

## 1. Architectural Strategy
To avoid disrupting screenplay layout (character cues, indented dialogue flow, fixed card dimensions of 200x190 in scattering and 420x420 in focus):
- **Inline-Only Parser**: Uses `Marked.parseInline` via `createInlineDialogueParser`, preventing block-level `#` headers, lists, or tables from breaking the screenplay visual rhythm.
- **Participant-Aware Turn Isolation**: When `participants` are known on the card (e.g. `[User, Gemini]`), `parseDialogue` restricts turn switching strictly to these identified actors, completely eliminating false speaker splits caused by colons inside numbered lists or explanatory sentences.
- **Non-Speaker Candidate Filtering**: In fallback mode without participants, lines starting with markdown list markers (`1. `, `* `, `- `), headings, blockquotes, tables, or containing sentence punctuation are prevented from becoming false speakers.
- **LLM Malformed Bold Healing**: In `fixMalformedBold`, automatically normalizes quotation-inverted bold delimiters (`“xxx”**` -> `“**xxx**”`) and balances unclosed single bold markers at sentence ends.
- **Supported Syntaxes**:
  - `inline code`
  - `**bold**`
  - `*italic*`
  - `~~strikethrough~~`
  - `[link text](url)`
  - `@Theme` or `@User` mentions (rendered as pill badges)
- **Sanitization & Safety**: Filtered through `DOMPurify.sanitize`.
- **Wails External Links**: Link clicks inside focused dialogue streams are intercepted and passed to `BrowserOpenURL(href)` (with `window.open` fallback) to prevent in-app webview navigation.
- **Scattering Preview**: Links in preview mode have `pointer-events: none` to preserve card drag and focus selection on the canvas.
