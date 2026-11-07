# Finnegan Knowledge Base

## 1. System Architecture & Build Environment

### 1.1 Wails & Linux (Debian 13 Trixie) Compilation
- **Wails CLI**: `v2.11.0` (installed at `/root/go/bin/wails`, symlinked to `/usr/local/bin/wails`).
- **Required Linux System Packages**:
  - `pkg-config`
  - `libgtk-3-dev`
  - `libwebkit2gtk-4.1-dev`
- **WebKitGTK 4.1 Build Tag**:
  - Debian 13 provides WebKitGTK 4.1 (`webkit2gtk-4.1`).
  - Wails builds must pass `-tags webkit2_41` (e.g. `wails build -tags webkit2_41`).
  - Symlinks created in `/usr/lib/x86_64-linux-gnu/pkgconfig/`: `webkit2gtk-4.0.pc -> webkit2gtk-4.1.pc` and `javascriptcoregtk-4.0.pc -> javascriptcoregtk-4.1.pc`.

### 1.2 Bugu Backend Integration
- **Package Path**: `Finnegan/bugu/...`
  - `config`: Handles `radar_targets.yml` loading and prompt target catalogs.
  - `models`: Data types for Targets, LLM Search Plans, Radar Requests/Responses.
  - `fetcher`: SearxNG client and Jina Reader markdown extractor.
  - `llm`: Gemini 3.8 Flash router (`https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent`).
  - `api`: Exposes `ExecuteRadar(cfg *config.Config, intent string) RadarResponse` and HTTP daemon handler.
- **Wails App Bindings**:
  - `App` struct in `app.go` holds `buguConfig` and binds:
    - `GetRadarTargets() []models.Target`
    - `RunRadar(intent string) api.RadarResponse`
    - `Greet(name string) string`
  - Automatically exports TypeScript definitions and bindings into `frontend/wailsjs/go/main/App.d.ts` and `frontend/wailsjs/go/models.ts`.

### 1.3 Git & Mutagen Strategy
- PVE Server `/root/Projects/Finnegan` is the authoritative Git repository.
- Mutagen ignores `.git` (`vcs: true`), `bin/`, `bugu/bugu*` binaries, `*.log`, and `node_modules/` (added 2026-10-11 — before that node_modules WAS synced and macOS/Linux native packages like `esbuild-darwin-arm64` vs `esbuild-linux-64` collided). Each side must run its own `npm install`. Changing `mutagen.yml` ignores requires recreating the session (`mutagen project terminate` + `mutagen project start`).
- Git ignores `.gitignore` includes `build/bin/`, `bin/`, `bugu/bugu*`, `*.log`, and `frontend/node_modules/`.

## 2. Bugu Volatile Memory (Temporary Cards Mechanism)

### 2.1 The "Pre-Inbox" Architecture
Bugu's discovered network contents are managed via a volatile memory pool in the Go backend, strictly segregating temporary network discoveries from the permanent Local-First SQLite (RxDB) database. This acts as a "Pre-Inbox" layer before contents are promoted to the permanent `Scattering/` directory.

### 2.2 Data Models (`cards.go`)
- **Card**: Core struct representing a piece of consciousness.
  - Fields: `ID`, `Type`, `Title`, `Content`, `SourceURL`, `CreatedAt`.
- **CardType Enum**:
  - `CardTypeLocal`: Permanent cards saved by the user (persisted to SQLite/RxDB).
  - `CardTypeRadar`: Temporary cards discovered by Bugu.
  - `CardTypeBabel`: Distilled network intelligence cards discovered by Bugu (contains `sourceUrl`, `originalText`, `translatedText`, `createdAt`).
    - *Single vs. Dual Language*: If source text matches target language, `translatedText` is empty, rendering as clean single-paragraph text without fake bilingual repetition.
    - *Desktop External Links*: Opened via Wails `BrowserOpenURL` instead of raw `<a target="_blank">`.
    - *Focus Expansion*: Text clamps are fully removed (`-webkit-line-clamp: unset`) in focus mode (420x420).
    - *Micro-timestamps*: Shows relative time badge ("刚刚", "5m 前", etc.) in the card header.

### 2.3 Backend API (`CardManager`)
- **Volatile Storage**: `tempCards map[string]Card` (lives purely in RAM, lost on restart, protecting disk space).
- **Macro 24h Expiration & Eviction (`TempCardTTL = 24 * time.Hour`)**:
  - `CleanExpiredCards() int`: Periodic purging background ticker (`10 * time.Minute`) evicting cards where `now.Sub(c.CreatedAt) > TempCardTTL`.
  - `GetTempCards() []Card`: Lazily evicts expired cards on access before returning active pool to frontend or search engine (`SearchLocalCards`).
  - `EvictTempCard(cardID string) bool`: Targeted eviction method callable via Wails IPC from frontend `metabolicInterval` upon macro TTL expiry.
- **Wails Bindings** (exposed in `app.go`):
  - `GetTempCards() []Card`: Returns the volatile pool for the frontend to render floating radar nodes.
  - `PromoteTempCard(cardID string) (*Card, error)`: Core promotion logic. Morphs a radar card's type to `local`, commits it to `<home>/Scattering/` via GlobalWatcher, and ejects it from the volatile pool.
  - `EvictTempCard(cardID string) bool`: Allows frontend to explicitly evict expired or dismissed cards from backend volatile storage.
  - `ClearTempCards()`: Allows manually flushing the volatile memory (bound to Wails UI).
  - `TestInjectBuguCard(title, content, sourceURL)`: Temporary test endpoint that injects a mock radar card.

## 3. Storage Layout & Directory Structure (Card Model)

### 3.1 Everything is a Card
- **Single Source of Truth**: Markdown files are the source of truth; RxDB/SQLite is just a reactive cache.
- **Identity via ID**: Cards are identified purely by their ULID in the YAML frontmatter (`id: ...`), not by file path. If duplicate IDs exist, the first is kept, a conflict event is emitted, and silent overwrites are strictly avoided.
- **Card States**:
  - **Volatile (RAM)**: Bugu discoveries (Temporary Cards).
  - **Scattering**: Permanent, unorganized cards stored in `<home>/Scattering/`.
  - **Weaving**: Cards associated with specific projects stored in `<home>/Weaving/<Project>/` or external directories.

### 3.2 Configuration & Layout
- **Pointer Config**: Located at `~/Library/Application Support/Finnegan/finnegan.yml`, declaring `home: <path>`.
- **System Config**: Located at `<home>/.finnegan/config.yml` (stores `external_projects`, `debounce_ms`, `bugu_max_concurrency`).
- **Data Directories**:
  - `Scattering/`
  - `Weaving/` (Internal projects)
  - `.finnegan/bases/` (Base snapshots for branches)
  - `.finnegan/cache.db` (RxDB SQLite Cache)
- **Watcher Logic**:
  - Dynamically watches `Scattering/`, `Weaving/`, and validated external projects (which must contain a `.finnegan-project` marker).
  - External files without an `id` are completely ignored (not indexed, not modified).

## 3. Storage Layout & Configuration (Everything is a Card)

### 3.1 Pointer Configuration
- Finnegan reads its root directory from the absolute pointer config at `~/Library/Application Support/Finnegan/finnegan.yml` (defaults to `~/Finnegan`). 
- All other configs, caches, and databases are strictly stored within that root `home`.

### 3.2 Directory Structure
The `<home>` directory is fully self-managed by Finnegan:
- **`Scattering/`**: The flat directory for local, unsorted, root cards. `CaptureThought` and `PromoteTempCard` write new Markdown files directly here with a ULID filename `YYYYMMDD-HHMM-<slug>.md`. 
- **`Weaving/`**: Directory containing internal projects.
- **`.finnegan/`**: System-managed directory (Never manually edit).
  - `config.yml`: Core config (includes `external_projects` registry, `debounce_ms`).
  - `cache.db`: The SQLite cache (RxDB backend), which can be rebuilt from `.md` files at any time.

### 3.3 The Watcher & External Projects
- The global File Watcher automatically derives its watch directories: `<home>/Scattering/` + `<home>/Weaving/` + any path in `external_projects`.
- Any external directory can be a project as long as it contains a `.finnegan-project` marker file.
- Finnegan only interacts with files inside external projects if they contain an `id` field in their YAML frontmatter. Non-card files in external projects are completely ignored.
- **Identity via ID**: Cards are identified strictly by their ULID. If the same ID is found in two different files, the watcher rejects the newer one and logs a conflict. No silent overrides.

## 4. Module & Configuration Architecture
- **Dual-Mode Pluggable Architecture (`=y` Built-in & `=m` Standalone `.plugin`)**: Documented in [architecture_modules.md](architecture_modules.md).
- **Module & Plugin Developer Guide**: Step-by-step developer workflow, contract checklists, and single-file `.plugin` / `plugin.yml` templates documented in [module_development_guide.md](module_development_guide.md).
- **4-Tier Config**: Global (`.finnegan/config.yml`) > Module Local > Environment > Defaults.
- **Shared Core LLM (`core/llm/`)**: Core provides unified Gemini SDK & OpenAI-compatible completion utilities (`core/llm.GenerateCompletion`, `core/llm.CleanJSONText`); modules must never cross-import another module's internal packages.

