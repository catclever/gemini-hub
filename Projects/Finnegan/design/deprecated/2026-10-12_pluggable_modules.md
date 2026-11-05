---
title: "Pluggable Module Architecture & LLM Delegation"
date: 2026-10-12
status: tentative
---

# 插件化模块架构与大模型网络层设计

## 1. 可行性分析 (Feasibility)

### 1.1 第三方模块可插拔 (Caddy-style 编译期插件)
在 Go 语言中，最成熟、无跨平台兼容性问题的“可插拔”方案是 **Caddy 模式（空导入注册）**。
- **第三方开发**：任何人都可以写一个独立的 Go package。
- **接入方式**：在 Finnegan 的一个入口文件里写一行 `_ "github.com/some/third-party-module"`，然后重新编译 Wails 即可。
- **前端接入**：Wails 原生支持绑定多个 struct（`Bind: []interface{}{ app, pluginA, pluginB }`），第三方模块可以直接把自己的 Go 方法暴露给 Svelte 前端。

### 1.2 Core 只做网络层，大模型逻辑下放
完全可行，且更符合模块独立性。
- **Core 的职责**：只负责在 `config.yml` 里统一收口 API Key、代理设置、并发限制和全局提供商（Provider）信息。
- **Module 的职责**：模块自己引入官方的 SDK（比如 `github.com/google/genai-go`），自己写 Prompt，自己定义 JSON Schema。模块向 Core 请求 LLM 配置，如果有就用，没有就用模块自己配置的 Key。

## 2. 核心改造点 (Modification Points)

### 2.1 建立标准化模块接口 (`core/module.go`)
定义一个所有模块必须遵守的协议：

```go
package module

// 模块上下文，由 Core 传给模块，提供底层设施
type Context struct {
    LLMConfig  func() LLMConfig       // 暴露全局大模型配置（网络层）
    Storage    StorageInterface       // 暴露数据库层
    Watcher    WatcherInterface       // 暴露文件监听总线
}

// 模块标准接口
type Module interface {
    Name() string                     // 模块名（如 "bugu"），用作 config.yml 里的一级节点
    ConfigTarget() interface{}        // 返回该模块专属配置的结构体指针（用于 YAML 自动注入）
    Init(ctx *Context) error          // 初始化逻辑
    Bindings() []interface{}          // 可选：需要暴露给 Wails 前端 API 的结构体
}

// 全局注册表
var registry = make(map[string]Module)

func Register(m Module) {
    registry[m.Name()] = m
}
```

### 2.2 全局 LLM 配置模型下沉为“环境提供者”
在 `config.yml` 中：
```yaml
llm:
  provider: "gemini"               
  api_key: "AIzaSy..."             
  base_url: ""                     # 供本地模型或反向代理使用

bugu:
  searxng_url: "http://..."
  # bugu 自己不写 api_key，依赖全局
```

在模块中（比如 Bugu）：
```go
func (b *BuguModule) Init(ctx *module.Context) error {
    llmCfg := ctx.LLMConfig()
    if llmCfg.APIKey != "" {
        // 使用全局 Key 实例化官方 SDK
        b.geminiClient = genai.NewClient(llmCfg.APIKey)
    } else if b.myConfig.FallbackKey != "" {
        // 全局没有，使用模块自己的后备 Key
        b.geminiClient = genai.NewClient(b.myConfig.FallbackKey)
    }
    return nil
}
```

### 2.3 改造现有的 App 和 Bugu
1. **抽离 Bugu**：把现有的 `bugu` 改造成实现了 `Module` 接口的包，在其 `init()` 中调用 `module.Register(&BuguModule{})`。
2. **前端 API 解耦**：把 `app.go` 里属于 Bugu 的 `GetRadarTargets`、`RunRadar` 移交回 Bugu 自己，通过 `Bindings()` 暴露给 Wails。
3. **改造 Bugu 大模型调用**：废弃 `bugu/llm/router.go` 里的手工 HTTP 拼接，直接引入 Google 官方的 Go SDK。

## 3. 模块的极致独立性 (Bugu 的外部复用)

如果 Bugu 未来可能脱离 Finnegan 用在别的地方（比如一个 Telegram 机器人，或者纯 CLI 工具），那么 Bugu **绝对不能** import Finnegan 的 `core` 包。我们需要采用 **适配器模式 (Adapter Pattern) / 依赖注入**：

### 3.1 Go 的包级复用
在 Go 中，如果 Finnegan Core 和 Bugu 都引入了 Google 的 `genai-go` SDK，Go 编译器会自动复用这个依赖包，最终的二进制文件里只会有一份代码，不存在包冗余的问题。

### 3.2 实例级的复用与依赖注入
为了让 Bugu 完全独立，Bugu 内部只定义自己需要的“标准接口”或者直接接收参数，不关心配置从哪来：

**独立的 Bugu 库 (完全不知道 Finnegan 的存在)：**
```go
package bugu

import "github.com/google/genai-go"

type Engine struct {
    llmClient *genai.Client // Bugu 直接复用官方 SDK 实例
}

// 独立的初始化方法
func NewEngine(geminiKey string, searxngURL string) *Engine {
    return &Engine{
        llmClient: genai.NewClient(geminiKey),
    }
}
```

**Finnegan 里的适配层 (`finnegan/modules/bugu_plugin.go`)：**
```go
package modules

import (
    "Finnegan/core/module"
    "path/to/standalone/bugu"
)

type BuguPlugin struct {
    engine *bugu.Engine
}

func (p *BuguPlugin) Init(ctx *module.Context) error {
    // 1. 从 Finnegan Core 获取全局 LLM 配置 (复用 Finnegan 的全局设施)
    llmCfg := ctx.LLMConfig()
    
    // 2. 将全局配置“注入”给独立的 Bugu 引擎
    p.engine = bugu.NewEngine(llmCfg.APIKey, p.MyConfig.SearxngURL)
    return nil
}
```

**结论**：
通过在 Finnegan 和 Bugu 之间加一层很薄的“Plugin Adapter”，我们既能享受 Finnegan 全局配置统一管理的红利，又能保证 Bugu 作为一个纯粹的 Go Package 随时可以被其他项目复用（或者开源出去）。
