# MusicFree Project Knowledge Base

## UI & DOM Interaction
- **Text Retrieval**: Always use `textContent` instead of `innerText` when extracting text from the MusicFree player DOM (e.g., track title, artist, source badge). This prevents empty strings when the elements are hidden behind custom panels.
- **React Fiber Property Inspection**: In playlist and album detail views, playlist metadata is stored on the title/header fiber under `memoizedProps.musicSheet` (for sheets) or `memoizedProps.album` (for albums). Detail see [CDP Direct Debugging & Architecture](file:///Users/kael/.gemini/Projects/fun.upup.musicfree/kb/cdp_direct_debugging.md).
- **MusicFree URL Hash Routing**: URL hashes follow `#/musicsheet/<platform>/<id>` and `#/album/<platform>/<id>`. Avoid naive `/sheet/` substring matching.

## CDP Direct Debugging SOP
- **Automated Zero-Copy Debugging**: MusicFree listens on CDP port `9222` (while Antigravity IDE listens on `9224`). Always verify via `lsof -iTCP -sTCP:LISTEN -n -P | grep -E "MusicFree|922"` and use CDP `Runtime.evaluate` to inspect live React state autonomously without burdening the user with manual console copying. See [CDP Direct Debugging](file:///Users/kael/.gemini/Projects/fun.upup.musicfree/kb/cdp_direct_debugging.md).

## QQ Music API (Proxy)
- **Playlist ID**: When fetching playlist details via the proxy (`/songlist?id=...`), always prioritize `dissid` over `tid` or `dirid`, as modern QQ API versions may omit `tid`.
- **My Favorite Playlist**: The "I Like" playlist usually has `dirid === 201`.

## Plugin Config Management
- **Source Mapping**: The MusicFree plugin source identifiers (e.g. `qq`, `qq音乐`, `netease`, `网易云`) must be explicitly mapped to the respective `API_CONFIG` objects to ensure custom panels can correctly match the current song's origin.
