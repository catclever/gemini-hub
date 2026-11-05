# Architecture & Technical Specifications

## 1. System Vision: "Soul in Cloud, Body at Edge"
EnginEdge is a lightweight native Rust binary acting as an edge executor and Model Context Protocol (MCP) server for the Descartes & Dalembert ecosystem.
- **Soul in Cloud**: Centralized intelligence, GitHub repo surveys, open-source intelligence, and living test specs delivered by Descartes Produit and Dalembert in the cloud.
- **Body at Edge**: Native, fast, memory-safe AST manipulation and secure local tool execution directly on the developer's machine or edge node.

## 2. Core Modules & Implementation Status
All four milestones have been successfully implemented, verified, and merged into `main`:
1. **Module A: Stdio MCP Server (`src/main.rs`, `src/protocol.rs`, `src/server.rs`, `src/tools.rs`)**:
   - JSON-RPC 2.0 over `stdio`.
   - Host compatibility: Cursor, Claude Desktop, Antigravity, Zed, Windsurf.
   - Clean stream rule: `stdout` strictly reserved for protocol JSON; all diagnostic logs go to `stderr`.
   - Built-in diagnostic tools: `ping`, `echo`, `get_status`.
   - **Tools Preset & Filtering Engine**:
     - Presets: `full` (17 tools, default, including `append_file`), `light` / `plugin` (9 core tools: AST + Cloud + Telemetry/Verification, stripping duplicate file IO and ping/echo for minimal Prompt Token bloat), `ast-only` / `ast` (3 syntax-only tools).
     - Fine-grained overrides: `--include <tool1,tool2>` (forced addition) and `--exclude <tool1,tool2>` (forced subtraction).
     - Graceful execution fallback: `tools/list` reflects filtered schemas while `tools/call` retains full dispatch capability.
2. **Module B: Tree-sitter AST Engine (`src/ast.rs`)**:
   - Multi-language AST navigation & editing (Rust, Go, TypeScript/JavaScript, Python, Ruby).
   - Core tools: `get_outline`, `read_symbol`, `replace_symbol`.
   - Syntax validation before disk write: prevents AST parse errors and line-number drift.
3. **Module C: Cloud WebSocket Bridge (`src/bridge.rs`)**:
   - Connects to `descartes-produit` and `Dalembert` over async WebSocket (`tokio-tungstenite`).
   - Dynamic proxy tools with offline fallback: `survey_architecture`, `search_code_examples`, `fetch_doc`, `inspect_spec`.
4. **Module D: Anti-Leak Security Jail (`src/security.rs`)**:
   - Chroot-like directory scoping strictly enforcing `$PWD` and rejecting `../` traversal or symlink escapes.
   - Sensitive file blocklist (`.env*`, `id_rsa*`, `id_ed25519*`, `*.pem`, `*.key`, `~/.aws`, `~/.ssh`, `.git/credentials`).
   - Secret redaction filter replacing tokens (`ghp_*`, `sk-*`, `AKIA*`, etc.) with `[REDACTED_SECRET]`.
5. **Module E: Command Safety Policy Engine (`src/policy.rs`)**:
   - Deterministic 0~100 weight scoring system evaluating tool commands.
   - Dual modes: `dev` mode (default, max weight 40) for everyday safe development vs `eval` mode (max weight 75) for benchmark evaluations.
   - Unlocks controlled `&&` chains, native compilers (`cmake`, `ctest`, `make`, `javac`, `mvn`, `gradle`, `go build`), and single-file rollback (`git restore <file>`, `git checkout -- <file>`) in eval mode while strictly blocking dangerous metacharacters and programs (`rm`, `curl`, etc.).
   - Exposed in `get_status` telemetry and dynamic `run_verification` schema hints.
6. **Module F: Automated Benchmark Suite (`src/bench.rs`)**:
   - Automated coding benchmark evaluation against official datasets (e.g. Aider Polyglot, built-in multi-language golden suite).
   - Temporary sandbox isolation, Eval mode policy activation, and telemetry collection (duration, thought steps, AST vs File tool ratios).
   - Automated ground-truth unit test verification grading (`cargo test`, `go test`, `pytest`, `node test`).
   - Markdown & JSON scorecard generation with real-time pass-rate calculation and official DeepSeek-V4.1-Flash baseline delta tracking (57.0% / 71.6%).
7. **Module K: Knowledge & Governance Engine (`src/knowledge.rs`)**:
   - Native project metadata resolution: maps workspace root to `~/.gemini/Projects/<project_name>/` with environment variable override (`ENGINEDGE_META_DIR` / `AGY_PROJECT_META_DIR`) and zero-overhead graceful fallback.
   - Core tools: `kb_search` (token & keyword search), `kb_read` (spec & gotcha reader), `kb_record` (atomic frontmatter writer with automatic `knowledge.md` / `grave.md` index syncing), `kb_audit` (pre-flight technical proposal anti-pattern validation).
   - Dual execution policies:
     - Standalone (`run` / `bench`): automatically loads knowledge context into system prompt if present, gracefully no-ops if absent.
     - MCP Server (`mcp`): default presets (`light`, `ast`, and default `full`) do not expose `kb_*` tools to eliminate token bloat; activated on demand via `--enable-kb`, `--preset kb`, or explicit `--include kb_*`.
8. **CI/CD & Packaging (`.github/workflows/`)**:
   - `ci.yml`: Automated cargo check, clippy, and unit tests across Ubuntu and macOS.
   - `release.yml`: Multi-target binary compilation (Linux x86_64/aarch64, macOS Apple Silicon/Intel) upon release tag.

## 3. Remote Infrastructure
- **PVE Server**: `Antigravity:/root/Projects/EnginEdge`
- **GitHub Origin**: `git@github.com:catclever/EnginEdge.git`
- **Sync**: Mutagen (`mutagen.yml`)
- **Test Suite**: 37 unit tests passing with 100% success rate (`cargo test`).
