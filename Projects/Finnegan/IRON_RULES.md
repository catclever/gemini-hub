# Finnegan Iron Rules

## [Global]
- **Project**: Finnegan
- **Architecture**: Wails (Go Backend) + RxDB (Frontend) via Custom IPC Storage Plugin.
- **Goal**: Local-First Consciousness Stream Sandbox.
- **Environment**: **PVE-Native**. All heavy development tasks MUST be delegated to PVE remote agents using the `pve-dispatch` skill.
- **Thin-Client Git**: The local Mac is a "Dumb Editor" mirrored to the PVE. Do NOT force initialize `git init` locally. All Git operations (status, commit, history) MUST be delegated exclusively to the remote PVE sub-agents.

## [Main Agent]
- Maintain architectural purity.
- Trigger ops to sync or build when necessary.
- **Strict Compilation Rule**: Default to PVE for ALL development and compilation tasks (Go build, Wails build, npm install). NEVER compile locally on Mac unless explicitly requested by the user.

## [Dev Agent]
- Backend is Go (Wails).
- Frontend uses RxDB & Svelte.
- **Modularization & Single-Responsibility Norms (No Monolithic God Files)**:
  - Do NOT enforce rigid line-count limits; instead, strictly organize files by **Domain Responsibility & Cohesive Boundaries**:
  - **Go Backend (`main` package & `core/`/`modules/`)**:
    - `app.go` is strictly reserved for `App` struct definition, lifecycle hooks (`NewApp`, `startup`, `shutdown`), and concise event-bus subscription wiring.
    - Event-bus and file-watcher handler implementations (`onThoughtCapturedEvent`, `onWatcherFileChanged`, `onWatcherFileDeleted`) MUST reside in `app_events.go`, never as giant inline closures inside `startup()`.
    - Wails-bound domain methods on `*App` MUST be split into domain-specific files within `package main`:
      - `app_capture.go`: Thought & Note capture, slug sanitization, and binary image asset persistence (`CaptureThought`, `CaptureThoughtWithImages`, `CaptureNote`, `saveAssetImages`).
      - `app_chatlog.go`: ChatLog parsing, LLM title derivation, and capture (`ParseChatLog`, `DeriveChatLogTitle`, `ProcessChatLog`, `CaptureChatLog`, `CaptureChatLogWithImages`).
      - `app_search_cmd.go`: Local vault search, module command discovery/dispatch, Bugu & TempCard Wails bindings, and `WatcherStorage` adapter.
    - Pure domain algorithms (keyword extraction, hashtag parsing, markdown frontmatter formatting, search scoring, chatlog parsing) belong in `core/<domain>/`, never in `app*.go`.
  - **Svelte/TS Frontend (`frontend/src/`)**:
    - **Four-Tier One-Way DAG**: `src/types/` (contracts only) $\rightarrow$ `src/lib/` (pure engines & controllers, zero DOM mutation) $\rightarrow$ `src/components/` (autonomous UI blocks with scoped styles) $\rightarrow$ `src/App.svelte` (top-level state holder & IPC event bridge).
    - **Orchestrator Purity (`App.svelte`)**: `App.svelte` holds top-level reactive state, Wails `EventsOn` wiring, and thin delegators. Domain workflows (such as Bugu radar queue/beacon management in `modules/bugu/buguSession.ts`, Bluesky butterfly beacon in `modules/atproto/bskySession.ts`, tag constellation recall in `lib/tagNetwork.ts`, window focus gravity/metabolic evaluation in `lib/gravityFallback.ts`, card capture/update/promotion reconciliation in `lib/cardCapture.ts`, or stage activity tracking in `lib/stageActivity.ts`) MUST be encapsulated in dedicated controller/helper modules rather than inlined in `App.svelte`.
    - **Pluggable Card Bodies & Controls (`UICard.svelte`)**: `UICard.svelte` is strictly the 3D physical shell, spring animation, and focus container. Every card content type (`thought`, `chat_log`, `note`, `babel`, `curio`) MUST have its own dedicated body component in `src/components/cards/*CardBody.svelte`, visual effect layers belong in `src/components/cards/CardAuraGlow.svelte`, and interactive card controls/overlays (such as temporary card collection & comment strip) belong in `src/components/cards/CardCollectControl.svelte`.
    - **Composite UI Decomposition (`OmniBar.svelte` & `CosmicRayNetwork.svelte`)**: Complex composite components with distinct sub-views MUST delegate independent visual sub-blocks to `src/components/<feature>/` (e.g., `AttachmentTray.svelte`, `TopActionBanner.svelte`, `CommandDropdown.svelte`, `CardCandidateDropdown.svelte`, `TagDropdown.svelte`, `WritingPaper.svelte`), and pure text/tag/ray topological calculations MUST be placed in `src/lib/` (`tagAutocomplete.ts`, `beamMath.ts`).
  - **Incremental Feature Gate (新增特性准入禁令)**:
    - When adding a new card control/overlay, NEVER inline its DOM, state, and >20 lines of CSS into `UICard.svelte`; always create a dedicated subcomponent in `src/components/cards/`.
    - When adding a new stage-level workflow or module session, NEVER inline >30 lines of business state-machine functions into `App.svelte` or `app.go`'s `startup()`; always extract to `src/lib/`, `src/modules/<mod>/`, or `app_events.go` first.

## [Ops Agent]
- Standard Wails CLI commands for build and run.
