---
title: Ignore frontend/dist in mutagen sync
status: completed
priority: low
tags:
- ops
- mutagen
- sync
id: task_mutagen_ignore_dist
---
# Retroactive log (Type 1 quick fix)

Added `frontend/dist/` to the ignore paths in `/Users/kael/Projects/Finnegan/mutagen.yml`
so PVE frontend builds are not synced back to the Mac.

## Follow-up for user
- Existing Mutagen session must be recreated for the ignore rule to take effect
  (`mutagen sync terminate Finnegan` then recreate from `mutagen.yml`). Not done by agent.
- Existing `frontend/dist/` on Mac is not deleted automatically.
- Mac-local `go build` / `wails dev` needs a local frontend build first (`go:embed all:frontend/dist`).
