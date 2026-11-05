# Card Lifecycle, Dynamic Decay & Gravitational Expansion

**Location**: `~/.gemini/Projects/Finnegan/kb/card_lifecycle_and_gravity.md`  
**Status**: Active / Production  
**Implemented In**: `frontend/src/App.svelte`, `frontend/src/UICard.svelte`, `storage.go`  

---

## 1. Storage & Memory Sourcing Hierarchy

Finnegan employs a three-tier architecture to manage card discovery, memory retention, and rendering performance:

```
[Local Vault: Scattering/ & Waving/] (Disk, Persistent)
               │
               ▼ (20% during expansion or candidate fallback)
     [In-Memory Pool] (RAM, 24h Macro TTL)  ◄─── [Bugu Babel Radar Cards]
               │
               ▼ (80% prioritized during expansion & metabolic loop)
    [Active Celestial Stage] (DOM, Bounded: 8 ~ 14 cards)
```

1. **Persistent Vault (`Scattering/` and `Waving/`)**:
   - `Scattering/`: Short thoughts, fragments, captured via Omnibar.
   - `Waving/`: Longer, structured notes, outlines, and organized cards.
   - Both are scanned by `LoadLocalCards()` in `storage.go` upon startup and observed via `GlobalWatcher`.

2. **In-Memory Transient Pool (`memoryPool` & Go `tempCards`)**:
   - Holds temporary cards (Bugu Babel translations, research discoveries).
   - **Macro TTL**: **24 Hours** (`Date.now() + 24 * 3600 * 1000` / `TempCardTTL = 24 * time.Hour`).
   - Cards in this pool can cycle between stage display and memory resting multiple times without being destroyed until their macro 24h lifespan lapses.
   - **Frontend Metabolic Loop**: Every 45 seconds (`metabolicInterval`), expired cards are evicted from `memoryPool` and notified to the backend via `EvictTempCard(cardID)`.
   - **Backend Autonomous Defense**: Go `CardManager` runs a 10-minute ticker (`CleanExpiredCards()`) and performs lazy purging on access (`GetTempCards()`), preventing expired cards from persisting across frontend reloads or polluting `SearchLocalCards()`.

3. **Active Celestial Stage (`cards`)**:
   - The set of cards rendered in the 3D WebKit viewport at any given moment.
   - **Base Capacity**: `10` cards (dynamically scales to ~16 on downward expansion).

---

## 2. Dynamic Half-Life Decay Engine

When a card enters the active stage, its stage lifetime $T_{\text{decay}}$ is computed dynamically:

$$T_{\text{decay}} = T_{\text{base}} \times f(\text{Type}) \times f(\text{Depth}) \times f(\text{QueuePressure}) \times \text{RandomJitter}$$

### Parameter Specifications:
- **Baseline Stage Duration $T_{\text{base}}$**: **3.5 Hours** (`3.5 * 3600 * 1000 ms`).
- **Type Weight $f(\text{Type})$**:
  - **Latest Manual Input (Exclusive VIP)**: Protected with a 12-hour duration and immune from forced eviction. If multiple manual cards are captured sequentially, only the latest holds the VIP status; previous ones degrade to standard decay.
  - **Bugu / Network Cards**: Standard baseline ($f = 1.0$, ~3.5 hours).
  - **Local Memory Echoes**: Shorter baseline ($f \approx 0.57$, ~2.0 hours).
- **Depth Factor $f(\text{Depth})$ (Meteor vs Fixed Star)**:
  - Near foreground ($Z \approx 0$): $f(\text{Depth}) \approx 0.6$ (burns faster, exits sooner like a meteor).
  - Distant background ($Z \approx 100$): $f(\text{Depth}) \approx 1.5$ (lingers longer like a distant star).
- **Queue Pressure $f(\text{QueuePressure})$**:
  - $\max\left(0.4, \frac{1}{1 + \text{RestingMemoryCount} \times 0.12}\right)$.
  - Higher backlog of un-staged memory cards proportionally accelerates stage decay to cycle fresh cards in.
- **Random Jitter**: $\pm 20\%$ variance ($0.8 \sim 1.2$) to prevent cards from expiring simultaneously.

---

## 3. Freshness & Cosmic Depth Optics (True Optical Hierarchy)

