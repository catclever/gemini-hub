---
title: Fix TypeScript build errors in @agent-k/core
status: completed
priority: high
tags:
- core
- typescript
- build
id: core_build_fix_001
---
# Objective
Fix the TypeScript compilation errors in `@agent-k/core` so that the package can be successfully built, allowing `inverseKinematics` and other new exports to be available in the `dist` folder.

# Requirements
1. Run `npm run build -w @agent-k/core` to reproduce the errors.
2. Fix the typing issue in `src/framework/BaseComponent.tsx` and `src/framework/Renderer.tsx` where `canvasProps` is being passed but is not declared in the type definition `{ data?: any; loading?: boolean; error?: any; actions?: any; }`.
3. Fix the Zod typing issue in `src/schema.ts` where it complains that `Property 'value' does not exist on type 'ZodNumberCheck'` (specifically, it says `Property 'value' does not exist on type '{ kind: "int"; message?: string | undefined; }'`).
4. Re-run `npm run build -w @agent-k/core` to ensure the build succeeds.
5. Once successful, change the `status` field in this file to `ready_for_review`.
