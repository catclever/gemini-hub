---
title: Implement Global Event Bus and Watcher
status: completed
merged_at: '2026-10-11T20:01:48+08:00'
backup_suffix: .pre_event_bus.bak
known_limitations:
- Notes with custom frontmatter `id` are not removed from DB on file delete (needs
  path->docID map in watcher).
- atproto/watcher/watcher.go still exists (user-owned, untouched).
priority: high
tags:
- architecture
- refactor
- core
iteration: 4
id: task_global_event_bus
---
# Task: Global Event Bus + Global Watcher (Iteration 4 — Bug Fixes from Review)

## Context
Iteration 3 drafts are accepted in design. Main-agent review found concrete bugs. Fix ONLY these. Do not refactor anything else.

## HARD BOUNDARY
- Do NOT touch `atproto/`. Do NOT modify root `finnegan.yml`. Do NOT modify task metadata files.

## Bugs

### B1. Doc ID derivation is inconsistent (CRITICAL)
- `core/markdown` derives fallback ID with **SHA-1** of abs path (this is the ID actually stored).
- `core/watcher/watcher_task_global_event_bus.go` (~L262-264) looks up the old doc with **SHA-256** of abs path → always misses.
- `app_task_global_event_bus.go` `CaptureThought` (~L149-151) returns a **SHA-256** docID → does not match the stored card, so `radar:results.docId` points at nothing.
- Side effect: because the first lookup misses, `markdown.Parse` receives a zero `existingCreatedAt`; the second lookup (~L283-291) sets it too late. For notes without frontmatter `created`, CreatedAt drifts to the latest mod time on every save (violates "preserve CreatedAt").
- Fix: export ONE function in `core/markdown` (e.g. `markdown.FallbackID(absPath string) string`, keep SHA-1) and use it everywhere. Restructure processFile so the existing doc (by frontmatter `id` if present, else FallbackID) is loaded BEFORE `markdown.Parse` and its CreatedAt is passed in. Remove the duplicate lookup.
- `CaptureThought` must return the same ID the watcher stores.
- Test: save a no-frontmatter file twice with different mtimes → CreatedAt unchanged; CaptureThought ID == stored doc ID.

### B2. Nil bugu config crashes the app (CRITICAL)
- If `radar_targets.yml` is missing, `a.buguConfig` is nil, but `NewCaptureListener(a.buguConfig, ...)` is still started and `api.ExecuteRadar(nil, ...)` will panic inside a goroutine → whole app crashes on first Omnibar submit.
- Fix: if buguConfig is nil, do NOT start the capture listener; log once. `CaptureThought` still saves the note normally. Also add a nil-guard + `recover()` in `processEvent` that logs DocID.

### B3. Wrong frontend import paths (build breaks)
- `frontend/src/App_task_global_event_bus.svelte`: `'../../wailsjs/go/main/App.js'` → must be `'../wailsjs/go/main/App.js'` (see `App.bak.svelte`).
- `frontend/src/rxdb-ipc-storage_task_global_event_bus.ts`: `'../../wailsjs/runtime/runtime'` → `'../wailsjs/runtime/runtime'`.
- Add `CaptureThought` to `frontend/wailsjs/go/main/App.d.ts` and `App.js` (draft-suffixed) matching Wails' generated format, so `tsc` passes without running `wails generate`.

### B4. Minor
- Temp card IDs in injectFunc embed raw user text (`bugu-%s-...` with intent). Use `bugu-<docID>-<unixnano>-<i>` instead.
- `shutdown` should also close the bus (if the bus exposes Close) after the watcher.

## Verification (MANDATORY, report actual output)
In a scratch copy with drafts swapped over originals:
- `go build ./...`
- `go vet ./...`
- `go test -race -count=3 ./core/... ./bugu/...`
- `cd frontend && npm ci (or install) && npx tsc --noEmit && npm run build`
Paste the final summary lines of EACH command into your final message. Last round's log was truncated — keep the final report short and put test output at the TOP.
Clean up scratch dir.