- **Organic Cosmic Depth & Initial Jitter ($Z \in [20, 30]$ at Birth)**: Newly spawned Bugu Babel cards are assigned an initial $Z$-depth with a random jitter in $[20, 30]$ (`initialZ = 20 + Math.random() * 10; z = 85 - (ratio * (85 - initialZ))`). This eliminates planar clustering at $z=20.0$, creating an authentic, staggered cosmic perspective across new discoveries. As the card ages and its remaining TTL ratio drops, it smoothly recedes toward deep space ($z \to 85$).
- **Temporary Card Interception & Explicit Promotion (Task 104)**:
  - *Direct Edit Interception*: Uncollected temporary cards intercept double-click and Alt+click actions, completely eliminating silent disk persistence and opening an external editor prematurely. Instead, a gentle floating prompt (`需先收集`) appears.
  - *Dual-State Collect Buttons (Task 104 & Task 133)*:
    - 摒弃了文字与下箭头托盘（避免误认为“下载”），采用纯净极简的“翻开的书”典籍图标。
    - 散落悬停态（Scattered Hover）：右上角浮现 `26px × 26px` 圆形半透明磨砂按钮。
    - 聚焦模态（Focused Modal）：弹窗右上角呈现 `32px × 32px` 圆形按钮。
    - **往里加页动效（Hover Animation）**: 鼠标悬停时，内嵌的书页图层以自然弹性曲线（`cubic-bezier(0.34, 1.45, 0.7, 1)`）从右上方滑入册中并优雅贴合落入书缝，生动诠释“将飘散灵感收入典籍”。
  - *In-Place Transformation*: 点击收集图标触发 `PromoteTempCard(card.id)`，将卡片持久化写入 `<home>/Scattering/`，就地蜕去虚无迷雾与呼吸光环，解锁外部编辑。
- **Authentic Cosmic Perspective Scale Hierarchy**:
  - Near foreground ($Z = 0$): Scale **$1.08$**, $Z_{3d} \approx \mathbf{+100px}$, commanding and prominent.
  - Midground ($Z = 50$): Scale **$0.86$**, $Z_{3d} \approx \mathbf{+25px}$.
  - Deep space ($Z = 100$): Scale **$0.64$**, $Z_{3d} \approx \mathbf{-50px}$, distant and compact.
  - Formula: $\text{Scale}(Z) = 1.08 - \frac{Z}{100} \times 0.44$, $Z_{3d} = (100 - Z) \times 1.5 - 50 + \text{pulseZ}$.
- **Dual-Tier Continuous Optical Grayscale (杜绝双重透明度相乘)**:
  - **Primary Text (`--card-text-color`)**:
    - 近景 ($Z = 0$): 字体呈现深邃炭黑 $\text{rgb}(34, 34, 34)$，实体清晰。
    - 中景 ($Z = 50$): 字体平滑过渡为柔和铅灰 $\text{rgb}(89, 89, 89)$。
    - 远景 ($Z = 100$): 字体呈现雅致雾铅灰 $\text{rgb}(145, 145, 145)$。
  - **Secondary / Translated Original Text (`--card-text-secondary`)**:
    - 消除 `.original` 的硬编码 `opacity: 0.75`，采用独立计算的次级灰度阶梯（$\text{rgb}(58 \sim 160)$），彻底避免容器 Alpha 与文字 Alpha 叠加产生的幽灵雾化。
  - 容器透明度自然衰减：$\text{Opacity}(Z) = 0.96 - \frac{Z}{100} \times 0.32$（近景 $0.96$ $\to$ 远景 $0.64$），临时卡片与永久卡片同步服从该景深规律。
- Departing cards (`isFadingOut = true`):
  - Animate over 2.5 seconds with downward drift, blur, and opacity reduction to 0 before removal.

---

## 4. Gravitational Y-Axis Expansion, Multi-Screen Overflow & 80/20 Distribution

### 4.1 Universal Gravitational Cascade & Viewport Placement
- **Mother Card Protection & Alignment (`isProtectedCard`)**:
  - Any card that triggers a Bugu radar session (`sourceCardId`) or serves as the mother (`child.echoOf === card.id`) of an active Babel echo on stage is elevated to VIP status (12h protected half-life) and is strictly immune to eviction or metabolic fade-out.
  - **Mother Card Alignment**: If the Mother card is triggered while located outside the user's active viewport ($|c.y - \text{scrollExpansion} \times 300| > 260$), it is dynamically summoned to the current viewport like a newly admitted card, ensuring the radar origin is immediately visible.
