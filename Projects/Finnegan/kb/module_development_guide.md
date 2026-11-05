---
description: 'Finnegan 模块与插件开发指南（涵盖内置静态模块 =y 与外部独立单文件/目录插件 =m 的完整开发流程、契约参考与代码示例）'
---

# Finnegan 模块与插件开发指南 (Module & Plugin Developer Guide)

Finnegan 支持两种完全同构的模块开发与分发方式：
- **模式一：内置模块（Built-in `=y`）**：位于源码树 `modules/<name>/`，与宿主一同静态编译，适合官方核心模块或高频调用的基础设施模块。
- **模式二：外部热插拔插件（External `=m`）**：部署于用户目录 `<home>/.finnegan/plugins/`，支持**单文件 `.plugin` 二进制**或**多语言插件目录（`plugin.yml`）**，无需重新编译 Finnegan 本体即可热插拔或覆盖同名内置模块。

---

## 1. 模式一：开发内置模块 (`modules/<name>/`)

### 1.1 目录结构规范
```text
modules/<name>/
├── module.go          # 实现 module.Module, ManifestProvider, CommandProvider, ActionProvider
├── module_test.go     # 单元测试（验证 Manifest、Commands 与 Action 路由）
└── ...                # 模块内部子包（注意：仅允许依赖 Finnegan/core/*，严禁跨模块依赖）
```

