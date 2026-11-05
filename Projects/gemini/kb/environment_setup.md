# Environment Setup & Global Symlink

**CRITICAL CONTEXT FOR AGENTS:**

The current workspace `/Users/kael/Library/XDG_Exile/gemini` is **NOT** a standard isolated local project. It is the canonical backing directory that the system's `~/.gemini` symlink points to.

## Implications:
1. **Global Scope:** Any modifications made to `GEMINI.md`, `AGENTS.md`, or the `config/` directories within this workspace directly alter the **machine-wide global configurations** for Antigravity.
2. **Rule Files:** The `GEMINI.md` file at the root of this workspace acts as the global rule set for all projects on this machine because it effectively resides at `~/.gemini/GEMINI.md`.
3. **Plugins & Skills:** Writing or editing skills in `config/plugins/` or other standard customization paths in this directory directly modifies the user's global agent tools.

Agents operating in this workspace must be aware that their file modifications have a global blast radius and should treat this directory as the system's central configuration hub.
