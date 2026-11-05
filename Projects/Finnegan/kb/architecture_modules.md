---
description: 'Finnegan 双模可插拔模块架构设计（Built-in 静态编译与 External 独立进程插件桥接、契约接口与前端动态水合机制）'
---

# Finnegan 双模可插拔模块架构设计 (Dual-Mode Pluggable Architecture)

## 1. 架构定位与设计原则

Finnegan 采用受 Linux 内核（`=y` 内置编译与 `=m` 动态加载）与 Caddy 模块机制启发的**双模同构可插拔架构**：
- **零反向依赖（Zero Core-to-Module Coupling）**：主程序包（`package main`）与核心层（`Finnegan/core/*`）严禁直接 `import` 任何具体业务模块的子包（如 `Finnegan/modules/bugu/*` 或 `Finnegan/modules/atproto/*`）。所有模块交互均通过 `Finnegan/core/module` 标准接口契约与 `ModuleManifest` 元数据完成。
- **双模同构共存（Built-in `=y` + External `=m`）**：同一套模块契约既支持直接编译进主程序二进制（零 IPC 开销、微秒级内存直通），也支持编译为独立单文件 `.plugin` 或插件目录放入 `<home>/.finnegan/plugins/` 实现免重编译热插拔。
- **同名热覆盖（Hot Override）**：启动时先注册内置模块（`init()`），随后扫描 `<home>/.finnegan/plugins/` 加载外部插件；若外部插件与内置模块同名，外部插件自动覆盖内置模块实例，便于独立调试与第三方替换。

```mermaid
flowchart TB
    subgraph CoreHost["Finnegan Core Host (package main & core/)"]
        Registry["module.Registry (全局模块注册表)"]
        HostAPI["appHostAPI (SpawnCard / CompleteSession / EmitEvent)"]
        LLMCore["core/llm (Gemini & OpenAI 统一客户端)"]
        AssetSrv["Wails AssetServer (/api/plugins/<name>/ui.js)"]
    end

    subgraph Builtin["Mode 1: 内置静态模块 (=y, In-Process)"]
        Bugu["modules/bugu (BuguModule)"]
        ATProto["modules/atproto (AtProtoModule)"]
        Curio["modules/curio (CurioModule)"]
    end

    subgraph External["Mode 2: 外部独立插件 (=m, ~/.finnegan/plugins/)"]
        Bridge["ExternalModule Bridge (core/module/external_bridge.go)"]
        SingleBin["<name>.plugin (单文件自包含二进制)"]
        DirPlugin["<name>/plugin.yml + bin + ui.js"]
    end

    subgraph Frontend["Svelte Cosmic Stage Frontend"]
        Hydrate["hydrateModuleManifests (promotionRegistry.ts)"]
        CardReg["loadExternalPluginCardComponents (cardRegistry.ts)"]
        Stage["CosmicStage / UICard / CardCollectControl"]
    end

    Bugu -->|init() Register| Registry
    ATProto -->|init() Register| Registry
    Curio -->|init() Register| Registry
    SingleBin <-- "--finnegan-manifest / --finnegan-ui / NDJSON stdio" --> Bridge
    DirPlugin <-- "YAML / NDJSON stdio" --> Bridge
    Bridge -->|LoadExternalPlugins| Registry
    Registry -->|GetModuleManifests()| Hydrate
    AssetSrv -->|Dynamic import()| CardReg
    Hydrate --> Stage
    CardReg --> Stage
    Bugu & ATProto & Bridge -->|HostAPI / EventBus| HostAPI
```

---

## 2. 核心层契约体系 (`Finnegan/core/module`)

### 2.1 基础生命周期契约 ([`core/module/module.go`](file:///Users/kael/Projects/Finnegan/core/module/module.go))
所有模块必须实现 `module.Module` 接口：
- `Name() string`：模块唯一标识符（同时作为 `.finnegan/config.yml` 顶层配置键、卡片 `origin` 标识及插件路由键）。
- `ConfigTarget() interface{}`：返回模块配置结构体指针，供核心层执行 4 级配置覆盖解码；无配置可返回 `nil`。
- `Init(ctx *module.Context) error`：核心层完成配置解码后调用，注入：
  - `ctx.LLMs map[string]LLMConfig`：全局 LLM 池配置（`default`、`router`、`distiller` 等）。
  - `ctx.Host HostAPI`：宿主回调接口（`SpawnCard(card models.BabelCard)`、`CompleteSession(cardID string)`、`EmitEvent(eventName string, data interface{})`）。
- `Bindings() []interface{}`：向 Wails 暴露的可选前端绑定对象切片。

