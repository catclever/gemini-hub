---
title: Gemini Hub Command Log
description: Verified Git operational commands for the central gemini-hub repository
  (/Users/kael/Library/XDG_Exile/gemini).
date: '2026-11-06'
---

# Gemini Hub Operational Command Dictionary

| Operation | Working Directory | Verified Command |
| :--- | :--- | :--- |
| **Stage & Commit Central Hub** | `/Users/kael/Library/XDG_Exile/gemini` | `git -C /Users/kael/Library/XDG_Exile/gemini add -A && git -C /Users/kael/Library/XDG_Exile/gemini commit -m "<commit_message>"` |
| **Push Main to Remote (`gemini-hub`)** | `/Users/kael/Library/XDG_Exile/gemini` | `git -C /Users/kael/Library/XDG_Exile/gemini push origin main` |
| **Create & Switch Branch** | `/Users/kael/Library/XDG_Exile/gemini` | `git -C /Users/kael/Library/XDG_Exile/gemini checkout -b <branch_name>` |
| **Switch Branch** | `/Users/kael/Library/XDG_Exile/gemini` | `git -C /Users/kael/Library/XDG_Exile/gemini checkout <branch_name>` |
| **Pull Main from Remote** | `/Users/kael/Library/XDG_Exile/gemini` | `git -C /Users/kael/Library/XDG_Exile/gemini pull origin main` |
| **Merge Feature Branch** | `/Users/kael/Library/XDG_Exile/gemini` | `git -C /Users/kael/Library/XDG_Exile/gemini merge <branch_name> -m "<commit_message>"` |
| **Push Feature Branch to Remote** | `/Users/kael/Library/XDG_Exile/gemini` | `git -C /Users/kael/Library/XDG_Exile/gemini push origin <branch_name>` |
