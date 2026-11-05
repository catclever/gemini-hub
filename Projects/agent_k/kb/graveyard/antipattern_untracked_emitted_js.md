# Anti-Pattern: Untracked Emitted JS Poisoning Vite/Rollup Build

**Date:** 2026-09-23  
**Symptoms:** `vite build` fails during Rollup chunk analysis with `dependentEntriesByModule.get is not a function or its return value is not iterable`.

## What Happened
When `tsc` is invoked without `"noEmit": true` (or `--noEmit`), TypeScript compiles `.ts`/`.tsx` files directly into `.js` files in the same `src/` directory.
When Vite/Rollup analyzes module imports (e.g. `import ... from './LayoutResolver'`), it resolves to the newly emitted `LayoutResolver.js` rather than `LayoutResolver.ts`, causing mixed module graphs, circular dependency ghost entries, and fatal Rollup bundling failures.

## Prevention & Rule
1. Ensure all `tsconfig.json` files for bundler-based packages explicitly specify `"noEmit": true`.
2. Clean up any emitted `.js` files inside `src/` directories immediately.