### 2.2 模块自描述清单契约 ([`core/module/manifest.go`](file:///Users/kael/Projects/Finnegan/core/module/manifest.go))
模块通过可选实现 `module.ManifestProvider`（`GetManifest() ModuleManifest`）向宿主与前端声明自身的视觉主题、信标类型、收集按钮策略、专属卡片类型与 Omnibar 命令，彻底消除前端对模块名称的硬编码：

| 字段 | 类型 | 作用说明 |
| :--- | :--- | :--- |
| `name` | `string` | 模块唯一名称（如 `"bugu"`、`"atproto"`、`"curio"`） |
| `themeColor` | `string` | 模块主题色（用于连线激光、边框光效与徽标，如 `"#f59e0b"`、 `"#38bdf8"`） |
| `beaconType` | `string` | 舞台信标形态：`"radar"`（雷达波）、`"butterfly"`（蝴蝶信标）、`"none"` |
| `promotionStrategy` | `*PromotionStrategySpec` | 临时卡片右上角「收集」按钮覆写策略（图标、Tooltip、内联批注输入框、是否绑定母卡折叠） |
| `cardTypes` | `[]CardTypeSpec` | 模块提供的专属卡片类型列表（`type` 名称及可选外部前端组件路径 `uiEntry`） |
| `commands` | `[]CommandDef` | 模块注册的 Omnibar 斜杠命令定义列表 |
| `isExternal` | `bool` | 是否由外部插件桥接器加载（由核心层自动标记） |

