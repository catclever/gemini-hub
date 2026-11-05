---
title: Fix demo-app tsconfig and build configuration
status: completed
priority: low
tags:
- demo-app
- build
- typescript
id: fix_demo_app_build_005
---
# Objective
Fix the build error in `apps/demo-app` so `npm run build -w demo-app` passes cleanly.

# Context & Issues
`apps/demo-app` lacks a `tsconfig.json`, causing `tsc` to scan parent directories and fail on modern Vite type declarations.

# Requirements
1. Create `apps/demo-app/tsconfig.json` with appropriate compiler options (e.g., target ES2020, moduleResolution bundler, jsx react-jsx, skipLibCheck true, include ["src"]).
2. Run `npm run build -w demo-app` and verify success.
3. When finished, update status in this file to `ready_for_review`.