## 5. UI Architecture, Dynamic Decay & Gravitational Expansion
- **Cosmic Stage Architecture**: Documented in [card_lifecycle_and_gravity.md](card_lifecycle_and_gravity.md).
- **Universal Gravitational Cascade & Viewport Placement**: Universal Screen Cascade Law across all screens ($5 \sim 6$ cards per screen comfort capacity); dynamic viewport center $Y_{\text{center}} = \text{round}(\text{scrollExpansion} \times 300\text{px})$; new manual thoughts and recalled Bugu mother cards 100% admit to the active viewport; recursive domino downward displacement into adjacent screens ($Y += 480\text{px}$) upon saturation with collision-free Mitchell sampling; initial 1~2 Bugu results stay in active bounds while 3+ overflow to the adjacent screen.
- **Three-Tier Card Sourcing**: Local vault (`Scattering/` and `Waving/`) -> 24h In-Memory Pool -> Active 3D Stage (bounded up to 30 cards total, deepest oldest card fades out to memory pool upon overflow).
- **Dynamic Half-Life Decay & Mother Card Protection**: Multi-factor half-life based on type (latest manual VIP and active Bugu mother cards protected via `isProtectedCard` for 12h and immune to eviction), $Z$-depth (closer burns faster), queue pressure, and jitter.
- **Smooth Multi-Screen Tide & Pulsating Scroll Cue**: Downward scroll accumulates into `scrollTarget` (`scrollExpansion` spring `0.08/0.45`, dynamic max range `2.2 ~ 3.5`) with 80/20 memory-to-vault replenishment and 45s auto-collapse; 3 vertically arranged pulsating dots (`.deep-space-scroll-cue`) appear at the bottom center whenever cards exist below the current viewport (`c.y - scrollExpansion * 300 > 260`).
- **Optical 3D Geometry & Invariant Center Focus**: 200x190 soft square cards, instant upright focus modal (420x420) locked to viewport center (`y = scrollExpansion * 300`) at any scroll depth, viewport-relative edge blur/fade, and dynamic z-index elevating over Omnibar when active.
- **Universal Gravitational Fallback Engine**: Documented in [card_lifecycle_and_gravity.md](card_lifecycle_and_gravity.md). Decouples visual optical aura traces from physical 3D depth; elevated cards (via full-text search, tag recall, or command staging) receive `elevatedAt` timestamp with a 10-minute elevation protection window. On `handleWindowFocus`, expired permanent cards sink back to their intrinsic age-determined depth (`calculateIntrinsicTargetZ`) strictly enforcing the "only backward, not forward (intrinsicZ > z + 5)" rule, while visual cues (`auraTraces`, `isSearchResult`) remain intact and `UICard`'s `animSpring` smoothly interpolates depth.

## 6. Omnibar, Module Command Protocol & Aura Search Engine
- **Module Command Protocol**: Documented in [module_command_protocol.md](module_command_protocol.md). Pluggable, zero-UI command declaration for modules (`core/module/command.go`). Universal two-stage parameter assembly (`Enter 1: Pick/Lock` -> `Enter 2: Dispatch`).
- **Command Parameter Card Selection UX**: When assembling card arguments for commands like `/bugu`, candidate cards are strictly sorted in reverse chronological order (`CreatedAt` descending) across both Go storage and frontend pools. The candidate list displays a clean single-line title with ellipsis (removing body snippets for a compact Raycast/Alfred aesthetic), and search queries dynamically extract an informative context snippet around the first match (`frontend/src/lib/cardTitle.ts`) while strictly preserving complete underlying card content for module execution.
- **Local-First Full Card Search Engine**: Documented in [local_card_search_engine.md](local_card_search_engine.md). Scans 100% of local vault Markdown files (`Scattering/`, `Weaving/`) and temporary cards, completely decoupled from frontend 3D viewport limits. Smart natural substring & subsequence matching without spaces (`core/search/search.go`), 250ms input debounce.
- **Aura Search Display & 3D Cosmic Repulsion**: Documented in [aura_search_and_stage_repulsion.md](aura_search_and_stage_repulsion.md). 3D Z-axis repulsion wave preserving ambient depth for small result sets, Color Wheel Max Angular Gap algorithm for chromatic collision avoidance, multi-color conic-gradient spinning aura borders with 3-stage temporal decay, and philosophical segregation between Esc (zero memory footprint rollback) and Enter (stage consolidation & 24h memory ingestion).

## 7. Frontend & Backend Modularization Architecture & Formal Extension Rules
- **Four-Tier Decoupled Frontend & Multi-File Backend Architecture**: Documented in [frontend_architecture_and_extensions.md](frontend_architecture_and_extensions.md) and enforced in `IRON_RULES.md`.
- **Go Backend Wails Entrypoint Modularization (`package main`)**: Instead of a monolithic `app.go`, Wails-bound methods on `*App` are separated by domain responsibility into `app.go` (struct, lifecycle `startup`/`shutdown`, EventBus wiring), `app_capture.go` (Thought/Note capture & binary image assets), `app_chatlog.go` (ChatLog parsing, LLM title derivation & capture), and `app_search_cmd.go` (local search, module command dispatch, Bugu/TempCard bindings, `WatcherStorage`).
- **Frontend Layer Separation**: Canonical Types (`src/types/card.ts`) -> Pure Domain/Physics Engines & Controllers (`src/lib/*.ts`, `src/modules/bugu/buguSession.ts`) -> Autonomous Feature Components & Sub-Blocks (`src/components/*.svelte`, `src/components/omnibar/*.svelte`, `src/components/cards/*.svelte`) -> Lean Orchestrator (`src/App.svelte`).
- **Responsibility-Driven Modularization Norms (职责驱动的模块化规范)**: Rather than enforcing rigid line-count limits, files are strictly governed by Single-Responsibility and Domain Cohesion:
  - Every card type (`thought`, `chat_log`, `note`, `babel`) renders via its own dedicated `*CardBody.svelte` in `src/components/cards/`, with aura/beam visual effects isolated in `CardAuraGlow.svelte`.
  - Composite UI containers (`OmniBar.svelte`) delegate distinct visual sub-views to `src/components/omnibar/` (`AttachmentTray.svelte`, `TopActionBanner.svelte`, `CommandDropdown.svelte`, `CardCandidateDropdown.svelte`).
  - `App.svelte` delegates multi-step async workflows and timer queues to dedicated controller/helper modules (`buguSession.ts`, `stageActivity.ts`, `captureHandlers.ts`).

## 8. Card Images & Multimodal Thought Architecture

### 8.1 Storage Layout & Wails AssetServer
- **Local Storage**: Binary images saved into `<home>/assets/<timestamp>-<sha256>.<ext>` with auto-created directory.
- **Markdown Contract**: YAML frontmatter stores `images: [ <filename>, ... ]` along with body text. Preserves Markdown as the Single Source of Truth.
- **Wails Asset Streaming**: High-speed, secure `assetserver.Options.Handler` intercepting `/api/assets/*` with strict path traversal protections (`filepath.Clean`, `EvalSymlinks`, boundary check strictly inside `<home>/assets`), MIME auto-detection, and HTTP caching.

### 8.2 OmniBar Multi-modal Capture (`AttachmentTray.svelte`)
- **Interaction**: Clipboard paste (`⌘V`) image sniffing, Finder file drag-and-drop, max 4 images.
- **Display**: Autonomous bottom tray docked inside `.omnibar-box`, 52x52px thumbnails, hover delete `✕`, empty-text `Backspace` delete highlight & removal.
- **Atomicity**: `CaptureThoughtWithImages` packs text + images into a single transaction and emits `thought:captured`.

### 8.3 3D Cosmic Stage & Focus Gallery (`ThoughtCardBody.svelte` & `CardImageGallery.svelte`)
- **Scattering State (200x190)**:
  - Album glow backdrop (`filter: blur(32px) saturate(1.4); opacity: 0.68`).
  - 82px contain window (`object-fit: contain`) with zero cropping for horizontal/vertical screenshots.
  - Multi-image 3.5s auto crossfade carousel with micro-dot cues and hover pause.
- **Invariant Focus State (420x420)**:
  - Natural scroll stream (Option A): Thought text is displayed first (`thought-content.focused`), followed immediately by the natural-ratio image gallery (`CardImageGallery`), ensuring the user's reflection/thought statement takes primary focus with the image as contextual illustration.
  - Horizontal swipe gallery (CSS scroll-snap) for multi-image switching with desktop prev/next buttons and indicator dots.
  - Vertical frictionless overflow scroll across entire card body without secondary click/modal.

## 9. Chat Log Cards & Dialogue Screenplay Architecture

### 9.1 Data Model & Metadata Lifting
- **Card Type**: `CardTypeChatLog` (`chat_log`).
- **Zero-Loss Principle**: The original dialogue stream text is 100% preserved in the Markdown body. All timestamps within dialogue lines (such as WeChat desktop `YYYY年MM月DD日 HH:MM`) are stripped to prevent visual noise and preserve natural reading rhythm.
- **Temporal Metadata Lifting**: First parsed timestamp becomes `started_at`, and final parsed timestamp becomes `ended_at`. `created_at` defaults to `started_at`, anchoring the card's spacetime coordinate and half-life decay directly to the moment of thought emergence rather than the paste action.
- **LLM Title & Participant Derivation**: Gemini 3.8 Flash (`DeriveChatLogTitle`) is queried to derive a concise, natural topic title (<= 20 chars) and extract participant handles (`participants: [A, B]`). If LLM is unreachable or unconfigured, regex heuristic derivation smoothly falls back to conversational cues.

### 9.2 Screenplay Typography (`ChatLogCardBody.svelte`)
- **Scattering State (200x190)**:
  - Top header row with title and optional Polaroid micro stamp badge (`.polaroid-stamp`: 22x22px white photo frame, -3° tactile rotation, stacked shadow and counter badge if multi-image, with hover micro-elevation) displaying the first image thumbnail while keeping 100% of dialogue space intact.
  - Preview of first 2~3 dialogue turns, character names in monospaced uppercase, subtle speech line-indent border, bottom gradient mask fade into deep space.
- **Invariant Focus State (420x420)**:
  - Header: Title, participant handles (`A · B`), and temporal span (`HH:MM ~ HH:MM` or relative date).
  - Stream: Full screenplay typography (`.screenplay-turn`, `.screenplay-character`, `.screenplay-dialogue` with subtle 2px border-left), natural frictionless scroll with hidden scrollbar.
  - Zero Gimmicks: Strictly avoids childish message-counter badges (e.g. no "8条对白") and specialized copy buttons, remaining 100% faithful to Finnegan's pure aesthetic and global card interaction primitives.

