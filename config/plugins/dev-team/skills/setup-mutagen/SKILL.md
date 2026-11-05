---
name: setup-mutagen
description: "Automatically inspects the local project ecosystem (Go, Node, Python, Rust, Wails desktop, etc.), generates optimal ignore rules including nested build/packaging artifacts, and initializes a bidirectional Mutagen sync session to the Antigravity PVE server."
---

# Setup Mutagen SOP

This skill defines the standard procedure for establishing and configuring bidirectional code synchronization between a local workspace (Mac) and the remote Antigravity PVE server using **Mutagen**.

It eliminates manual configuration errors by automatically detecting project technologies (Go, Node/TypeScript, Python, Rust, Ruby, JVM, C/C++, Swift, and **Wails desktop applications**), generating a declarative `mutagen.yml` configuration file with tailored ignore rules, and starting synchronization via **`mutagen project start`**.

---

## When to Use This Skill
Activate this skill whenever:
- The user requests to sync a local project to the Antigravity PVE server (e.g., "帮我同步到服务器", "初始化mutagen", "连接PVE").
- A new project is being initialized with `Project-Environment: PVE-Native` under the `project-manager` skill.
- Setting up the prerequisite Bifrost sync link required by `pve-dispatch` or `night-shift`.

---

## Environment & Server Defaults
- **Remote SSH Alias**: `Antigravity` (configured in `~/.ssh/config`).
- **Remote Target Base**: `/root/Projects/<project_name>`.
- **Sync Mode**: `two-way-resolved`.
- **Symlink Mode**: `posix-raw`.
- **VCS Ignore**: Always enable `vcs: true` (automatically ignores `.git/`, `.gitignore` entries, etc.).

---

## Language & Framework Detection Matrix

The skill inspects project root and nested frontend directories to apply the corresponding ignore rules:

| Ecosystem | Manifest Indicators | Key Ignore Patterns |
| :--- | :--- | :--- |
| **Universal / OS** | All projects | `.DS_Store`, `.idea/`, `.vscode/`, `.gemini/`, `.agent/`, `.codex/`, `*.log`, `tmp/`, `temp/` |
| **Wails Desktop** | `wails.json` | `build/bin/`, `build/windows/*.syso`, `frontend/dist/`, `frontend/node_modules/`, `wails-*.log` *(Note: `build/` root is preserved for assets)* |
| **Nested Frontend** | `frontend/`, `web/`, `client/`, `ui/` | `<dir>/node_modules/`, `<dir>/dist/`, `<dir>/build/`, `<dir>/.next/`, `<dir>/.turbo/` |
| **Go** | `go.mod`, `go.sum`, `*.go` | `bin/`, `vendor/`, `*.test`, `*.out`, `*.exe`, `*.so`, `*.dylib` |
| **Node / Web** | `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb` | `node_modules/`, `dist/`, `build/`, `.next/`, `.nuxt/`, `.output/`, `.turbo/`, `coverage/` |
| **Python** | `pyproject.toml`, `requirements.txt`, `setup.py`, `Pipfile`, `uv.lock` | `.venv/`, `venv/`, `env/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.mypy_cache/`, `*.egg-info/`, `dist/` |
| **Rust** | `Cargo.toml`, `Cargo.lock` | `target/` |
| **Ruby** | `Gemfile`, `Gemfile.lock` | `.bundle/`, `vendor/bundle/` |
| **Java / JVM** | `pom.xml`, `build.gradle`, `gradlew` | `target/`, `build/`, `.gradle/`, `*.class` |
| **C / C++** | `CMakeLists.txt`, `Makefile`, `meson.build` | `build/`, `cmake-build-*/`, `*.o`, `*.a`, `*.so`, `*.dylib` |
| **Swift** | `Package.swift` | `.build/`, `.swiftpm/`, `DerivedData/` |

---

## Critical Handling: Packaging Artifacts & Embedded Dist

