---
id: standardize_builtin_modules_manifest_and_host_api_149
title: Standardize Built-in Modules (Bugu, ATProto, Curio) to Pluggable Host Contracts
status: completed
priority: high
tags:
- modules
- bugu
- atproto
- curio
- jules
session: conversation://f02d8867-c211-4b1b-9cc3-b201d0775800
---

# Standardize Built-in Modules (Bugu, ATProto, Curio) to Pluggable Host Contracts

## 任务目标与背景
Refactor built-in modules (modules/bugu, modules/atproto, modules/curio) to conform strictly to the new Pluggable Core Host contracts (ManifestProvider, ActionProvider, HostAPI, and core/llm):
1. In modules/bugu: Implement module.ManifestProvider (GetManifest() declaring ThemeColor '#f59e0b', BeaconType 'radar', PromotionStrategySpec with icon 'anchor_comment' & bindMotherCard: true), route card spawning and session completion via module.Context.Host (with bus fallback), and delegate modules/bugu/llm/client.go to Finnegan/core/llm.
2. In modules/atproto: Implement module.ManifestProvider (GetManifest() declaring ThemeColor '#38bdf8', BeaconType 'butterfly', PromotionStrategySpec with icon 'anchor_comment' & bindMotherCard: true) and module.ActionProvider (ExecuteAction handling 'fetch_comments'), replace Finnegan/modules/bugu/llm import with Finnegan/core/llm, and route card spawning/completion via ctx.Host.
3. In modules/curio: Implement module.ManifestProvider (GetManifest() declaring CardTypes: [{Type: 'curio'}]).
4. Strict boundary: Modify ONLY files under modules/bugu/, modules/atproto/, and modules/curio/ (zero changes outside modules/).

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

## Jules Dispatch Status
- **Pre-flight Commit**: `eb8c52565fffb14e22642febf45be32d5f4a00a1` (`origin/main`)
- **Jules Session ID**: `sessions/8280735717040164395`
- **Jules Session URL**: https://jules.google.com/session/8280735717040164395
- **Plan Approved**: Yes (`:approvePlan` triggered via REST API)
- **Strict File Boundary**: Confined to `modules/bugu/`, `modules/atproto/`, and `modules/curio/` to avoid any conflict with concurrent Core/Frontend work.

## PR #18 Review Status
- **PR**: `catclever/Finnegan#18` (Standardize Built-in Modules)
- **Changed Files Verified (Strictly inside `modules/`)**:
  - `modules/atproto/atproto.go`
  - `modules/atproto/atproto_test.go`
  - `modules/bugu/llm/client.go`
  - `modules/bugu/module.go`
  - `modules/bugu/module_test.go`
  - `modules/curio/module.go`
  - `modules/curio/module_test.go`
- **Status**: Merged on GitHub remote (`origin/main`), holding off `git pull` on PVE `/root/Projects/Finnegan` and local Mac sync until user's concurrent work in conversation `bce37722-25ac-4706-8480-cb1873d584bf` completes.