### 9.3 OmniBar Ingestion Flow & Image Support
- **Auto-Detection (`isChatLogFormat`)**: Evaluates pasted clipboard content for conversational structures regardless of whether image attachments are present.
- **Top Banner Cue**: When active, top banner displays `⌘ ↵ 记录对话录` (或在携带附件时点亮 `⌘ ↵ 记录图文对话录`) `· ↵ 换行 · / 命令`.
- **Atomic Dispatch with Images**: Calls `CaptureChatLogWithImages(text, images)` to persist binary assets into `<home>/assets/`, write `images: [...]` into YAML frontmatter, generate ULID Markdown file in `<home>/Scattering/`, and emit `thought:captured` with `type: chat_log`.
- **Visual Presentation**: `ChatLogCardBody.svelte` seamlessly renders `CardImageGallery` alongside screenplay dialogue in 420x420 focused mode, and album glow in 200x190 scattering mode.

## 10. Multi-Screen Scroll Depth & Universal Domino Cascade Fixes

### 10.1 Multi-Screen Scroll Deadlock Fix
- **Problem**: Previously, `getMaxScrollExpansion` clamped maximum scroll expansion to $2.2$ because unstaged vault/memory cards were not yet physically present in `activeCards` at deep coordinates ($Y \ge 720$), deadlocking the scroll engine from ever staging cards beyond Screen 2.
- **Resolution**: `getMaxScrollExpansion` accepts `totalAvailable` (`localVaultPool.length + memoryPool.length + cards.length`). If `totalAvailable > 10`, max scroll scales proportionally up to $5.0$ ($2.2 + (\text{total} - 10) \times 0.12$, clamped at $5.0$).

### 10.2 Screen 1 Draining & Zone Jumping Elimination
- **Problem**: When `explicitTargetY` was passed, `calculateSpatialPlacement` still generated 4 dynamic screen zones. When Screen 1 had 5 cards, density caused the Mitchell best-candidate search to break in Screen 2, while `applyCascade` also moved an existing card to Screen 2, draining Screen 1 to 0 cards on startup.
- **Resolution**: When `explicitTargetY !== undefined`, `screenZones` is strictly confined to `[{ minY: explicitTargetY - 240, maxY: explicitTargetY + 240, centerY: explicitTargetY }]`, with fallback centered at `viewCenterY`. Screen 1 retains 6 cards on initial load, and cards cascade smoothly downward. Stale coordinates clobbering in `App.svelte` `replenishStage` was replaced with direct assignment `cards = res.updatedCards`.
- **Bugu Mother Card Summoning**: If `startBuguRadar` is called and the mother card is currently in `localVaultPool` or `memoryPool` (or farther than $260\text{px}$ from current viewport), it is summoned immediately into the active viewport coordinates.

## 11. Force Refresh Shortcuts & Thought Card Timestamp

### 11.1 Force Refresh / Hard Reload (`Cmd+Shift+R`, `Ctrl+Shift+R`, `Shift+F5`)
- `handleWindowKeydown` in `App.svelte` strictly binds `(metaKey || ctrlKey) && e.shiftKey && key === 'r'` as well as `e.shiftKey && key === 'F5'` to `window.location.reload()`. Unshifted `Cmd+R`/`Ctrl+R` are ignored to prevent accidental reloading during typing or browsing.
- Search session restoration in `OmniBar.svelte` is bound to `Esc` (`按 Esc 还原全部卡片`), eliminating shortcut collisions with standard browser/system refresh keys.

### 11.2 Thought Card Timestamp Display (`ThoughtCardBody.svelte`)
- Both scattering state ($200\text{px} \times 190\text{px}$) and focused state ($420\text{px} \times 420\text{px}$) render `thoughtTime` (`.card-time`).
- In scattering state, `.thought-footer` sits neatly at the bottom right (`margin-top: auto; padding-top: 4px;`) displaying relative/short dates (e.g. `刚刚`, `5m 前`, `2h 前`, `10/17 14:20`), providing an intuitive stream-of-consciousness temporal anchor.

## 12. Multi-Dimensional Keyword Cognitive Engine & Facet-Driven Bugu Search

### 12.1 Built-in Keyword Cognitive Engine (`core/keywords`)
- **Cognitive vs. Execution Decoupling**: Keyword extraction is isolated from search and network layers. The Keyword Engine acts as the sole "comprehender", extracting semantic facets and persisting them directly to the Markdown YAML frontmatter (`keywords:`).
- **The 4 Real-World & Spiritual Anchor Dimensions (实心锚点体系)**:
  - All keywords MUST be discrete, concrete anchors (2~5 Chinese characters, or 1~3 English words; mood strictly 2~4 characters). Long sentences, explanatory prose, or clinical psychiatric tags are strictly prohibited.
  - `object` (名物与通用指涉): Tangible objects, roles, people, books, tools, food, places, and tech frameworks. Encompasses both proper nouns and common everyday referents (e.g. `菜市场`, `叔叔`, `外卖员`, `设计师`, `猫`, `前端`, `老白茶`, `Claude`, `Colab`).
  - `motif` (处境与母题): Classic life, dialogue, and work tropes or behavioral action slices recurring in human experience (e.g. `逃席`, `吐槽模型`, `创造需求`, `薅羊毛`, `额度焦虑`, `熟人借钱`, `深夜排错`).
  - `mood` (心境与心绪): Crystallized 2~4 character nouns capturing affective states, aesthetic vibes, and existential textures (e.g. `吐槽欲`, `通透`, `松弛感`, `抽离感`, `戏谑`, `会心一笑`, `物哀`, `安宁`).
  - `concept` (观念与议题): Core thought handles, philosophical tensions, and argument pivots (e.g. `伪提效`, `存量陷阱`, `机械迎合`, `以Bug改Bug`, `前端即逻辑`, `朋友圈人设`).
  - Full backward-compatibility alias mapping supported (`entity->object`, `event/symptom->motif`, `emotion/metaphor->mood`, `judgment/question/methodology->concept`).
- **Adaptive Salience Gating**: Two-in-one Gemini 3.8 Flash prompt evaluates active dimensions. Inactive or irrelevant facets return empty arrays and are purged before frontmatter serialization, preventing category noise.
- **Lossless YAML Frontmatter Round-Trip (`frontmatter.go`)**: Injects/updates `keywords:` while preserving existing attributes (`id`, `created`, `images`, `tags`), comments, and raw Markdown body. Uses `watcher.GetWatcher().WriteFile(filePath, content, "keywords")` to avoid watcher infinite loops.
- **Strict Trigger Boundary**: Triggers asynchronously only on permanent local `.md` card creation (`CaptureThought`, `CaptureThoughtWithImages`, `CaptureChatLogWithImages`, `PromoteToLocal`). Never invoked on in-memory volatile temporary cards (`babel`).
- **Event Bus Integration**: Emits `bus.EventKeywordsExtracted` upon completion, notifying downstream consumers (Bugu, card relations engine, and Wails frontend `keywords:extracted`).

### 12.2 Bugu Facet-Driven Routing & Dynamic Recency (`modules/bugu`)
- **Facet-Aware Search Planning (`router.go`)**:
  - `GenerateFacetSearchPlan(intent, keywords)` injects current year (2026) and the 4 anchor dimensions into prompt.
  - **Target-Specific Query Planning (`TargetQueries`)**: Maps each selected target ID to 1-2 native queries specifically tailored to that target's domain nature and facet (e.g. object/tech terms for code/doc sites, motif/discussion for community forums, mood/concept for indie blogs/humanities platforms), preventing four-dimension query stuffing and zero-hit cross-mismatch.
  - **Context-Adaptive Multilingual Routing**: Replaced rigid minor-language quotas with topic-adaptive routing: universal tech/science/philosophy queries branch across global languages (en, zh, ru, de, fr, ja, es); localized Chinese life slices or cultural motifs prioritize Chinese, English, and culturally resonant platforms without forcing unrelated minor-language tech forums.
  - `object`: Routes to documentation, GitHub, and niche technical/cultural targets with `time_range: "year"`.
  - `motif`: Routes to live community discussion targets (HN, Reddit, V2EX, GitHub Issues) with `time_range: "month"` or `"week"`.
  - `mood`: Routes to personal web domains, IndieWeb, literary & reflective blogs with `time_range: ""` (unconstrained temporal resonance).
  - `concept`: Routes to reflective essays, Substack, LessWrong with `time_range: "year"` or unconstrained.
- **Native SearxNG Engine Parameter & Time Range Fix (`searxng.go` & `radar.go`)**:
  - `type: engine` targets (e.g. Marginalia, Wiby, IndieWeb) pass their value strictly via `&engines=<engine>` rather than appending the engine name into the search query text `q=`.
  - Targets with `PreferredEngines` automatically append `&engines=<comma_separated>`.
  - Fixed time-range override logic in `radar.go`: explicit empty string `""` in `TargetTimeRanges` successfully overrides `DefaultTimeRange`, ensuring timeless mood/concept searches are never forced into year boundaries.
- **Multimodal Summary Injection & Fallback Discovery (`radar.go`)**:
  - `ExecuteRadar` checks `keywordsOpt`. If empty, queries `ExtractKeywordsForDoc(docID)` using `GlobalWatcher.GetPathForID` and `Scattering/`/`Weaving/` directory resolution to retrieve frontmatter keywords on demand. Automatically strips manual `*` tag markers.
  - Injects card `visual_summary` (image perception) and `link_summary` (URL context) into `intent`, enabling rich multimodal thought card resonance.