- **Universal Screen Cascade Law (通用单屏引力级联法则)**:
  - Single screen comfort capacity is $5 \sim 6$ cards.
  - Current Viewport Center: $Y_{\text{center}} = \text{round}(\text{scrollExpansion} \times 300\text{px})$.
  - When admitting a card (new thought/chat log, summoned mother card, or cascading card) into Screen $K$:
    - If Screen $K$ has $\le 5$ solid cards: placed in a safe collision-free pocket via 28-sample Mitchell best-candidate algorithm.
    - If Screen $K$ is saturated ($\ge 6$ cards): selects the oldest, non-protected background card ($C_{\text{victim}}$) and smoothly displaces it downward into Screen $K+1$ ($Y += 480\text{px}$ zone), recursively triggering the cascade if Screen $K+1$ is also full.
    - Maximum stage capacity is 30 cards; the deepest, oldest card in deep space fades out into `memoryPool` if total stage cards $> 30$.
- **Bugu Multi-Screen Distribution**:
  - Initial findings (first 1~2 Babel cards) stay on the current screen clustered around the Mother card.
  - Subsequent findings (3rd card onward) flow into the adjacent screen below ($Y \in [Y_{\text{center}} + 300, Y_{\text{center}} + 720]$) and apply the universal cascade to adjacent screen cards if saturated.
  - Mother card shoots golden beams (`BuguRayNetwork`) penetrating the bottom screen boundary, with pulsating cues guiding the user downwards.
- **Refined Universal Deadzone (`OMNIBAR_DEADZONE`)**: `halfWidth: 290, halfHeight: 32`. Card centers are strictly forbidden from sitting directly under the central Omnibar across all screens.
- **Omnibar Invariant Elevation & Stacking Rule**:
  - `.omnibar-container` operates at `z-index: 50`.
  - `.cards-wrapper` operates at `z-index: 5` during idle and hover states, and **only elevates to `z-index: 100` when a card is in focused modal state (`focusedCardId !== null`)**.
  - `<CosmicStage>` is rendered before `<OmniBar>` in DOM order, ensuring unfocused cards strictly pass underneath the input bar and never obscure it.
- **Omnibar Scroll Fade**: During viewport scrolling (`isScrolling = true`), `.omnibar-container` transitions to `opacity: 0; transform: scale(0.96); filter: blur(8px)`. After scrolling stops for 450ms, it smoothly fades back in.
- **Directional Pulsating Scroll Cues (`.deep-space-scroll-cue`)**:
  - **Dynamic Top / Bottom Anchoring**:
    - **Initial Load & Screen 1 Dwell**: On initial entry to Screen 1 (`scrollExpansion <= 0.08`) or after resting on Screen 1 for $>1.2\text{s}$ without upward wheel input, defaults to anchoring at the bottom (`.direction-down`, `bottom: 24px`).
    - **Deep Space Direction Following**: When navigated beyond Screen 1 (`scrollExpansion > 0.08`), anchor position dynamically tracks the last mouse scroll gesture (`lastScrollDirection`):
      - Downward wheel: anchors at bottom (`bottom: 24px`), pulsing cascading downwards (dot $1 \to 2 \to 3$).
      - Upward wheel: anchors at top (`top: 24px`), pulsing cascading upwards (dot $3 \to 2 \to 1$).
  - **Boundary Suppression (Boundary Zero-Pollution)**:
    - **Bottom Boundary**: When reaching maximum scroll depth (`scrollExpansion >= maxScroll - 0.22`) and the mouse is wheeling downwards, the cue is strictly suppressed (`isCueVisible = false`).
    - **Top Boundary**: When reaching Screen 1 (`scrollExpansion <= 0.08`) and the mouse is wheeling upwards, all cues are suppressed until an inactivity dwell ($1.2\text{s}$) smoothly resets the default downward hint.
  - **Dual Cosmic Palettes (Decoupled from Bugu Amber)**:
    - **Downward Cue**: **深灰蓝色 (Deep Slate Blue)** (`#4a5c78`, `#6f8cb0`, shadow `rgba(111, 140, 176, 0.85)`), providing non-distracting depth guidance into the cosmic abyss.
    - **Upward Cue**: **蓝白色 (Ice Blue-White)** (`#edf5ff`, `#ffffff`, celestial starlight halo `rgba(150, 205, 255, 0.95)`), signaling upward return to the celestial zenith of Screen 1.
