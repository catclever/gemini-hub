# Card Lifecycle, Dynamic Decay & Gravitational Expansion Design

**Date**: 2026-10-13  
**Status**: Approved by User  
**Task ID**: `card_lifecycle_decay_007`

## 1. Storage & Memory Sourcing Hierarchy

1. **Persistent Vault (`Scattering/` and `Waving/`)**:
   - `Scattering/`: Fleeting thoughts and note fragments.
   - `Waving/`: Longer, structured thoughts, outline drafts, and finished notes.
   - Both directories are scanned by the Go backend on startup and updated via filesystem watcher events.
   - Acts as the eternal memory reservoir for memory echoes.

2. **In-Memory Transient Pool (Session Cache / TTL ~24 Hours)**:
   - Contains temporary cards produced by Bugu (Babel radar translations) or search exploration.
   - Macro TTL is set to **~24 hours** (or app session duration).
   - In-memory cards can undergo multiple cycles: *Spawning -> Active on Stage -> Receding back to memory -> Re-emerging on Stage -> Expiring after TTL*.

3. **Active Celestial Stage (On-Screen Rendering Pool: 8 ~ 14 cards)**:
   - Total cards rendered in the active 3D viewport at any time is strictly bounded to 8 ~ 14 cards (default baseline ~10 cards).

## 2. Dynamic Half-Life Decay Engine

When a card enters the active stage, its stage lifetime $T_{\text{decay}}$ is computed:
$$T_{\text{decay}} = T_{\text{base}} \times f(\text{Type}) \times f(\text{Depth}) \times f(\text{QueuePressure}) \times \text{RandomJitter}$$

### Parameters:
- **Baseline Duration $T_{\text{base}}$**: ~3 to 4 hours.
- **Type Weight $f(\text{Type})$**:
  - **Latest Manual User Input (Exclusive VIP)**: Only the single most recent manual input enjoys VIP protection (extended half-life + immune to eviction). If multiple manual cards are created, only the latest holds the VIP status.
  - **External / Module Generated Cards (Bugu / External Editor)**: Standard slow half-life (~3 to 4 hours).
  - **Historical Memory Echoes (Scattering / Waving)**: Standard half-life (~1 to 2 hours).
- **Depth Factor $f(\text{Depth})$ (Meteor vs Fixed Star)**:
  - Near foreground ($Z \approx 0$): Decay multiplier $\approx 0.6\times$ (burns faster, moves out sooner).
  - Distant background ($Z \approx 100$): Decay multiplier $\approx 1.5\times$ (slowly floats in background).
- **Queue Pressure $f(\text{QueuePressure})$**:
  - Scales down active stage lifetime when backlog of unshown in-memory cards increases, allowing fresh cards to cycle onto the stage.
- **Random Jitter**: $\pm 20\%$ variance to prevent synchronized fading.

## 3. Freshness & Visual Clarity Rule
- Newly spawned cards do NOT forcibly occupy the closest foreground; they can land naturally at any depth.
- However, while fresh (`isFresh = true`), a new card is granted **100% optical clarity**: opacity = 1.0, contrast = 100%, sharp outline, unaffected by background fog.

## 4. Gravitational Y-Axis Expansion & Auto-Collapse
1. **Pull Down to Expand**:
   - Swiping or scrolling down expands virtual canvas height to $200\text{vh} \sim 300\text{vh}$.
   - Priority for populating the expanded space:
     1. Unshown or resting in-memory temporary cards (Bugu).
     2. Historical cards from `Waving/` and `Scattering/`.
2. **Auto-Collapse (Gravitational Tide)**:
   - After **45 seconds** of user inactivity, the canvas smoothly contracts with spring damping back to $100\text{vh}$.
   - Cards outside the viewport gently recede into the cosmic fog without destroying in-memory cards.