### 12.3 Resonant Distillation Gating, Scheme 1 Object Standard, and Ray Matched Anchors
- **Model Separation Strategy (`config.go`)**:
  - `radar_targets.yml` and `LLMConfig` support splitting the planning model from the distillation model:
    - `router_model`: Dedicated to generating multi-lingual facet queries and target routing (defaults to `default_model` or `gemini-3.8-flash`).
    - `distiller_model`: Dedicated to high-signal extraction, translation, and anchor resonance evaluation.
  - Backward compatibility: If omitted, both seamlessly fall back to `default_model`. Default target language standardized to `"Chinese"`.
- **Scheme 1 Distillation Resonance Gating (`distiller.go` & `radar.go`)**:
  - High-signal distillation and anchor resonance verification are executed in a **single LLM call** (`DistillMarkdown`).
  - **4-Dimensional Equal Pass**: Any of `object`, `motif`, `mood`, `concept` can independently pass gating.
  - **Refined Object Quality Standard**: When matching an `object` anchor, the extracted content MUST contain substantive experience sharing, insightful perspectives, clever usage, or meaningful discussion about that core object. Pure installation/setup manuals, navigation directories, marketing/SEO fluff, or articles mentioning a generic background word in passing are strictly filtered out (`matched_anchor` set to empty string).
  - **Free-Text Intent Fallback**: If card anchors are empty/null (e.g. free-text radar or keywords not yet extracted), distill directly against `USER INTENT` extracting a concise 2-4 word core topic as `matched_anchor` instead of discarding all cards.
  - **Elimination of Snippet Retries After Rejection**: If full markdown is extracted and rejected by the LLM (`card == nil`), the anti-pattern secondary retry with Search Snippet is permanently eliminated.
  - **Extraction Fallback Gate & Protection**: Search Snippet fallback is allowed only when Jina/Reddit extraction fails or is blocked, and requires snippet length $\ge 80$ characters. Jina Reader incorporates a 256KB body limit and 15,000-rune safety truncation.
  - **Title Recovery & Spam Filter**: Populates original article title into `card.Title` (eliminating `"Babel Echo"` naming loss) and passes text through `babel.UniversalSpamFilter`.
  - **Domain Caps & URL Normalization**: Enforces max 3 candidate URLs per hostname in search queue, max 2 successfully spawned cards per hostname on stage, and normalizes URLs by stripping tracking parameters (`utm_*`) and trailing slashes.
- **Amber Ray Matched Anchor Badge (`BuguRayNetwork.svelte`)**:
  - In `BuguRayNetwork.svelte`, the golden laser ray (`BuguRayNetwork`) connecting mother and child cards renders a glowing micro-badge at 80% distance along the line: `<div class="ray-anchor-badge">「{target.matchedAnchor}」</div>`.
  - Visual styling conforms to cosmic aesthetics: pure amber luminous text (`rgba(251, 191, 36, 0.95)`), dark frosted glass background (`backdrop-filter: blur(4px)`), and delicate scale that informs without overpowering.
- **Unified Card Time Formatting Engine (`frontend/src/lib/time.ts`)**:
  - Standardized time formatting across Thought, Babel, and ChatLog cards:
    - Point time: `< 5m` ("刚刚"), `< 24h` ("今天 HH:mm"), `< 48h` ("昨天 HH:mm"), `< 30d` ("N 天前 HH:mm"), same year ("MM/DD HH:mm"), different year ("YYYY/MM/DD").
    - Easter egg: Exactly N years ago today renders as `"N 年前的今天"`.
    - Interval time: Same-day ("MM/DD HH:mm – HH:mm"), cross-day ("MM/DD HH:mm – MM/DD HH:mm"), cross-year ("YYYY/MM/DD HH:mm – YYYY/MM/DD HH:mm").
  - 100% test coverage with native `node --test` suite (`time.test.ts`).

### 12.4 Card Relationship Architecture Foundation (`.finnegan/relations.db`)
- Stored as a pure Go SQLite Property Graph in `<home>/.finnegan/relations.db`.
- Supports edge records (`source_id`, `target_id`, `relation_type`, `dimension`, `weight`, `reason`, `origin`) mirrored into an in-memory bidirectional adjacency map, supporting microsecond-level relational card summoning on the 3D stage without external graph server daemons.

## 13. Note Cards & Deterministic Memo Architecture

### 13.1 Conceptual Positioning & Dual-Track Separation
- **Thought vs. Note**:
  - `thought` / `chat_log`: Ephemeral and stream-of-consciousness, decay half-life, float in 3D Cosmic Stage (Scattering state), 4-dimensional emotional/philosophical anchors (`object`, `motif`, `mood`, `concept`), participate in Bugu deep-web radar resonance.
  - `note`: Deterministic factual memos, cheat sheets, shell commands, and configuration notes. Free of emotional attitude, high utility, zero decay.
- **Capture Staging & Reload Exclusion (生成时挂载，重载时排除)**:
  - *Immediate Capture Feedback*: Newly captured note cards (`handleCaptureNote` & `bus.EventThoughtCaptured`) are immediately staged onto the active 3D Cosmic Stage (`cards`) via `stageCandidate`, ensuring instant visual delight and immediate interactability.
  - *Cold Reload / Ambient Exclusion*: On subsequent app cold starts, page reloads (`⌘ + Shift + R`), or background stage replenishment (`replenishStageCandidates`, `fetchNewCardIntoMemory`, `getUnstagedMemoryCards`), note cards are strictly ignored (`c.type !== 'note'`). They exist purely in the local vault (`localVaultPool` & SQLite cache) and do not clutter the persistent cosmic space unless summoned via search.
- **Search Inclusion (搜索态唤醒)**: Note cards participate fully in local full-card search (`SearchLocalCards`) and Aura search. When hit by a query, they are staged with chromatic Aura borders and can be focused/navigated seamlessly.

### 13.2 Keyword/Tag Engine Bypass
- `type == "note"` explicitly bypasses the `KeywordEngine` (`ProcessCard`) in the `bus.EventThoughtCaptured` event bus subscriber.
- The YAML frontmatter remains pure (`id`, `type: note`, `created`, `updated`, `source: local`), completely eliminating Gemini LLM extraction calls and token overhead.

### 13.3 Decoupled Bugu Radar Exclusion
- **Command Parameter Contract**: `core/module/command.go` introduces `RequireKeywords: true` on `ParamSpec`.
- **Zero-Coupling Gating**:
  - Bugu declares `RequireKeywords: true` on its `card` parameter.
  - OmniBar's candidate card picker (`searchParamCards`) dynamically checks `requireKeywords` and filters out `type === 'note'` as well as cards without anchors.
  - Backend `radar.go` guards against note cards, rejecting radar execution if a note card is targeted.
  - Bugu has zero knowledge of the `note` type; exclusion is governed purely by the presence of resonant keyword anchors.

### 13.4 OmniBar Capture Flow & Extensible :note Card Type Syntax
- **Decoupling from Command System**: `note` is completely decoupled from the slash command system (`GetRegisteredCommands`). Slash commands are reserved strictly for module actions (e.g. `/bugu`), while card generation uses card-type prefix syntax.
- **Prefix Syntax (`:note `)**:
  - Format: `:cardType ` with **no leading space at start** and **exactly one trailing space**.
  - Abstracted into `frontend/src/lib/cardType.ts` (`parseCardTypePrefix`), providing an extensible prefix convention for future card types (`:todo `, `:memo `, etc.).
  - Entering `:note ` immediately engages note drafting mode without triggering Aura search or command suggestions.
- **Relaxed # Title Syntax (Header & Footer)**:
  - Supports Markdown H1 `# <title>` placed at either the first line or the last line of the input (shared across `note` and `chat_log` cards).
  - Regex relaxed to `^\s*#\s*(.+)$`: Tolerates leading indentation / whitespace (`   #标题`) and allows zero space between `#` and title text (`#Redis启动`, `#对话标题`).
  - `chatlog.ExtractHashTitle` automatically extracts `title` and cleanly strips the title line from the body content.
  - The extracted title is lifted into YAML frontmatter (`title: <title>`), used as the semantic file slug (`YYYYMMDD-HHMM-<title>.note.md`), and rendered in OmniBar's top banner: `📝 备忘「<title>」 · ↵ 换行 · Esc 取消`.
- **Keyboard Shortcuts & Multi-line Editing**:
  - `↵` (Enter): Inserts a newline, allowing clean multi-line memos, command scripts, and code snippets.
  - `⌘ ↵` (Cmd+Enter / Ctrl+Enter) & Right Submit Button: Submits and saves the note via `CaptureNote`, writes to `<home>/Scattering/YYYYMMDD-HHMM-<slug>.note.md`, injects into `localVaultPool`, and triggers a success toast (`已保存备忘`).
  - `Esc`: Closes OmniBar and cancels note drafting.

### 13.5 Dedicated Note Card Renderer & Search Focus Solidification
- **Dedicated Body Component (`NoteCardBody.svelte`)**:
  - **Scattering State (200x190)**: Renders `📝` badge, title chip (`.note-preview-title`), truncated monospace preformatted text snippet with bottom gradient mask fade, and footer timestamp.
  - **Invariant Focus State (420x420)**: Top header with `📝` badge, timestamp, and bold title (`h3.note-focused-title`); body formatted with `ui-monospace` pre-wrap (`.note-pre-content`), preserving indentations, shell commands, and multiline memos with natural scroll and hidden scrollbar.
- **Search Click Solidification (`toggleFocus`)**:
  - Clicking any search hit card automatically confirms the search view (`confirmSearchView()`) instead of reverting to the pre-search snapshot.
  - This guarantees that note cards (which only exist on stage as search hits) remain mounted in `cards`, allowing `focusedCardId` to seamlessly expand them into 420x420 focus mode without disappearing or flickering.
  - Exiting focus mode returns the card to the solidified search results; a subsequent Esc or "恢复全部" click smoothly rolls back the stage to the pre-search state.