- **Refined Temporary Card Aesthetics (Mist-Blue Transparency & Breathing 灰白 Vignette Rim)**:
  - **Translucent Mist-Blue Base**: Airy translucent cool mist-blue gradient (`rgba(226, 236, 248, 0.58)` to `rgba(210, 222, 238, 0.42)` with `blur(16px)`), harmonizing with cosmic space and wallpaper.
  - **Dynamic Breathing 灰白 Vignette Rim**: Internal `::before` pseudo-element with radial gradient feathering into an organic misty rim (`rgba(248, 250, 252, 0.32)` to `rgba(224, 234, 246, 0.70)`) and a gentle 5.5s breathing aura (`temporary-rim-breathe`) that softly shifts illumination like starlight mist.
  - **Zero Solid Border Interference**: Strictly enforces `border: 1px solid transparent !important` across default, hover, and focus states. Eliminates double-border clutter (no solid rectangular line fighting with orbiting beads).
  - **Decoupled Pearl 灰白 Orbiting Beads**: Decouples border beads from Bugu's amber gold to luminous pearl gray-white (`#e2e8f0` / `#f8fafc`, `drop-shadow(0 0 2.5px rgba(241, 245, 249, 0.85))`), blooming to `#ffffff` on hover.
  - **Focused Card Scrollability**: Focused state locks `overflow-y: auto !important; -webkit-overflow-scrolling: touch; overscroll-behavior: contain;` without clipping, allowing fluid vertical text scrolling.
- **Bugu Magic UI Animated Beam, Refined Fiber & Resonant Aperture Blooms (`BuguRayNetwork.svelte`)**:
  - **Refined Cosmic Fiber Gauge**: Thinned track from $1.5\text{px}$ to $0.9\text{px}$, and traveling pulse from $2.8\text{px}$ to $1.6\text{px}$ (`stroke-width: 1.6px`), achieving exquisite high-precision cosmic filament optics without heavy visual weight.
  - **Synchronized Source & Target Aperture Blooms (起点/终点引力光圈共鸣)**:
    - **Source Aperture Node (发射瞬间最亮与离去渐隐)**: Positioned at Mother exit port ($22\text{px}$ radius radial gradient halo + $3.2\text{px}$ core). 脉冲发射的瞬间（$f = 0.04 \sim 0.07$）达到**最亮峰值**（Cycle 1: 0.92, Cycle 2: 0.58, Cycle 3: 0.28），随着脉冲向深空逐渐远离（$f = 0.07 \to 0.18$）平滑减淡熄灭，完美实现能量喷薄与脱离感。
    - **Target Aperture Node (撞击瞬间最亮与平滑归零)**: Positioned at Child entrance port. Progressively warms up and illuminates as the pulse approaches in deep space ($f = 0.50 \to 0.70$), reaches maximum peak brilliance at the exact instant of impact ($f = 0.75$), and gradually dissipates until it fully extinguishes at $f = 1.00$ (precisely synchronizing with the interval before the next cycle).
    - **Strict Chromatic & Opacity Lockstep**: Maximum bloom brightness in each of the 3 cycles identically matches the beam pulse peak ($0.92 \to 0.58 \to 0.28$) in pure Amber Gold (`#f59e0b`).
  - **2x Expanded Decaying Horizon (4.8s / 周期，总长 14.4s)**: 单个脉冲周期从 $2.4\text{s}$ 翻倍至 **$4.8\text{s}$**，总衰减时间从 $7.2\text{s}$ 翻倍至 **$14.4\text{s}$**。终点光圈熄灭消散窗口扩大至完整的 $1.2\text{s}$，随后的异步发射间隔也同步放缓至 $4.8\text{s} \sim 7.2\text{s}$，彻底告别“闪现过快”的压迫感，呈现出悠然呼吸的宁静宇宙深空光景。
  - **Docking Overlap & 3D Parallax Elimination**: `DOCKING_INSET_PX = 2; translateZ(-5px); z-index: -1`. The $22\text{px}$ bloom halo seamlessly wraps the card border, eliminating both visible gaps and internal card cutting.
  - **Cubic Bezier S-Curve Routing & Staggered Scheduler**: Natural gravitational tangential curvature with $4.8\text{s} \sim 7.2\text{s}$ asynchronous staggered launch.