> **铁律**：模块内部若需调用大模型，必须统一使用 [`Finnegan/core/llm`](file:///Users/kael/Projects/Finnegan/core/llm/client.go)（`corellm.GenerateCompletion` 与 `corellm.CleanJSONText`），**严禁** import 其他模块的子包（例如 `Finnegan/modules/bugu/...`）。

### 1.2 完整后端模板 (`modules/example/module.go`)
```go
package example

import (
	"context"
	"fmt"

	corellm "Finnegan/core/llm"
	coremodels "Finnegan/core/models"
	"Finnegan/core/module"
)

type ExampleConfig struct {
	Endpoint string `yaml:"endpoint"`
	LLMID    string `yaml:"llm_id"`
}

type ExampleModule struct {
	cfg *ExampleConfig
	ctx *module.Context
}

// 编译期接口契约检查
var _ module.Module = (*ExampleModule)(nil)
var _ module.ManifestProvider = (*ExampleModule)(nil)
var _ module.CommandProvider = (*ExampleModule)(nil)
var _ module.ActionProvider = (*ExampleModule)(nil)

func init() {
	module.Register(&ExampleModule{})
}

func (m *ExampleModule) Name() string {
	return "example"
}

func (m *ExampleModule) ConfigTarget() interface{} {
	if m.cfg == nil {
		m.cfg = &ExampleConfig{
			Endpoint: "https://api.example.com",
			LLMID:    "default",
		}
	}
	return m.cfg
}

func (m *ExampleModule) Init(ctx *module.Context) error {
	m.ctx = ctx
	return nil
}

func (m *ExampleModule) Bindings() []interface{} {
	return []interface{}{m}
}

// 1. 自描述清单：声明主题色、信标动画、收集按钮覆写策略、专属卡片类型与命令
func (m *ExampleModule) GetManifest() module.ModuleManifest {
	return module.ModuleManifest{
		Name:       "example",
		Version:    "1.0.0",
		ThemeColor: "#10b981",   // 翡翠绿主题光效
		BeaconType: "radar",     // 可选："radar" | "butterfly" | "none"
		PromotionStrategy: &module.PromotionStrategySpec{
			Icon:             "anchor_comment",          // "default_book" 或 "anchor_comment"
			Tooltip:          "附着母卡收录（附带批注）",
			HasCommentPrompt: true,
			Placeholder:      "写下你的批注（回车直接收录）...",
			BindMotherCard:   true,
		},
		CardTypes: []module.CardTypeSpec{
			{Type: "example_card"},
		},
		Commands: m.GetCommands(),
	}
}

// 2. 声明 Omnibar 斜杠命令
func (m *ExampleModule) GetCommands() []module.CommandDef {
	return []module.CommandDef{
		{
			ID:          "example:scan",
			Name:        "示例深空探测",
			Trigger:     "ex",
			Description: "围绕选定卡片触发探测",
			Namespace:   "example",
			IsPrimary:   true,
			Params: []module.ParamSpec{
				{
					Name:                "card",
					Type:                module.ParamTypeCard,
					Description:         "选择目标母卡",
					DataSource:          "cards",
					RequireKeywords:     true,
					ExcludedTypes:       []string{"note"},
					AutoStageToViewport: true,
				},
			},
		},
	}
}

// 3. 执行 Omnibar 命令并通过 HostAPI 流式投递卡片
func (m *ExampleModule) ExecuteCommand(ctx context.Context, cmdID string, params map[string]interface{}) (interface{}, error) {
	if cmdID != "example:scan" {
		return nil, fmt.Errorf("unknown command: %s", cmdID)
	}

	var motherCardID, content string
	if cardMap, ok := params["card"].(map[string]interface{}); ok {
		motherCardID, _ = cardMap["id"].(string)
		content, _ = cardMap["content"].(string)
	}

	go func() {
		if m.ctx != nil && m.ctx.Host != nil {
			// 如需调用 LLM：
			llmCfg := m.ctx.LLMs["default"]
			_, _ = corellm.GenerateCompletion(ctx, llmCfg, llmCfg.DefaultModel, content)

			// 实时向 3D 星空舞台投递生成的卡片
			m.ctx.Host.SpawnCard(coremodels.BabelCard{
				Origin:        "example",
				Title:         "Example Echo",
				Content:       "探测返回的灵感内容",
				EchoOf:        motherCardID,
				MatchedAnchor: "核心锚点",
			})
			// 通知宿主本次会话完成，收起雷达/蝴蝶信标
			m.ctx.Host.CompleteSession(motherCardID)
		}
	}()

	return map[string]interface{}{"status": "triggered", "card_id": motherCardID}, nil
}

// 4. 响应前端卡片内部触发的自定义动作
func (m *ExampleModule) ExecuteAction(ctx context.Context, actionID string, payload map[string]interface{}) (interface{}, error) {
	if actionID == "refresh_price" {
		return map[string]interface{}{"status": "ok"}, nil
	}
	return nil, fmt.Errorf("unknown action: %s", actionID)
}
```

### 1.3 挂载内置模块
在根包 [`main.go`](file:///Users/kael/Projects/Finnegan/main.go) 顶部添加一行空白导入即可完成编译期挂载（无需修改 `app.go` 或任何核心代码）：
```go
import (
	_ "Finnegan/modules/example"
)
```

---

## 2. 模式二：开发外部独立插件 (`~/.finnegan/plugins/`)

外部插件运行在独立子进程中，与内置模块享有**完全相同的能力**（斜杠命令、母卡连线、信标动画、收集按钮批注覆写、自定义卡片 UI）。

### 2.1 方式 A：单文件自包含 `.plugin` 二进制（推荐 Go 开发者）
将后端逻辑与编译后的前端 `ui.js` 通过 `//go:embed` 打包进单个二进制文件 `<name>.plugin`，放入 `<home>/.finnegan/plugins/<name>.plugin`（赋予可执行权限 `chmod +x`）。

```go
package main

import (
	_ "embed"
	"encoding/json"
	"fmt"
	"os"
)

//go:embed dist/ui.js
var uiBundle []byte

func main() {
	// 1. 响应宿主清单探测
	if len(os.Args) > 1 && os.Args[1] == "--finnegan-manifest" {
		manifest := map[string]interface{}{
			"name":        "taobao",
			"version":     "1.0.0",
			"description": "淘货灵感雷达插件",
			"themeColor":  "#ff5000",
			"beaconType":  "radar",
			"promotionStrategy": map[string]interface{}{
				"icon":             "anchor_comment",
				"tooltip":          "附带心愿批注收入星轨",
				"hasCommentPrompt": true,
				"placeholder":      "备注预算或入手理由...",
				"bindMotherCard":   true,
			},
			"cardTypes": []map[string]interface{}{
				{"type": "taobao_item", "uiEntry": "/api/plugins/taobao/ui.js"},
			},
			"commands": []map[string]interface{}{
				{
					"id":          "taobao:hunt",
					"name":        "淘货雷达",
					"trigger":     "tb",
					"description": "根据灵感卡片搜寻好物",
					"isPrimary":   true,
				},
			},
		}
		_ = json.NewEncoder(os.Stdout).Encode(manifest)
		return
	}

	// 2. 响应宿主前端 UI Bundle 提取
	if len(os.Args) > 1 && os.Args[1] == "--finnegan-ui" {
		_, _ = os.Stdout.Write(uiBundle)
		return
	}

	// 3. 处理命令 / 动作调用（读取 stdin JSON，输出 NDJSON 流）
	var req struct {
		Type   string                 `json:"type"`   // "command" | "action" | "promote_hook"
		ID     string                 `json:"id"`     // 命令 ID 或动作 ID
		Params map[string]interface{} `json:"params"` // 参数载荷
	}
	if err := json.NewDecoder(os.Stdin).Decode(&req); err != nil {
		fmt.Fprintf(os.Stderr, "invalid input: %v\n", err)
		os.Exit(1)
	}

	// 流式输出第 1 张卡片（宿主立即渲染上屏）
	emitNDJSON(map[string]interface{}{
		"event": "spawn_card",
		"card": map[string]interface{}{
			"origin":         "taobao",
			"title":          "复古黄铜台灯",
			"content":        "手工锻造黄铜灯罩，暖光护眼",
			"source_url":     "https://item.taobao.com/...",
			"matched_anchor": "书房器物",
		},
	})

	// 结束会话并输出最终结果
	emitNDJSON(map[string]interface{}{
		"event":   "complete_session",
		"card_id": "",
	})
	emitNDJSON(map[string]interface{}{
		"result": map[string]interface{}{"status": "ok"},
	})
}

func emitNDJSON(v interface{}) {
	b, _ := json.Marshal(v)
	fmt.Println(string(b))
}
```

### 2.2 方式 B：目录型插件 (`<home>/.finnegan/plugins/<name>/plugin.yml`)
适合使用 Python / Node.js / Rust 快速编写插件：
```text
~/.finnegan/plugins/my_plugin/
├── plugin.yml     # 插件元数据清单
├── plugin         # 可执行脚本或二进制（chmod +x）
└── ui.js          # 可选：自定义卡片渲染组件 ESM bundle
```
`plugin.yml` 示例：
```yaml
name: my_plugin
version: "0.1.0"
description: "自定义外部插件"
executable: "./plugin"
ui_bundle: "ui.js"
theme_color: "#a855f7"
beacon_type: "butterfly"
promotion_strategy:
  icon: "anchor_comment"
  tooltip: "附带批注收集"
  has_comment_prompt: true
  placeholder: "输入批注..."
  bind_mother_card: true
commands:
  - id: "my_plugin:run"
    name: "运行外部插件"
    trigger: "mp"
    description: "触发自定义外部插件"
    is_primary: true
```

---

## 3. 前端扩展机制与自定义卡片 UI 开发

### 3.1 收集按钮覆写 (`PromotionStrategySpec`)
无需编写任何前端代码，只需在 `GetManifest()` 或 `plugin.yml` 中配置 `PromotionStrategy`，[`CardCollectControl.svelte`](file:///Users/kael/Projects/Finnegan/frontend/src/components/cards/CardCollectControl.svelte) 即会自动为 `card.origin === "<module_name>"` 的临时卡片启用对应收集体验：
- `icon: "default_book"` + `hasCommentPrompt: false`：默认「翻开典籍加页」动效，点击即刻落盘。
- `icon: "anchor_comment"` + `hasCommentPrompt: true` + `bindMotherCard: true`：点击后展开内联批注输入框，回车后将卡片连同用户批注作为子卡绑定至母卡并折叠进母卡叠层。

### 3.2 自定义卡片组件注册 (`CardTypeSpec` & `ui.js`)
1. **内置模块卡片组件**：
   在 `frontend/src/components/cards/` 下创建 `<Name>CardBody.svelte`，并在 [`cardRegistry.ts`](file:///Users/kael/Projects/Finnegan/frontend/src/components/cards/cardRegistry.ts) 的 `builtinRegistry` 中注册。
2. **外部插件动态 `ui.js` 组件**：
   外部插件只需导出一个符合 Svelte 组件挂载签名（或 Custom Element 包装器）的 `default` 导出，构建为单文件 ESM `ui.js`。组件接收以下标准 Props：
   - `card: CosmicCard`：卡片完整数据对象。
   - `isFocused: boolean`：`false` 为 200×190 散落态，`true` 为 420×420 居中聚焦态。
   - `displayTime: string`：已由全局时钟计算好的相对时间字符串。
3. **在卡片内调用模块后端动作**：
   前端组件可通过 Wails 统一桥接函数直接触发模块后端的 `ActionProvider.ExecuteAction`：
   ```ts
   import { ExecuteModuleAction } from '../../wailsjs/go/main/App.js';

   await ExecuteModuleAction('atproto', 'fetch_comments', {
     uri: card.sourceUrl,
     parentCardId: card.id,
   });
   ```

---

## 4. 模块开发自检清单 (Verification Checklist)

1. **零耦合检查**：运行 `go list -f '{{.Imports}}' .`，确认根包不直接依赖 `Finnegan/modules/<name>/...` 子包；模块内部不依赖其他兄弟模块。
2. **契约完整性测试**：在 `modules/<name>/module_test.go` 中编写单元测试，断言 `GetManifest()` 返回的 `Name`、`ThemeColor`、`BeaconType`、`PromotionStrategy` 与 `GetCommands()` 符合预期。
3. **空指针防御**：在 `Init(ctx *module.Context)` 与 `ExecuteCommand` 中安全判空 `ctx != nil`、`ctx.LLMs != nil`、`ctx.Host != nil`，确保模块在无宿主 Mock 环境下可独立单测。
