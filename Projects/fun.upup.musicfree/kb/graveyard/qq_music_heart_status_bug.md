# Post-Mortem: QQ Music Custom Panel Red Heart Status Loss

## Context
In the MusicFree QQ Music custom panel, the red heart (like) status was reported as inaccurate: "点了一次之后 下次再打开自定义面板 又消失了" (After clicking once, it disappears next time the custom panel is opened).

## What Failed and Why
1. **API Parameter Mismatch (QQ Music API)**:
   - *What was tried*: Using `favPlaylist.tid` to fetch the "I Like" playlist details (`/songlist?id=...`).
   - *Why it failed*: In newer QQ API responses, the playlist object often lacks a `tid` but contains a `dissid`. Passing `undefined` to the `/songlist` endpoint caused the request to fail silently. As a result, the local `myFavSet` was incorrectly initialized as an empty Set, meaning it could not correctly verify if songs were liked.
2. **Missing UI State Cache Initialization**:
   - *What was tried*: The `handleLike` function assumed `config.myFavSet` was already populated by the initial check. 
   - *Why it failed*: Because the initial API fetch failed, `config.myFavSet` was `undefined`. Clicking "Like" triggered the API successfully but failed to add the song to the local Set, causing the status to disappear upon reopening the panel.
3. **Visibility-dependent DOM property (`innerText`)**:
   - *What was tried*: `updateSongState` checked if the song changed by reading `titleEl.innerText`.
   - *Why it failed*: When the panel is hidden (`display: none`), reading `innerText` can return an empty string in some environments. This caused a false positive for a song change, forcing a reset of the red heart to its unliked state.
4. **Missing Configuration Aliases**:
   - *What was tried*: Resolving `API_CONFIG` using `currentSongInfo.source.toLowerCase()` (e.g., `"qq音乐"` or `"qq"`).
   - *Why it failed*: The config only mapped exactly to `qq_pve`. When opening the panel, the config lookup failed, and the script skipped checking the remote like status altogether.

## What NOT to do / Lessons Learned
- **Do NOT** rely solely on legacy API fields like `tid` without providing modern fallbacks (e.g., `dissid || tid || dirid`).
- **Do NOT** assume a cache object (`Set`, `Map`) exists before mutating it in event handlers. Always defensively initialize it if missing.
- **Do NOT** use `innerText` for background or hidden DOM elements; use `textContent` to ensure styles and visibility do not alter the returned text.
- **Do NOT** leave edge-case string mappings incomplete. Always provide comprehensive alias mappings for config objects (e.g., mapping `"qq"`, `"qq音乐"` to `qq_pve`).
