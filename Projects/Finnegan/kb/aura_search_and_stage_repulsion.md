# Aura Search Display, 3D Cosmic Repulsion & Temporal Decay

**Location**: `~/.gemini/Projects/Finnegan/kb/aura_search_and_stage_repulsion.md`  
**Status**: Active / Production  
**Implemented In**: `frontend/src/App.svelte`, `frontend/src/UICard.svelte`  

---

## 1. 3D Cosmic Repulsion & Stage Stashing

When a user initiates a search from the Omnibar, the 3D space undergoes an optical transformation rather than a harsh screen clear:

```
                      [Camera / User Viewport]
                                 │
                                 ▼
   [Foreground Z: 15 ~ 35]   ── Top Search Results (Luminous Flowing Aura Border)
                                 │
   [Mid-Deep Z: 60 ~ 95]     ── Existing Stage Cards (Pushed Back, Soft Depth Blur)
                                 │
   [Deep Cosmos Z > 100]     ── Exceeded Cards (isFadingOut = true, Graceful Exit)
```

### 1.1 Stage Snapshot & Repulsion Math
1. **Pre-Search Snapshot (`stashedCards`)**:
   Before modifying the active stage, the current array of cards is deep-cloned into `searchSession.stashedCards`.
2. **Foreground Placement**:
   Top search results ($K = \min(\text{targetCapacity}, N)$) are placed in the foreground with shallow depth coordinates ($z \in [15, 35]$), immediately capturing optical focus.
3. **Cosmic Repulsion Wave**:
   Existing cards already on stage are dynamically pushed backward along the Z-axis:
   $$z_{\text{new}} = z_{\text{old}} + 35 + N \times 4$$
   - **Small Result Sets ($N = 1 \sim 2$)**: Old cards are pushed back slightly into mid-depth ($z \in [60, 85]$). They remain visible as ambient background context, avoiding visual emptiness.
   - **Large Result Sets ($N \ge 8$)**: Old cards are pushed beyond the cosmic event horizon ($z > 100$). They receive `isFadingOut = true` and fade out softly into the void.

### 1.2 Downward Expansion & Wheel Prioritization
When the user scrolls the mouse wheel down during an active search:
- The stage capacity (`targetCapacity`) expands downward via the spring-driven `scrollExpansion` tide.
- **Priority Rule**:
  1. The newly revealed capacity slots are **100% prioritized to stage remaining unallocated search results** (marked with aura borders).
  2. When all search results have been exhausted, the system automatically falls back to pulling regular resting cards from `memoryPool` / `localVaultPool` **without aura borders**.

---

## 2. Color Wheel Max Angular Gap Algorithm

To ensure each search session receives a distinct, aesthetically striking aura color without clashing with existing glowing cards, Finnegan uses a circular maximum angular gap search:

```
                                0° (Red)
                         \       |       /
                   300° (Purple) |   /  60° (Yellow)
                              \  |  /
                240° (Blue) ───── O ───── 120° (Green)
                              /  |  \
                   180° (Cyan) / |   \
```

### Algorithm Steps:
1. **Active Color Sampling**:
   Extract all colors from active cards currently on the stage and resting in `memoryPool`.
2. **Hue Degree Mapping**:
   Parse HSL strings to numerical degree angles: $H = \{h_1, h_2, \dots, h_m\}$, where $h_i \in [0^\circ, 360^\circ)$.
3. **Circular Adjacent Gaps**:
   Sort $H$ ascending and compute circular gap lengths:
   $$\Delta \theta_i = h_{i+1} - h_i \quad (0 \le i < m-1)$$
   $$\Delta \theta_{\text{wrap}} = (h_0 + 360^\circ) - h_{m-1}$$
4. **Midpoint Placement**:
   Identify the largest angular gap $\Delta \theta_{\max}$. Place the new search color exactly at the center of this sector:
   $$h_{\text{new}} = \left(h_k + \frac{\Delta \theta_{\max}}{2}\right) \bmod 360^\circ$$
5. **Output Color**:
   Construct high-luminance, high-saturation cybernetic tone: `hsl(${h_new}, 95%, 62%)`. If no colors currently exist, a uniform random angle $h \in [0, 360)$ is selected.

---

## 3. Flowing Light Aura Border & 3-Stage Temporal Decay

Implemented in `frontend/src/UICard.svelte`:

### 3.1 Border Rendering Modes
Each card maintains an `auraTraces` array:
- **Single Search Hit (`auraTraces.length === 1`)**:
  Renders a continuous rotating neon light ray tracing the border perimeter using `@keyframes aura-spin`.
- **Multiple Search Hits (`auraTraces.length >= 2`)**:
  Renders a dynamic multi-color `conic-gradient` spinning halo incorporating all distinct colors from successive search hits.

### 3.2 Temporal Decay Spectrum
The aura's intensity decays over time based on $\Delta t = \text{Date.now()} - \text{latestHitTime}$:
1. **Stage 1: Luminous Flowing Ray ($\Delta t < 3 \text{ min}$)**:
   - Full spinning animation ($3\text{s}$ period).
   - Prominent dual-layer neon glow: `box-shadow: 0 0 16px ${hsla}, 0 0 30px ${hsla}`.
2. **Stage 2: Soft Steady Glow ($3 \text{ min} \le \Delta t \le 30 \text{ min}$)**:
   - Gentle, decelerated rotation ($8\text{s}$ period).
   - Softened box-shadow: `0 0 10px ${hsla}`.
3. **Stage 3: Fine Crisp Contour ($\Delta t > 30 \text{ min}$)**:
   - Rotation halted; static 1.5px fine colored border line.
   - Preserved until the card is eventually evicted from memory, serving as a silent artifact of past discovery.

### 3.3 Search Re-Hit Rejuvenation
If an existing card in memory or on stage is hit by a new search query:
- The new search color is appended to `auraTraces`.
- `macroExpiresAt` is refreshed to `Date.now() + 24 * 3600 * 1000` (re-granting 24-hr TTL).
- `spawnTime` is reset to the current timestamp, instantly restoring the card to **Stage 1 (100% luminous clarity)**.

---

## 4. Esc (Ephemeral Flash) vs. Enter (Consolidation)

The lifecycle of search cards adheres to strict philosophical state boundaries:

### 4.1 Esc: "一闪念" (Zero Memory Footprint)
- Triggered when the user presses `Esc` or deletes the query back to empty.
- **Instant Rollback**: `cards = [...searchSession.stashedCards]`.
- **Zero Memory Contamination**: None of the temporary search results are committed to `memoryPool`. No TTL timers remain. The entire operation vanishes without leaving a single trace.

### 4.2 Enter: "固化视界" (Stage Consolidation)
- Triggered when the user presses `Enter` in search mode.
- **Stage Lock**: Current staged cards remain permanently active. Pushed-out cards are discarded.
- **Memory Ingestion**: All unallocated search results ($N_{\text{staged}} \dots N_{\text{total}}$) are committed into `memoryPool` with a **24-hour Macro TTL**. They naturally re-emerge during subsequent tidal wheel scrolling and 80/20 metabolic cycles.