### 1. Wails Desktop Applications (`wails.json`)
Wails combines a Go backend with an embedded web frontend using `//go:embed all:frontend/dist`.
- **`frontend/dist/` MUST be ignored**:
  `wails build` on PVE automatically invokes `npm run build` in `frontend/` right before Go compilation, generating `frontend/dist` directly on PVE. Syncing these hundreds of hashed static assets back to Mac causes massive I/O churn, dirty Git state, and unnecessary synchronization traffic.
- **`build/bin/` MUST be ignored**:
  `build/bin/` contains platform-dependent native executables (e.g. Linux ELF binaries on PVE, macOS `.app` on Mac). Syncing platform-specific binaries between Linux and Mac causes executable permission conflicts and unusable local binaries.
- **CRITICAL: NEVER blanket ignore `build/` in Wails**:
  Wails stores native packaging templates in `build/darwin` (Info.plist, icons) and `build/windows` (manifests, icons). A blanket `build/` ignore will break Wails compilation. Only `build/bin/` and temporary artifacts should be ignored.

---

## Standard Workflow: Declarative `mutagen.yml` + `mutagen project start`

The declarative configuration workflow is the **official standard** because `mutagen.yml` stays in the project root, can be version-controlled, and encapsulates project lifecycle management.

### Step 1: Generate `mutagen.yml`
Create a `mutagen.yml` file in the project root. Example for a Wails project:

```yaml
sync:
  defaults:
    mode: "two-way-resolved"
    ignore:
      vcs: true # Automatically respects .git and .gitignore
      paths:
        - ".DS_Store"
        - ".idea/"
        - ".vscode/"
        - ".agent/"
        - ".gemini/"
        - ".codex/"
        - "*.log"
        - "tmp/"
        - "temp/"
        # Wails packaging & build ignores
        - "build/bin/"
        - "build/windows/*.syso"
        - "frontend/dist/"
        - "frontend/node_modules/"
        # Go build output
        - "bin/"
        - "vendor/"
        - "*.test"
        - "*.out"
    symlink:
      mode: "posix-raw"

  <project_name>:
    alpha: "."
    beta: "Antigravity:/root/Projects/<project_name>"
```

### Step 2: Ensure Remote Directory Exists
```bash
ssh Antigravity "mkdir -p /root/Projects/<project_name>"
```

### Step 3: Launch with `mutagen project start`
Run inside the project root:
```bash
mutagen project start
```

### Step 4: Manage & Monitor Project Lifecycle
- **Check Project Status**: `mutagen project list` (or `mutagen sync list`)
- **Pause Synchronization**: `mutagen project pause`
- **Resume Synchronization**: `mutagen project resume`
- **Flush Pending Changes**: `mutagen project flush`
- **Terminate Synchronization**: `mutagen project terminate`

---

## Automated Execution (Via Helper Script)

This skill provides a helper script that automates the entire process in one shot:

```bash
# 1. Preview detected rules without making changes (Dry Run)
python3 ~/.gemini/config/plugins/dev-team/skills/setup-mutagen/scripts/setup_mutagen.py --dry-run

# 2. Standard Workflow: Write mutagen.yml and execute `mutagen project start`
python3 ~/.gemini/config/plugins/dev-team/skills/setup-mutagen/scripts/setup_mutagen.py --start

# 3. Write configuration file only (without starting)
python3 ~/.gemini/config/plugins/dev-team/skills/setup-mutagen/scripts/setup_mutagen.py --write-config

# 4. Ad-hoc alternative: Create standalone sync session via `mutagen sync create`
python3 ~/.gemini/config/plugins/dev-team/skills/setup-mutagen/scripts/setup_mutagen.py --create
```

---

## Post-Setup Integration
Once synchronization is established:
1. Update `~/.gemini/Projects/<project_name>/IRON_RULES.md` to reflect `Project-Environment: PVE-Native` if remote execution is intended.
2. The project is now ready for `pve-dispatch` (which queries `mutagen sync list` to resolve the `Beta` URL path) and `night-shift`.