### 4.2 Smooth Downward Pull Gesture & Multi-Screen Depth
- Scrolling downward with mouse wheel or trackpad accumulates into `scrollTarget` via `computeNextScrollTarget` (normalizing `deltaMode` and soft-clamping impulses) and drives `scrollExpansion` (`spring(0, { stiffness: 0.16, damping: 0.72 })`) from `0` up to `getMaxScrollExpansion(cards, totalAvailable)` (`2.2` up to `5.0`).
- When total available pool cards (`localVaultPool.length + memoryPool.length + cards.length`) exceed single-screen capacity, `poolBasedMax` unlocks multi-screen scroll depth proportionally ($2.2 + (\text{total} - 10) \times 0.12$, capped at $5.0$).
- The 3D `.scene` translates upward (`translateY(-scrollExpansion * 300px)`) with `will-change: transform` and no CSS transition lag, staying locked at 60fps with card springs.
- **Screen Zone Placement Locking**: When staging cards with `explicitTargetY` (e.g. current viewport), candidate zones are strictly locked to the target screen (`minY: targetY - 240, maxY: targetY + 240`). Natural domino cascade handles pushing saturated cards down into subsequent screens without jumping or draining Screen 1.

### 4.3 80/20 Stage Replenishment Rule
When new card slots become available during downward expansion or after card decay:
1. **If resting cards exist in `memoryPool`**:
   - **80% of new slots**: Drawn from resting cards in `memoryPool`.
   - **20% of new slots**: Newly sourced from un-cached `localVaultPool` cards, **inserted into `memoryPool` with a 24-hr macro TTL**, and staged with `isFresh: true`.
2. **If all memory cards are already on stage**:
   - **100% of new slots**: Automatically fetched from the local vault, inserted into `memoryPool`, and staged.

### 4.4 Viewport Stability & Focus-Driven Lifecycle (Abolished 45s Auto-Collapse, Task 106)
- **Viewport Invariance**: The previous 45-second gravitational auto-collapse was completely abolished. Viewport depth is 100% governed by user scroll gestures; scrolling to Screen 2 or 3 permanently maintains that viewing coordinate.
- **Mid-Reading Calmness**: Active stage cards no longer evaporate mid-reading during foreground usage.
- **Focus-Driven Temporary Decay**:
  - In `handleWindowFocus`, uncollected temporary cards past their half-life execute a two-stage retreat:
    - If $z < 65$: steps backward into deep space ($z += 20 \sim 25$), resetting `spawnTime = now`.
    - If $z \ge 65$: gracefully dissolves and fades out (`isFadingOut = true`) into `memoryPool`.

### 4.5 Universal Gravitational Fallback Engine (Task 112 & Task 118)
- **Strict 4-Phase Extinction & Cooldown Sequence**:
  1. *Light Active (Locked)*: As long as any optical aura (search glow, tag ice blue neon) is shining (`hasActiveAura`), the card is strictly locked in the foreground.
  2. *Unlocked Moment*: The instant the light naturally extinguishes (search aura duration is 15 minutes, tag aura is 2 minutes), the card reaches the Unlocked state at `unlockedAt`.
  3. *10-Minute Post-Extinction Cooldown Buffer*: From `unlockedAt`, a 10-minute cooldown window begins (`now < unlockedAt + 10m`). The card remains quietly in place.
  4. *Focus-Driven Gravitational Sinking ("Only Backward, Never Forward")*:
     - On window focus, once the 10-minute post-extinction cooldown has elapsed (`now >= unlockedAt + 10m`):
     - Computes intrinsic target depth: `intrinsicZ = calculateIntrinsicTargetZ(card)`.
     - Only if `intrinsicZ > card.z + 5` does the card sink back to its historical epoch via `animSpring`. Cards already in the foreground never jump forward.