## 14. OmniBar Capture Button & Search Result Preservation
- **Rounded Feather Quill & Dashed Writing Lines (`.omnibar-submit-btn`)**:
  - The capture button is **hidden when the OmniBar input is blurred** (`!isOmnibarFocused`) and pops into view with a smooth micro-scale animation when the input gains focus.
  - To prevent blur during click, the button traps `on:mousedown|preventDefault`, guaranteeing that mouse submission always commits seamlessly before input focus shifts.
  - **Organic Rounded Feather Plume**: Reconstructed the icon as an unmistakable, rounded feather quill (soft billowing plume curves, subtle semi-translucent vane fill `fill-opacity="0.14"`, curved central rachis stem, and delicate barb splits), eliminating any resemblance to a pencil.
  - **Dashed Writing Lines**: Directly beneath the writing nib, two lines of neat, rounded dashed strokes (`stroke-dasharray="2 3" stroke-linecap="round"`) represent the handwriting text produced on paper.
  - Hovering over the active button animates the quill into a gentle calligraphic tilt (`rotate(-7deg)` around its nib origin `20% 80%`).
  - Adapts to the bottom-right when multi-line text expands the input vertically (`align-items: flex-end`), illuminating in midnight slate (`#18181b`) for thoughts and regal violet (`#5b21b6`) for `:note ` memos.
  - Top action banner remains clean and concise, showing only contextual navigation (`↵ 换行 · / 命令` or `↵ 换行 · Esc 取消`), while the button conveys its shortcut via hover tooltip (`title="录入 (⌘↵)"` / `title="保存备忘 (⌘↵)"`).
- **Search Action Terminology (`保留搜索结果`)**:
  - The probe resonance commit action was renamed from "确认搜索" to "保留搜索结果" (`⇧ ↵ 保留搜索结果`), reflecting the action's true semantic intent of preserving matching search hits onto the active 3D stage while retaining Esc for stage restoration.

## 15. Writing Paper Sheet Mode & Search Suppression (`WritingPaper.svelte`)
- **Architectural Isolation (`src/components/omnibar/WritingPaper.svelte`)**:
  - In strict compliance with composite decomposition norms, the immersive writing sheet is fully encapsulated into an autonomous sub-component rather than bloating `OmniBar.svelte`.
  - `OmniBar.svelte` functions purely as a lean orchestrator, dynamically toggling between the compact capsule and the expanded paper sheet via `isWritingMode`.
- **Expansion Criteria & Thresholds**:
  - Triggers when input content (excluding `:note ` prefix) reaches $\ge 80$ characters, or when multi-line breaks reach $\ge 4$ lines (with text $> 10$ characters).
  - Explicitly bypassed during slash command navigation (`commandSelectMode` or `commandParamMode`).
- **Complete Search Suppression (搜索熔断机制)**:
  - Long prose paragraphs are nearly impossible to meaningfully match against existing cards via fuzzy substring/subsequence search.
  - When in Writing Paper Mode, `onFreeSearch` is completely suppressed. Any pre-existing active search probes are immediately reverted, eliminating background search overhead and preventing 3D stage jitter during long-form composition.
- **Paper Skeuomorphic Physics & Tactile Texture (`Task 086`)**:
  - **Elimination of Literal Badges (去标签化物理隐喻)**:
    - Completely removed artificial badge labels (such as `📜 写作信笺` or `📝 备忘便签`). A real object communicates its identity through its physical affordance, edge silhouette, and surface texture rather than explanatory signs.
    - When `:note ` contains an explicit title (`# Title`), it is styled as a quiet, calligraphic manuscript heading (`.paper-note-title`) rather than a heavy UI badge.
  - **Dog-Ear Folded Corner (右上折角物理结构)**:
    - The top-right corner features a photorealistic folded page corner (`.dog-ear-cutout`, `28px x 28px`), composed of a drop-shadowed under-crease (`.dog-ear-shadow`) and a gradient flap (`.dog-ear-flap`) with back-lighting (`clip-path: polygon(0 0, 100% 100%, 0 100%)`).
    - The container adopts an asymmetrical silhouette (`border-radius: 12px 2px 14px 14px`), where the top-right corner is crisp and squared to cradle the folded corner naturally.
  - **Manuscript Ruled Lines (格线吸附与 Local 滚动)**:
    - Features faint horizontal manuscript lines using `repeating-linear-gradient` with lines every $32\text{px}$ (`rgba(60, 80, 120, 0.07)`).
    - Applied directly to `.paper-textarea` with `background-attachment: local` and `line-height: 32px`, ensuring text baselines sit directly on the ruled lines and that the lines scroll seamlessly in lockstep with the text content.
    - Note mode (`:note `) shifts to a subtle lavender ruled tone (`rgba(124, 58, 237, 0.065)`).
  - **Ivory Parchment Tone & Layered Ambient Shadow**:
    - Replaced generic cold frosted glass with a warm ivory parchment gradient (`linear-gradient(178deg, #ffffff 0%, #fdfdfa 32%, #f7f5ed 100%)`).
    - Supported by an upper paper edge highlight (`inset 0 1px 0 rgba(255,255,255,1)`), a paper rim highlight (`inset 0 0 0 1px rgba(255,255,255,0.6)`), and floating ambient shadow (`0 20px 48px rgba(0, 0, 0, 0.22), 0 4px 14px rgba(0, 0, 0, 0.06)`).
  - **Punched Pin-Hole Margin & Graphite Pencil Stats**:
    - The top header margin line is rendered as a delicate manuscript guide line (`border-bottom: 1px solid rgba(225, 135, 135, 0.25)`) featuring a subtle punched binding hole (`.paper-pin-hole`).
    - Word and line counts are displayed in the footer as faint graphite pencil annotations (`.paper-pencil-stat`, `ui-monospace`, `color: rgba(100, 116, 139, 0.55)`), perfectly matching the physical stationery metaphor.

## 16. Global Candidate Cards 3-Tier Hierarchy & Universal Viewport Staging (`Task 087`)

### 16.1 Architectural Decoupling & 3-Tier Sourcing Engine (`src/lib/paramCandidateEngine.ts`)
- **Complete Decoupling from Bugu**:
  - Eliminated hardcoded `trigger === 'bugu'` checks and ad-hoc pool merging from `OmniBar.svelte`.
  - Replaced with a pure functional engine: `partitionCardTiers()` and `rankSearchCandidates()`.
- **The 3-Tier Sourcing Hierarchy**:
  - **Tier 1 (Current Viewport · `current_screen`)**:
    - Active stage cards (`cards`) located within the active viewport boundary ($|c.y - Y_{\text{center}}| \le 260\text{px}$, where $Y_{\text{center}} = \text{round}(\text{scrollExpansion} \times 300\text{px})$).
    - Regardless of whether they are volatile temporary network cards or local persistent cards.
    - Sorted by recency (`createdAt` / `spawnTime` descending).
  - **Tier 2 (Other Screens · `other_screens`)**:
    - Active stage cards (`cards`) located on other screens ($|c.y - Y_{\text{center}}| > 260\text{px}$).
    - Sorted by physical proximity to the active viewport ($|c.y - Y_{\text{center}}|$ ascending).
    - Tagged with dynamic relative screen index (`screenIndex`, e.g. `第2屏`).
  - **Tier 3 (Vault Archive · `vault`)**:
    - Offline cards resting in `localVaultPool` or inactive memory that are not currently mounted on the 3D stage.
    - Strictly sorted in reverse chronological order (`createdAt` descending).
- **Search Ranking Uniformity**:
  - When searching with a text query, hits are partitioned and grouped by tier priority: Tier 1 hits $\to$ Tier 2 hits $\to$ Tier 3 hits, while strictly preserving search relevance score within each tier.

### 16.2 Declarative Command Filter Contract (`core/module/command.go` & `src/types/card.ts`)
- `ParamSpec` introduces declarative contract fields:
  - `RequireKeywords bool`: Card must have extracted keywords in frontmatter.
  - `ExcludedTypes []string`: Card types to exclude (e.g. `["note"]`).
  - `AllowedTypes []string`: Explicitly permitted card types.
  - `AutoStageToViewport bool`: Whether selecting an off-screen card automatically summons it to the active screen.
- Bugu declares `RequireKeywords: true`, `ExcludedTypes: ["note"]`, `AutoStageToViewport: true`. Other modules can declare custom constraints with zero UI code.

### 16.3 Seamless Continuous Down-Scroll & Auto-Scroll (`CardCandidateDropdown.svelte`)
- **Elimination of Artificial Truncation**:
  - Removed the `length >= 6 break` hard cap in `OmniBar.svelte`.
- **Visual Section Cues & Source Badges**:
  - Clean non-selectable section dividers: `🌌 当前屏幕 (N)`, `🪐 其他屏幕 (N)`, `📜 历史归档 (N+)`.
  - Right-aligned micro-chips on each card: `[当前屏]`, `[第N屏]`, `[归档]`.
- **Fluid Keyboard & Wheel Navigation**:
  - Moving the highlight with `ArrowDown` / `ArrowUp` triggers `activeEl.scrollIntoView({ block: 'nearest', behavior: 'smooth' })`, ensuring the highlighted item is never cut off.
  - Seamlessly crosses tier dividers without extra keys or modal interruptions.
  - Reaching the bottom of the list automatically increments vault pagination and pulls the next batch of historical cards.

