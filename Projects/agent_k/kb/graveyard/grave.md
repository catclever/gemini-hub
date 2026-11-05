# The Graveyard (Negative Knowledge)

This directory stores post-mortems, failed approaches, and anti-patterns.
Each markdown file describes the context, what was tried, why it failed, and what NOT to do.

## Anti-Patterns Index
- [Untracked Emitted JS Poisoning Vite/Rollup](./antipattern_untracked_emitted_js.md): Running `tsc` without `noEmit` pollutes `src/` with `.js` files, breaking Rollup chunk analysis with `dependentEntriesByModule.get is not a function`.
- [Cross-Package React 18/19 Type Conflict](./antipattern_react_18_19_jsx_clash.md): Mismatched `@types/react` versions between packages trigger TS2786 (`bigint is not assignable to ReactNode`); resolve via unified versions or explicit `React.ComponentType<any>` casting.