### 4.5 Associative Resurgence Lifecycle & Ice Blue Synapse Ray Network
- **Pure Spatial Tag Visibility Threshold ($Z \le 16$)**:
  - Tags in scattering mode (`ThoughtCardBody.svelte`) are only visible when the card is in the extreme foreground ($Z \le 16$), hovered, focused, or surrounded by an active resonance aura (`card.auraTraces`). Otherwise they smoothly fade out via CSS transition (`0.25s ease`).
- **Global Vault Recall & Safe Staging**:
  - Clicking any `#{tag}` pill toggles `activeConstellationTag`. When activated, Finnegan searches `memoryPool` and `localVaultPool` for unstaged cards possessing the tag and summons them safely into the active viewport ($Y \approx \text{scrollExpansion} \times 300\text{px}$).
- **Resurgence Lifecycle (2-Min Gravitational Sinking & Aura)**:
  - Summoned permanent cards enter at foreground depth $Z = 10$ and are endowed with an Ice Blue resonance aura (`hsl(199, 89%, 60%)`, 120,000ms duration).
  - Over the 120s window, their effective depth sinks continuously according to:
    $$z(t) = z_{\text{target}} - (z_{\text{target}} - 10) \times \left(\frac{\text{remainingMs}}{120000}\right)$$
  - After 2 minutes, the aura fades out, and as depth crosses $Z > 16$, the tags naturally fade out.
- **Ice Blue Synapse Ray Network (`SynapseRayNetwork.svelte`)**:
  - Undirected SVG Bezier filaments in `#38bdf8` beneath cards (`z-index: -1`, `translateZ(-5px)`).
  - Displays a floating glass badge `#{tag}` (10px typography) at midpoint $t = 0.5$.
  - When active, dims non-constellation cards to `opacity: 0.35` (`transition: opacity 0.3s ease`).

### 4.6 Universal Gravitational Fallback Engine (常态卡片通用全局引力归位兜底机制)
- **Implemented In**: `frontend/src/lib/gravityFallback.ts`, `frontend/src/App.svelte` (`handleWindowFocus`)
- **Optical & Physical Decoupling (光芒视觉与物理深度解耦)**:
  - 无论常态卡片被全文搜索（`transformSearchResults`）、标签联想召回（`activateConstellationTag`）还是命令拉出（`handleExecuteCommand` / `ensureCardStagedInViewport`），统一注入 `elevatedAt: now` 时间戳。
  - **10 分钟提升保护期**: 在 10 分钟窗口内（$T_{\text{elapsed}} < 10 \times 60 \times 1000\text{ms}$），卡片维持前台显眼深度供用户聚焦查阅。
  - **切屏聚焦沉降归位 (Window Focus Trigger)**: 当用户切屏切回 Finnegan 触发 `handleWindowFocus` 时，针对保护期已满的常态卡片，按创建时间计算其自然固有深度 $Z_{\text{intrinsic}} = \text{calculateIntrinsicTargetZ}(\text{card})$。
  - **只往后不往前法则 (Strict "Only Backward, Not Forward" Rule)**: 严格执行 $Z_{\text{intrinsic}} > Z_{\text{current}} + 5$ 判定。只有当自然深度比当前深度深 5 个单位以上时，卡片才平滑沉降回深空；若卡片创建于近期导致固有深度较浅，则坚决不向前跃迁。
  - **光环与视觉线索独立保留**: 沉降过程仅更新卡片物理 $Z$ 坐标，由 `UICard.svelte` 的 `animSpring` 自动执行平滑缓动，搜索高亮光芒与光环痕迹（`isSearchResult`, `auraTraces`）完全保留。

### 4.7 Focus-Driven Relative Time Refresh (切屏聚焦相对时间自动刷新机制)
- **Task**: `focus_driven_relative_time_refresh_121`
- **Implemented In**: `frontend/src/lib/time.ts`, `frontend/src/App.svelte`, `frontend/src/UICard.svelte`, `frontend/src/components/cards/*`
- **Problem & Root Cause**:
  - Finnegan 卡片展示语义相对时间（“刚刚”、“今天 HH:mm”、“昨天 HH:mm”、“前天 HH:mm”、“N 天前 上午”）。
  - Svelte 组件内部原先直接通过 `$: displayTime = getCardDisplayTime(card)` 计算。当跨日、跨午夜或时间流逝后切屏切回 Finnegan 时，因卡片引用未变化，响应式无法感知真实时间推移，导致卡片长时间停留在“刚刚”或“今天”。