### 16.4 Universal Viewport Staging & Cascade Displacement (`src/lib/stageDecay.ts`)
- **`ensureCardStagedInViewport()`**:
  - Universal physical method replacing private Bugu mother-card summoning code.
  - If target card is already in the viewport ($|c.y - Y_{\text{center}}| \le 260\text{px}$), illuminates and grants VIP decay immunity ($12\text{h}$) without moving its spatial position.
  - If target card is on another screen or offline in the vault, executes Mitchell best-candidate sampling centered at $Y_{\text{center}}$, staging the card into the current screen.
  - If current screen is saturated ($\ge 6$ cards), `applyCascade` smoothly displaces the oldest non-protected card into Screen $K+1$ ($Y += 480\text{px}$), preserving single-screen comfort capacity ($5 \sim 6$ cards).

## 17. Cinematic Cosmic Depth & 3D Parallax Dynamics (`Task 094`, Scheme B)

### 17.1 Wide-Angle Non-Linear Scale Curve (`src/UICard.svelte`)
- **Scale Dynamic Range**:
  - Replaced the narrow linear scale $[0.64, 1.08]$ with an expansive **$[0.38, 1.25]$** range.
  - The ratio between nearest and farthest card expanded from $1.68\times$ to **$3.29\times$** (area ratio $> 10.8\times$).
- **Power-Law Perspective Equation**:
  $$\text{uniformScale} = 0.38 + 0.87 \times (1 - z_{\text{norm}})^{1.25}$$
  - **Foreground ($Z \approx 0 \sim 15$)**: Scales between $1.25\times$ ($250\text{px}$) and $1.09\times$ ($218\text{px}$), providing dramatic near-field presence with crystal-clear readability.
  - **Middle Depth ($Z \approx 40 \sim 60$)**: Scales between $0.85\times$ and $0.71\times$, forming distinctly visible stratified depth tiers.
  - **Distant Background ($Z \approx 80 \sim 100$)**: Gracefully contracts to $0.50\times \sim 0.38\times$ ($76\text{px} \sim 100\text{px}$), appearing as celestial memory fragments and micro-chips scattered across deep space.

### 17.2 3D Depth Displacement & Perspective Convergence
- **`translateZ` Dynamic Range**:
  - Expanded from $[-50, +100]\text{px}$ to **$[-180\text{px}, +180\text{px}]$**:
    $$z_{\text{3d}} = (100 - Z) \times 3.6 - 180$$
- **Camera Perspective Field-of-View (`CosmicStage.svelte`)**:
  - Retuned `.cards-wrapper` perspective from $1000\text{px}$ to **$800\text{px}$**, accentuating the optical convergence of distant objects.
- **Dynamic Parallax Tilt Factor**:
  - Cards further in the foreground experience greater responsive tilt during mouse displacement, producing authentic multi-plane camera parallax.

### 17.3 Deep Background Optical Tuning & Spatial Clearance
- **Depth Blur Threshold**:
  - Tuned to trigger gently at $z_{\text{norm}} > 0.60$: $\text{depthBlur} = (z_{\text{norm}} - 0.60) \times 6\text{px}$, capping total blur at $4.5\text{px}$.
- **Hover Gravitational Pull**:
  - When hovering over any distant micro-card, Svelte Spring pulls it directly to the extreme foreground: `scale: 1.10`, `z3d: 180px`, `blur: 0px`, `opacity: 1`, allowing instant effortless inspection.
- **Anti-Collision Clearance (`src/lib/stageCoords.ts`)**:
  - Adjusted `CARD_CLEARANCE` to $290\text{px} \times 270\text{px}$ to comfortably accommodate $1.25\times$ magnified foreground cards without spatial clipping.

### 17.5 Plump & Balanced Scale Tuning ($0.55 \sim 1.25$, `Task 099`)
- **Plump Perspective Equation**:
  $$\text{uniformScale} = 0.55 + 0.70 \times (1 - z_{\text{norm}})^{1.2}$$
  - **Foreground ($Z \approx 0 \sim 11$, Today)**: $\text{Scale} \approx \mathbf{1.20\times} \sim \mathbf{1.25\times}$ ($240\text{px} \sim 250\text{px}$, $z_{\text{3d}} \approx +95\text{px} \sim +115\text{px}$). 气势饱满醒目，临场感强烈。
  - **11 Days Ago ($Z \approx 55$, Recent Month)**: $\text{Scale} \approx \mathbf{0.82\times}$ ($164\text{px}$, $z_{\text{3d}} \approx -12\text{px}$). 层次分明后撤。
  - **Distant Background ($Z \approx 100$)**: $\text{Scale} \approx \mathbf{0.55\times}$ ($110\text{px}$, $z_{\text{3d}} = -120\text{px}$). 远景卡片整体更加饱满充实，维持在桌面便签与精致卡片的质感，不再过于收缩。
- **Physical `translateZ` Calibration**:
  - Balanced to $[-120\text{px}, +120\text{px}]$: $z_{\text{3d}} = (100 - Z) \times 2.4 - 120$.
  - Hover state pulls to $\text{scale: } 1.15, z_{\text{3d}}: 140\text{px}, \text{blur: } 0$.



## 18. Manual Hashtags Unification & Cognitive Dimension Routing (`Task 095`)

### 18.1 Deprecation of `tags: []` and In-Place `*` Provenance Markers
- **Unified Keywords Model**:
  - Standalone `tags: []` YAML frontmatter field is deprecated. All user-input hashtags are unified directly into `keywords:` in frontmatter.
  - Manual provenance is designated with an in-place asterisk `*` suffix (e.g. `'WebKitGTK 4.1*'`, `'松弛感*'`).
  - AI extraction and manual entries live harmoniously in the same 4-dimensional anchor structure (`object`, `motif`, `mood`, `concept`).

### 18.2 Body Sanitation & Clean Text Grammar (`StripAndExtractHashtags`)
- **Extraction & Sanitation**:
  - Standalone lines consisting purely of hashtags (e.g. `#tag1 #tag2`) and trailing hashtags at the end of thoughts (e.g. preceded by sentence-ending punctuation `。`/`.`/`!`) are completely stripped from the markdown body.
  - Inline hashtags (e.g. `#WebKitGTK 4.1`, `#跨平台UI`) have `#` stripped in place, leaving the clean tokens within the sentence (`WebKitGTK 4.1`, `跨平台UI`) to preserve natural grammatical fluency.
  - Extracted tags are routed to their known cognitive dimension:
    - `mood`: 2~4 character affective nouns (e.g. `松弛感`, `抽离感`, `吐槽欲`, `通透`, `会心一笑`, or ending with `感`/`欲`).
    - `motif`: Behavioral action slices and recurring life/work scenes (e.g. `逃席`, `吐槽模型`, `体验新玩具`, `薅羊毛`, `额度焦虑`).
    - `concept`: Thought pivots, tensions, and philosophical handles (e.g. `伪提效`, `存量陷阱`, `机械迎合`, `以Bug改Bug`, or ending with `主义`/`陷阱`).
    - `object`: Specific names, frameworks, tools, foods, places, roles, and default fallback (e.g. `WebKitGTK 4.1`, `跨平台UI`, `v1.0.0`).

### 18.3 Non-Destructive Frontmatter Merging (`MergeKeywordsToMarkdown`)
- In `core/keywords/frontmatter.go`, `MergeKeywordsToMarkdown` inspects existing frontmatter keywords before applying AI extraction:
  - Any existing manual entry ending with `*` is unconditionally preserved.
  - AI extraction never overwrites or duplicates manual `*` entries (even if the AI model extracts the identical term without `*`).
  - Dimensions containing only manual entries are retained even if AI extraction produces empty results for those dimensions.

### 18.4 Frontend Selective Display & Normalized Autocomplete
- **`ThoughtCardBody.svelte`**:
  - Only displays keywords possessing the `*` suffix (rendered cleanly as `#{kw}` without `*`).
  - Pure AI-extracted keywords are not rendered on the thought card body.
- **OmniBar Autocomplete**:
  - Aggregates all keywords and tags across local vault cards, normalizes away `*` markers (`replace(/\*+$/, '').trim()`), deduplicates, and presents them in sorted alphabetical order.

## 19. Tag Association Display Network & Resurgence Lifecycle (`Task 103`)

### 19.1 Pure Spatial Foreground Tag Visibility
- In `ThoughtCardBody.svelte`:
  - Hashtags (`#{tag}`) in scattering mode are only rendered visible when the card is in the frontmost layer (`card.z !== undefined && card.z <= 16`), or `isHovered`, or `isFocused`, or has an active resonance aura (`card.auraTraces && card.auraTraces.length > 0`).
  - Smooth visibility transitions via CSS: `opacity: 0; pointer-events: none; transition: opacity 0.25s ease;` when not matching, and `opacity: 1; pointer-events: auto;` when matching.
  - Each `#{tag}` pill is clickable (`on:click|stopPropagation`), dispatching custom event `'tagClick'` with `{ tag, cardId: card.id }`.

### 19.2 Global Vault Recall & Staging Engine
- `App.svelte` / `CosmicStage.svelte` manages `activeConstellationTag` (string | null):
  - Clicking an active tag toggles it off.
  - When activated: queries memory pool and local vault pool for cards possessing the target tag/keyword that are not currently on stage.
  - Recalls and stages matching cards into the active stage using collision-free coordinate allocation near current viewport center ($Y \approx \text{scrollExpansion} \times 300\text{px}$).