若某个模块未显式实现 `ManifestProvider`，[`BuildModuleManifest(m Module)`](file:///Users/kael/Projects/Finnegan/core/module/manifest.go#L67-L88) 会自动回退并通过 `CommandProvider` 提取其命令列表生成基础清单。

### 2.3 扩展行为钩子契约 (`CommandProvider` / `ActionProvider` / `PromoteHookProvider`)
1. **`CommandProvider`** ([`core/module/command.go`](file:///Users/kael/Projects/Finnegan/core/module/command.go))：
   - `GetCommands() []CommandDef`：声明 Omnibar 斜杠命令及参数过滤契约（`RequireKeywords`、`ExcludedTypes`、`AllowedTypes`、`AutoStageToViewport`）。
   - `ExecuteCommand(ctx context.Context, cmdID string, params map[string]interface{}) (interface{}, error)`：处理 Omnibar 命令派发。
2. **`ActionProvider`** ([`core/module/manifest.go`](file:///Users/kael/Projects/Finnegan/core/module/manifest.go#L58-L60))：
   - `ExecuteAction(ctx context.Context, actionID string, payload map[string]interface{}) (interface{}, error)`：处理卡片内部触发的模块级异步动作（例如 Bluesky 卡片展开评论串 `actionID == "fetch_comments"`），由前端统一通过 `ExecuteModuleAction(moduleName, actionID, payload)` 或运行时事件路由调用。
3. **`PromoteHookProvider`** ([`core/module/manifest.go`](file:///Users/kael/Projects/Finnegan/core/module/manifest.go#L62-L65))：
   - `OnCardPromoted(ctx context.Context, card models.BabelCard, comment string, echoOf string) (*models.BabelCard, error)`：当用户点击临时卡片的「收集」按钮转正落盘前触发，允许模块对卡片内容、批注或元数据执行自定义增强。

---

## 3. 外部插件桥接与单文件协议 ([`core/module/external_bridge.go`](file:///Users/kael/Projects/Finnegan/core/module/external_bridge.go))

在 `App.startup()` 阶段，[`LoadExternalPlugins`](file:///Users/kael/Projects/Finnegan/core/module/external_bridge.go#L262-L292) 会自动扫描 `<home>/.finnegan/plugins/`，支持两种物理形态：

### 3.1 形态 A：单文件自包含插件 (`<name>.plugin`)
编译后的单个可执行二进制文件（内部通过 Go `embed` 嵌入前端编译产物 `ui.js`），宿主通过标准 CLI 协议标志与其交互：
- `<binary> --finnegan-manifest`：输出 JSON 或 YAML 格式的 `ModuleManifest`。
- `<binary> --finnegan-ui`：向 `stdout` 输出打包好的前端 ESM 组件代码（由宿主通过 `/api/plugins/<name>/ui.js` 零拷贝托管）。
- `<binary>`（无标志执行）：从 `stdin` 读取 JSON 请求，并通过 `stdout` 实时输出 **NDJSON（Newline-Delimited JSON）** 事件流。

### 3.2 形态 B：目录型多语言插件 (`<name>/plugin.yml`)
适用于 Python / Node.js / Rust / Shell 脚本或拆分式插件目录，包含：
- `plugin.yml`：声明 `ModuleManifest` 及 `executable`（默认 `./plugin`）与 `ui_bundle`（默认 `ui.js`）。
- 可执行文件与可选 `ui.js`。

### 3.3 实时 NDJSON 流式通信协议
当宿主调用外部插件的 `ExecuteCommand`、`ExecuteAction` 或 `OnCardPromoted` 时，向子进程 `stdin` 写入 JSON 请求载荷：
```json
{
  "type": "command",
  "id": "taobao:Radar",
  "params": { "card": { "id": "01J...", "content": "..." } },
  "config": { ... },
  "llms": { "default": { "provider": "gemini", "default_model": "gemini-3.8-flash" } }
}
```
子进程在执行期间可随时向 `stdout` 按行刷新输出 NDJSON 指令，宿主实时解析并映射为内部动作（实现与内置模块完全一致的流式飞入卡片体验）：
- `{"event": "spawn_card", "card": { ...BabelCard... }}` $\to$ 立即调用 `Host.SpawnCard` 将卡片推入 3D 星空舞台。
- `{"event": "complete_session", "card_id": "..."}` $\to$ 立即调用 `Host.CompleteSession` 结束雷达/回声信标动画。
- `{"event": "emit", "name": "custom:event", "data": { ... }}` $\to$ 透传至 Wails 前端事件总线。
- `{"result": { "status": "ok" }}`（或 `{"error": "..."}`）$\to$ 作为本次调用的最终返回值。

---

## 4. 共享基础设施与 4 级配置体系

### 4.1 核心层统一 LLM 客户端 ([`core/llm/client.go`](file:///Users/kael/Projects/Finnegan/core/llm/client.go))
- 提供 [`GenerateCompletion(ctx, llmCfg, modelName, prompt)`](file:///Users/kael/Projects/Finnegan/core/llm/client.go#L36-L49) 与 [`CleanJSONText(raw)`](file:///Users/kael/Projects/Finnegan/core/llm/client.go#L22-L33)。
- 自动根据 `llmCfg.Provider` / `llmCfg.BaseURL` 路由至 Google Gemini SDK 或 OpenAI 兼容端点（DeepSeek、本地 Ollama/vLLM 等）。
- 所有内置模块（`bugu`、`atproto` 等）共享该底层实现，严禁模块之间互相 `import` 私有 `llm` 子包。

### 4.2 4 级配置覆盖体系 (4-Tier Configuration Hierarchy)
1. **Tier 4（代码默认）**：模块在 `ConfigTarget()` 中初始化默认结构体字段。
2. **Tier 3（环境变量）**：模块在 `ConfigTarget()` 中读取 `os.Getenv` 覆盖默认值。
3. **Tier 2（模块本地配置）**：模块读取自身配置文件（如 `bugu.yml`）覆盖。
4. **Tier 1（全局最高优先级）**：宿主在 `startup()` 中读取 `<home>/.finnegan/config.yml`，按 `m.Name()` 匹配顶层 `yaml.Node` 并原位解码覆盖到 `m.ConfigTarget()`。

---

## 5. 前端动态水合与组件热加载架构

1. **启动水合（Manifest Hydration）**：
   - [`App.svelte`](file:///Users/kael/Projects/Finnegan/frontend/src/App.svelte) 在 `onMount` 中调用 Wails 绑定 `GetModuleManifests()`。
   - [`hydrateModuleManifests(manifests)`](file:///Users/kael/Projects/Finnegan/frontend/src/lib/promotionRegistry.ts#L50-L75) 将每个模块的 `PromotionStrategy`、`ThemeColor` 与 `BeaconType` 注册进前端动态注册表。
   - [`CardCollectControl.svelte`](file:///Users/kael/Projects/Finnegan/frontend/src/components/cards/CardCollectControl.svelte) 根据卡片的 `card.origin` 动态查询 `getPromotionStrategy(card.origin)`，自动决定渲染默认「典籍加页」收集按钮还是「附着母卡批注」收集框。
2. **外部卡片 UI 动态加载（Dynamic ESM Card Loader）**：
   - [`loadExternalPluginCardComponents(manifests)`](file:///Users/kael/Projects/Finnegan/frontend/src/components/cards/cardRegistry.ts#L31-L55) 遍历带有 `cardTypes` 且声明了 `uiEntry`（或 `isExternal`）的模块，通过原生 `import('/api/plugins/<pluginName>/ui.js')` 动态加载 Svelte 组件并调用 `registerCardBodyComponent(type, mod.default)`。
   - 当舞台上出现 `card.type === '<custom_type>'` 的卡片时，[`UICard.svelte`](file:///Users/kael/Projects/Finnegan/frontend/src/UICard.svelte) 自动使用该组件渲染散落态（200×190）与聚焦态（420×420）视图。
