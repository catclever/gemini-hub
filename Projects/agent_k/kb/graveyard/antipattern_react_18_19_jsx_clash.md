# Anti-Pattern: Cross-Package React 18 / 19 Type Conflict (TS2786)

**Date:** 2026-09-23  
**Symptoms:** `TS2786: 'ComponentName' cannot be used as a JSX component. Type 'bigint' is not assignable to type 'ReactNode'.`

## What Happened
In a monorepo workspace where some packages or root devDependencies use `@types/react` v19 while sub-apps (like `demo-app`) use `@types/react` v18, React 19 expands `ReactNode` to include `bigint | Promise<ReactNode>`.
When a component typed with React 19 is passed into a JSX context governed by React 18's `JSX.Element`, TypeScript rejects the component.

## Prevention & Rule
1. Unify `@types/react` versions across monorepo workspaces where possible.
2. In consumers crossing the boundary, safely cast external components to `React.ComponentType<any>` (or cast props to `any`) to decouple runtime JSX from conflicting compile-time definitions.