### 19.3 Resurgence Lifecycle (Elevated Staging, 2-Min Aura, and Gravitational Sinking)
- For permanent cards summoned/recalled by associative tag discovery:
  - **Initial Z**: Foreground depth $Z = 10$ (immediately entering the $\le 16$ visibility zone).
  - **Resonance Aura**: Flowing neon aura trace with color `'hsl(199, 89%, 60%)'` (#38bdf8 Ice Blue) and $120,000\text{ms}$ (2 minutes) duration.
  - **Gravitational Sinking**: Effective $Z$ depth interpolates smoothly from $Z = 10$ down to intrinsic age-determined depth $z_{\text{target}}$:
    $$z(t) = z_{\text{target}} - (z_{\text{target}} - 10) \times \left(\frac{\text{remainingMs}}{120000}\right)$$
  - After 2 minutes, the aura fades out, and as the card sinks past $Z > 16$, its tags naturally fade out.

### 19.4 Ice Blue Synapse Ray Network (`SynapseRayNetwork.svelte`)
- Renders beneath cards at `z-index: -1`, `transform: translateZ(-5px)`, `pointer-events: none`.
- Modeled with SVG Cubic Bezier curves in ethereal Ice Blue (`#38bdf8`), undirected (no arrow pulse direction).
- Triggered on:
  - `hoveredCardId`: connects hovered card with all stage cards sharing any of its tags.
  - `activeConstellationTag`: connects all pairs of stage cards possessing that tag.
- Floating glass badge `#{tag}` (10px typography) rendered at Bezier midpoint $t = 0.5$.
- Ambient constellation dimming: non-matching cards smoothly dim to `opacity: 0.35` (`transition: opacity 0.3s ease`).
- Clicking canvas background or pressing Escape / clicking active tag again clears `activeConstellationTag`.

## 20. Temporary Card Initial Depth Jitter, Metabolic Loop Relaxation & Explicit Promotion (`Task 104`)

### 20.1 Initial Z-Depth Jitter ($Z \in [20, 30]$)
- In `frontend/src/lib/stageCoords.ts` (`calculateSpatialPlacement`):
  - Previously, all newly born Bugu temporary cards were deterministically placed at $z = 85 - 65 \times 1.0 = 20.0$, creating an artificial planar clustering effect.
  - Updated formula assigns an initial random jitter in $[20, 30]$:
    $$z_{\text{initial}} = 20 + \text{Math.random()} \times 10$$
    $$z = 85 - \left(\text{ratio} \times (85 - z_{\text{initial}})\right)$$
  - Fresh discoveries ($ratio \approx 1.0$) sit staggered at $z \in [20, 30]$ in the foreground, and gradually recede toward $z \to 85$ as the 24-hr TTL elapses.

### 20.2 Metabolic Interval Relaxation (2s -> 45s)
- In `frontend/src/App.svelte`:
  - `metabolicInterval` execution cycle was increased from `2000ms` (2 seconds) to `45000ms` (45 seconds).
  - Eliminates redundant high-frequency array filtering, stage decay duration checks, and background CPU wakeups.

### 20.3 Direct Edit Interception & Explicit Promotion ("Collect" Action)
- In `frontend/src/UICard.svelte` & `frontend/src/App.svelte`:
  - **Interception of Uncollected Cards**:
    - Temporary cards (`isTemporary = card.origin === 'bugu' || card.type === 'radar' || card.isTemporary`) intercept double-click (`handleDoubleClick`) and Alt+click (`handleClick`).
    - Direct calls to `OpenCardInEditor` are strictly blocked, preventing silent disk file creation and external editor spawning.
    - Instead, a floating toast prompt appears: `需先收集` (title tooltip updated to: `需先收集卡片才能编辑`).
  - **Explicit Collect Button (`.collect-btn`, Task 104 & Task 133)**:
    - 废除原先易被误认为“下载”的下箭头收纳盒与文字标签，全面升级为纯图标圆形按钮。
    - **Scattered Hover State**: 右上角浮现 `26px × 26px` 圆形半透明磨砂按钮。
    - **Focused State (420x420 Modal)**: 右上角呈现 `32px × 32px` 圆形按钮。
    - **“翻开的书”与往里加页动效**: 默认呈现极简的“展开典籍”SVG；当鼠标悬停（Hover）时，书页图层（`.adding-page`）以弹性阻尼曲线从右上方滑入册中并优雅贴合落入书缝，生动诠释“将飘散灵感归入典籍”的仪式感。
    - **In-Place Transformation**:
      - Clicking "收集" calls `PromoteTempCard(card.id)`, generating a persistent markdown file in `<home>/Scattering/YYYYMMDD-HHMM-<slug>.md`.
      - In frontend, the card state mutates in-place (`card.origin = 'local'`, `card.isTemporary = false`, deletes `macroExpiresAt`), stripping away temporary borders and beads, unlocks standard double-click / Alt+click editing, and dispatches custom event `cardPromoted` to synchronize `cards`, `memoryPool`, and `localVaultPool` in `App.svelte`.

## 21. Focus-Driven Temporary Decay, Viewport Invariance & Universal Gravitational Fallback (`Task 106` & `Task 112`)

### 21.1 Removal of 45-Second Viewport Auto-Collapse (`Task 106`)
- In `frontend/src/App.svelte`:
  - Completely purged `tideTimer` and all `resetTideTimer()` invocations.
  - The canvas viewport coordinates strictly obey user scroll gestures; scrolling to Screen 2 or Screen 3 stays permanently locked at that depth without arbitrary timer-based auto-reversion to Screen 1.
  - Removed mid-reading stage card evaporation from `metabolicInterval`. Stage departure is strictly governed by physical space crowding and window focus events.

### 21.2 Focus-Driven Two-Stage Decay for Temporary Cards (`Task 106`)
- In `handleWindowFocus` (`window.addEventListener('focus', ...)`):
  - When returning to Finnegan, evaluates uncollected temporary cards past their half-life (`now - c.spawnTime >= c.decayDuration`):
    - **Stage 1 (Deep Space Drift)**: If $z < 65$, card steps back into deep space ($z += 20 \sim 25$), resets `spawnTime = now`, and smoothly drifts backward, shrinking with softer font colors via `animSpring`.
    - **Stage 2 (Cosmic Dissolution)**: If $z \ge 65$, gracefully triggers `isFadingOut = true` and dissolves into stardust, returning to `memoryPool`.

### 21.3 Universal Gravitational Fallback Engine for Permanent Cards (`Task 112` & `Task 118`, `gravityFallback.ts`)
- **Strict 4-Phase Unlock-Extinction-Cooldown Sequence (`Task 118`)**:
  1. *Phase 1 (Locked State · Light On)*: As long as any optical aura (search neon/glow, tag ice blue highlight) is active (`hasActiveAura`), the card is strictly locked in the foreground. Physical sinking is completely blocked.
  2. *Phase 2 (Unlocked Moment · Light Off)*: Optical auras possess natural lifespans (default search aura is 15 minutes, tag aura is 2 minutes). When the aura naturally expires, the light extinguishes, transitioning the card to the Unlocked state at timestamp `unlockedAt`.
  3. *Phase 3 (10-Minute Post-Extinction Cooldown)*: A quiet 10-minute cooldown window begins *after* the light extinguishes (`now < unlockedAt + 10 * 60 * 1000`). The card remains safely resting in place, preserving visual stability.
  4. *Phase 4 (Focus-Driven Sinking · "Only Backward, Never Forward")*:
     - When the window regains focus (`handleWindowFocus`) after the 10-minute post-extinction cooldown has elapsed (`now >= unlockedAt + 10m`):
     - Computes intrinsic target depth based on creation timestamp: `intrinsicZ = calculateIntrinsicTargetZ(card, now)`.
     - Strictly executes **only backward, never forward**: if `intrinsicZ > card.z + 5`, `card.z` sinks back into its historical depth via `animSpring`. Cards already in the foreground never jump forward.
- **Search Optical Stage Alignment (`UICard.svelte`)**:
  - Search aura lifecycle cleanly maps into 15-minute duration: Stage 1 (0~3m, flowing neon) -> Stage 2 (3~10m, soft glow) -> Stage 3 (10~15m, thin colored border) -> Extinguished (>15m, `hasAura = false`, `auraStage = 0`).

## 22. Focus-Driven Relative Time Refresh Mechanism (`Task 121`)
- **Implemented In**: `frontend/src/lib/time.ts`, `frontend/src/App.svelte`, `frontend/src/UICard.svelte`, `frontend/src/components/cards/*`
- **Background & Stale Temporal Drift**:
  - Finnegan's cards display intuitive relative times ("刚刚", "今天 HH:mm", "昨天 HH:mm", "2 天前 上午", "1 年前的今天").
  - Because Finnegan remains open in background workspaces across days and hours, card components previously rendered static relative strings on mount. Since card object references do not mutate upon day/time passage, Svelte reactive statements never re-executed, causing cards to stay stuck on "刚刚" or "今天" across midnight.
- **Global Reactive Stage Time Anchor**:
  - `frontend/src/lib/time.ts` exports a reactive Svelte store `stageTime: Writable<number>` and an updater `refreshStageTime(now?: number)`.
  - In `frontend/src/App.svelte`, `refreshStageTime()` is called immediately inside `handleWindowFocus()` and on `document.visibilitychange` when returning to Finnegan. It is also refreshed inside `metabolicInterval` (45s).
- **Reactive Tree Propagation**:
  - `UICard.svelte` computes `$: displayTime = getCardDisplayTime(card, $stageTime)`.
  - `VirtualCardProxy.svelte` computes `getTime(card, $stageTime)`.
  - `ThoughtCardBody.svelte`, `BabelCardBody.svelte`, `NoteCardBody.svelte`, `ChatLogCardBody.svelte` bind fallback computations to `$stageTime`.
  - As soon as the user focuses the Finnegan window, all cards on the Cosmic Stage instantly recalculate their relative time format against the current wall-clock time without requiring app reloads or card remounts.

## 23. Natural Calendar Day Temporal Hierarchy & "前天" Formatting (`Task 123`)
- **Implemented In**: `frontend/src/lib/time.ts` (`formatPointTime`)
- **Defect Analysis**:
  - 旧算法采用滚动的物理毫秒差：`diffMs < 24 * 3600 * 1000` 判为“今天”，`diffMs < 48 * 3600 * 1000` 判为“昨天”，且代码库中从未支持过“前天”（大于 48h 直接跳到“2 天前 上午”）。
  - 若用户当前在中午/下午查看（例如 12:36），前天（27日）下午或晚间撰写的卡片因时间差只有 40~45 小时（$< 48\text{h}$），全部被误归类为“昨天 HH:mm”。
- **Calendar Day Hierarchy Solution**:
  - 重构为按自然日历日（`dayDiff = round((nowMidnight - targetMidnight) / 86400000)`）严格划分：
    - `dayDiff === 0`: 今天（< 5分钟为“刚刚”，否则为“今天 HH:mm”）
    - `dayDiff === 1`: 昨天（“昨天 HH:mm”）
    - `dayDiff === 2`: **前天**（“前天 HH:mm”）
    - `dayDiff >= 3 && dayDiff < 30`: N 天前（“{dayDiff} 天前 {period}”）
  - 彻底契合人类自然日历直觉，前天撰写的任何时间段卡片均正确、统一显示为“前天 HH:mm”。

## 25. Universal Babel Module & Layered Gatekeepers Architecture (`Task 131`)
- **Background & Decoupling Rationale**:
  - Previously, Babel models and logic were tightly coupled under `modules/bugu/models/babel.go` and `modules/bugu/buguSession.ts`, despite Bluesky (ATProto) and other network discovery channels producing equivalent distilled intelligence cards.
  - Substantive card queuing, rate-limiting, and viewport-adaptive staging were trapped inside `buguSession.ts`, creating leaky abstraction boundaries.
- **Universal Base & Layered Gatekeepers (`core/babel/` & `core/models/`)**:
  - `core/models/babel.go`: Defines the universal `BabelCard` struct (`ID`, `Origin`, `Title`, `Content`, `SourceURL`, `OriginalText`, `TranslatedText`, `PublishedAt`, `AuthorName`, `AuthorAvatar`, `EchoOf`, `MatchedAnchor`, `EchoReason`, `ReplyCount`, `RepostCount`, `LikeCount`, `CreatedAt`).
  - `modules/bugu/models/babel.go`: Migrated into a type alias to `coremodels.BabelCard` for complete backward compatibility.
  - **Universal Base**:
    - `filter.go`: Foundation hygiene checks (empty string, short text, invalid UTF-8, mojibake `\uFFFD`, control character density, pure URL drainage, and SEO scam promotional keywords).
    - `translator.go`: Multi-language detection. Automatically detects Chinese (Han characters); if Chinese, leaves `translated_text` empty to eliminate fake bilingual redundancy; if foreign (English, Japanese, Russian, etc.), calls configured LLM (Gemini 3.8 Flash) to translate into natural Simplified Chinese.
  - **Layered Gatekeepers (`gatekeeper.go`)**:
    - `BuguGatekeeper`: Enforces deep markdown paragraph distillation and 4-dimensional cognitive anchor resonance (`object`, `motif`, `mood`, `concept`). Discards cards lacking a valid `MatchedAnchor`.
    - `BlueskyGatekeeper`: Enforces social spam account detection (filtering spam handles/bots), extracts lightweight anchors from hashtags (`#tag`) or keywords without forcing complex philosophical reasoning, and translates non-Chinese posts into Chinese.
- **Wails Event Normalization**:
  - Standardized as `babel:card_spawned` and `babel:session_completed`.
  - Maintains dual-dispatch compatibility with legacy `bugu:card_spawned` and `bugu:radar_completed`.
- **Frontend Decoupled Architecture (`frontend/src/modules/babel/`)**:
  - `types.ts` & `babelSession.ts`: Autonomous controller managing queue scheduling (850ms staggered interval) and viewport-adaptive staging.
  - `buguSession.ts` is refactored into a thin beacon/radar lifecycle controller delegating all card queuing to `babelSession`.
  - Both Bugu and Bluesky cards render universally via `BabelCardBody.svelte`.

## 26. Universal Cosmic Ray Network & Staggered Cascading Photon Flow (`Task 132`)
- **Geometric Abstraction (`frontend/src/lib/beamMath.ts`)**:
  - Centralized cubic Bezier curve docking and 3D z-depth scaling calculations (`computeAnimatedBeamPath`, `getCardScale`, `computeCubicBezierPoint`).
  - Unified `DOCKING_INSET_PX = 2` close-boundary clipping across all card connections.
  - Eliminated over 1,200 lines of duplicate SVG calculation and CSS styling between Bugu and Synapse networks.
- **Unified Engine (`frontend/src/components/cards/CosmicRayNetwork.svelte`)**:
  - Replaces `BuguRayNetwork.svelte` and `SynapseRayNetwork.svelte` with a single high-performance canvas mounted in `CosmicStage.svelte`.
  - Seamlessly handles Mother-Child radar rays (Bugu amber & Bluesky ice-blue) alongside Tag Synapse association rays.
- **Staggered Cascading Photon Flow (瀑布式错峰级联发光)**:
  - Solves the jarring sensation where multiple connection rays illuminated simultaneously.
  - Every connection is assigned a staggered delay (`--cascade-delay: ${index * 90}ms`), creating an organic, celestial waterfall cascading effect across the screen.
  - **Traveling Photon Pulse**: Energy particles flow from the source mother card along the cubic Bezier path toward the target card, exciting a blooming aperture glow (`cosmic-target-bloom`) upon arrival.
  - **Thematic Color Injection**:
    - Bugu discoveries: Amber gold (`#f59e0b`).
    - Bluesky & Synapse connections: Ice blue (`#38bdf8`).
- **Hover Persistence**:
  - When a mother card or tag is hovered, connected beams transition into an illuminated, looping laser state (`permanent-pulse`, `permanent-track`, `permanent-bloom`), providing uninterrupted visual clarity while inspecting connected consciousness streams.

## 27. Dual-Mode Pluggable Module Architecture & External Plugin Bridge (`Task 148` & `Task 149`)
- **Full Architectural Blueprint**: Documented in [architecture_modules.md](architecture_modules.md).
- **Developer Guide & Templates**: Documented in [module_development_guide.md](module_development_guide.md).
- **Zero-Coupling Core Host (`package main` & `core/module/`)**:
  - Removed all compile-time imports of `Finnegan/modules/*` sub-packages from `package main`.
  - Standardized `ManifestProvider` (`GetManifest() ModuleManifest`), `ActionProvider` (`ExecuteAction`), `PromoteHookProvider` (`OnCardPromoted`), and `HostAPI` (`SpawnCard`, `CompleteSession`, `EmitEvent`).
- **Dual-Mode Coexistence (`=y` Built-in & `=m` External `~/.finnegan/plugins/`)**:
  - `LoadExternalPlugins` in `core/module/external_bridge.go` loads both directory plugins (`<name>/plugin.yml`) and single-file self-contained binaries (`<name>.plugin` supporting `--finnegan-manifest`, `--finnegan-ui`, and real-time NDJSON `spawn_card` / `complete_session` streaming over stdio).
  - Frontend dynamically hydrates manifests on mount via `GetModuleManifests()` (`hydrateModuleManifests` in `promotionRegistry.ts`) and dynamically imports external card UI bundles from `/api/plugins/<name>/ui.js` (`loadExternalPluginCardComponents` in `cardRegistry.ts`).



## 28. WebCapture 网页解析服务与形态路由架构 (Tasks 163, 164, 165)

### 28.1 全局 Jina 基础设施下沉 (Task 163)
- **配置模型 (core/config/config.go)**:
  - JinaConfig 包含 APIKey 与 BaseURL（默认缺省为 https://r.jina.ai/）。
  - 支持 JINA_API_KEY 环境变量作为后备。
  - core/keywords 与 modules/bugu 统一继承并降级回退至此全局 Jina 配置。

### 28.2 WebCapture 管道与二元形态路由器 (Task 164)
- **包路径**: Finnegan/core/webcapture
  - fetcher.go: 依赖 Jina Reader 请求目标网址 Markdown。
  - **快速熔断防御 (Fail-Fast)**:
    - 401/403 触发 ErrPageProtected；
    - 429/5xx、Cloudflare 盾或人机验证触发 ErrBlocked；
    - 字符数小于 30 触发 ErrEmptyContent；
    - 只要触发快速熔断，立即中断并返回结构化错误，100% 杜绝向磁盘写脏数据。
  - router.go:
    - **对话白名单域名**: share.gemini.google/*, gemini.google.com/share/*, chatgpt.com/share/*, claude.ai/share/*, perplexity.ai/page/* 统一映射为 chat_log；
    - **内容启发式规则**: 调用 chatlog.IsChatLog(md) 检测多轮问答对话流，命中则映射为 chat_log；
    - **常规文章回退**: 其余页面统一映射为 note。
- **Wails 绑定与落盘**:
  - app_webcapture.go 暴露 CaptureURL(urlStr string) (*Card, error)。
  - 自动向 Scattering/ 写入 <time>-<slug>.chat_log.md 或 <time>-<slug>.note.md。
  - 发射 bus.EventThoughtCaptured 通知前端与 CosmicStage。

### 28.3 OmniBar 纯 URL 嗅探与连续输入交互 (Task 165)
- **严格触发边界 (frontend/src/lib/webcapture.ts)**:
  - 仅当输入文本为唯一独立的 URL (^https?://[^\s]+$) 且无图片附件时才触发 CaptureURL。
  - 若为图文混排（如带有个人感想、多词、附加图片），则绝不拦截，正常走原有 thought / chat_log 捕获流程。
- **连续输入体验**:
  - 抓取中提示 正在解析网页内容...；
  - 成功或失败均有明确 Toast 反馈；
  - 无论成功失败，输入框清空后均在 50ms 内自动重新获取焦点 (focus())，供用户无缝键入后续批注或灵感。
- [ChatLog Card Inline Markdown & Safe Link Handling](chatlog_inline_markdown.md): Documenting the inline-only Markdown parsing mechanism, participant-aware turn isolation, non-speaker filtering, and LLM malformed bold healing in ChatLog cards.