- **Architecture & Reactive Time Anchor**:
  1. **Global Time Store (`stageTime: Writable<number>`)**: `frontend/src/lib/time.ts` 导出全局时间锚点 Store 与 `refreshStageTime()` 函数。
  2. **Focus & Visibility Interceptor**: 在 `App.svelte` 的 `handleWindowFocus()` 及 `document.visibilitychange` 中调用 `refreshStageTime()`，并在 `metabolicInterval` (45s 循环) 同步刷新。
  3. **Full Reactive Tree Cascade**: `UICard.svelte`（`getCardDisplayTime(card, $stageTime)`）、`VirtualCardProxy.svelte` 以及所有卡片 Body 组件（`ThoughtCardBody`, `BabelCardBody`, `NoteCardBody`, `ChatLogCardBody`）全部接入 `$stageTime` 订阅，窗口获得焦点的瞬间全场卡片相对时间自动无感重算并更新。

### 4.8 Natural Calendar Day Temporal Hierarchy & "前天" Formatting (自然日历日时空体系)
- **Task**: `calendar_day_time_formatting_and_qiantian_123`
- **Implemented In**: `frontend/src/lib/time.ts` (`formatPointTime`)
- **Key Breakthrough**:
  - 彻底废除旧式滚动的 24h/48h 物理毫秒差判定，改由真实本地自然日历日（`targetMidnight` 与 `nowMidnight` 跨度 `dayDiff`）主导：
    - `dayDiff === 0`: 今天（< 5分钟为“刚刚”，否则为“今天 HH:mm”）
    - `dayDiff === 1`: 昨天（“昨天 HH:mm”）
    - `dayDiff === 2`: **前天**（“前天 HH:mm”）
    - `dayDiff >= 3 && dayDiff < 30`: N 天前（“{dayDiff} 天前 {period}”）
  - 解决前天下午/晚上撰写的卡片因物理时间未满 48 小时被误判为“昨天”，以及历史版本中缺乏“前天”语义层级的缺陷。

---

## 5. UI Geometric & Interaction Polish

- **Card Dimensions**:
  - Scattered state: `width: 200px; height: 190px;` (gentle square post-it proportion, `border-radius: 16px;`).
  - Text is vertically centered with 5-line ellipsis (`-webkit-line-clamp: 5`).
- **Focus State (Invariant Center Focus)**:
  - Symmetrical square modal: `420px × 420px` locked at the exact geometric center of the current viewport (`x = 0, y = scrollExpansion * 300`), compensating for `.scene`'s `translateY(-scrollExpansion * 300px)` at any scroll depth and smoothly returning to `(card.x, card.y)` when unfocused.
  - **Instant Uprightness**: Tilt angles (`rotate`, `rotateX`, `rotateY`) and scene `$globalTilt` instantly snap to $0^\circ$ on the very first frame of focus, preventing wobble during flight.
- **Layering & Z-Index**:
  - In background: `.cards-wrapper` sits at `z-index: 5`, behind the Omnibar (`z-index: 50`).
  - On hover or focus: `.cards-wrapper` jumps to `z-index: 100` (`.elevated`), elevating the active card above the Omnibar.
- **Peripheral Radial Vignette & Viewport-Relative Edge Blur**:
  - **画布级径向渐隐**: `.cards-wrapper` 挂载 `radial-gradient(ellipse at center, black 80%, rgba(0, 0, 0, 0.4) 93%, transparent 100%)` 遮罩，保证中心 80% 区域绝对清澈，仅外圈 20% 平滑消融于背景毛玻璃中。
  - **动态穿透**: 当卡片被 Hover 或 Focus 触发 `.elevated` 时，遮罩自动切换为 `none`，杜绝边缘卡片悬停放大时被硬切。
  - **视口相对离心模糊 (Viewport-Relative Edge Blur)**: `UICard.svelte` 根据卡片相对于当前滚动视口中心的坐标 (`viewY = card.y - scrollExpansion * 300`) 计算离心距 $dist = \sqrt{x^2 + \text{viewY}^2}$ 与 $0 \sim 5\text{px}$ 柔和高斯模糊，确保第二屏、第三屏卡片在滑入视口中心时完全清晰通透。
