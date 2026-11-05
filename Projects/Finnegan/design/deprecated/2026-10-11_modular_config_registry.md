---
title: "Unified Modular Configuration System"
date: 2026-10-11
status: tentative
---

# Unified Modular Configuration System (含全局 LLM)

## 1. 痛点
1. **配置散落**：`bugu`、`atproto` 等模块各自读取环境变量或私有配置。
2. **大模型逻辑重复**：目前 LLM 调用代码直接硬编码在 `bugu/llm/router.go` 中（手工拼接 JSON，写死了 Gemini 3.8 Flash）。未来其他模块（如收件箱自动打标签）如果需要用大模型，会导致严重的逻辑重复和 API Key 分裂。

## 2. 扁平化的一级配置节点
取消 `modules:` 命名空间。在 `<home>/.finnegan/config.yml` 中，模块名直接作为一级节点。为了避免与核心配置冲突，模块注册时系统会检查命名冲突。

```yaml
# 核心配置
external_projects: []
debounce_ms: 300

# 全局 LLM 核心模块
llm:
  provider: "gemini"               # gemini / openai / anthropic / ollama
  api_key: "AIzaSy..."             # 全局唯一的大模型 Key
  default_model: "gemini-3.8-flash"

# 各业务模块
bugu:
  searxng_url: "http://127.0.0.1:8080"
  max_concurrency: 2
  # bugu 不再需要配大模型 key，直接调用全局 llm

atproto:
  pds_url: "https://bsky.social"
  did: "did:plc:..."
```

## 3. 全局 LLM 模块 (core/llm)

把大模型抽离为一个全局的核心设施。由于 Finnegan 大量需要大模型输出结构化数据（如 Bugu 的搜索计划），全局 LLM 必须原生支持**结构化输出 (Structured Output)**。

```go
package llm

import "context"

// 全局唯一的 LLM 客户端接口
type Client interface {
    // 基础文本生成
    GenerateText(ctx context.Context, prompt string, systemInstruction string) (string, error)
    
    // 结构化数据生成（自动绑定 JSON Schema）
    GenerateStructured(ctx context.Context, prompt string, systemInstruction string, resultStruct interface{}) error
}

// 在 app 启动时初始化
func InitGlobalLLM(cfg *Config) error { ... }
```

## 4. 动态注册表实现 (YAML Node Decode)

```go
var registry = make(map[string]interface{})

func RegisterModuleConfig(name string, cfgPtr interface{}) {
    registry[name] = cfgPtr
}

type GlobalConfig struct {
    ExternalProjects []string             `yaml:"external_projects"`
    DebounceMs       int                  `yaml:"debounce_ms"`
    
    // 接收所有未显式定义的一级节点
    RawModules       map[string]yaml.Node `yaml:",inline"` 
}

func LoadConfig(path string) (*GlobalConfig, error) {
    // 1. 先把基础配置读出来，其余的全放进 RawModules
    // 2. 遍历已注册的模块
    for name, cfgPtr := range registry {
        if node, exists := cfg.RawModules[name]; exists {
            node.Decode(cfgPtr) // 精准注入
        }
    }
}
```
