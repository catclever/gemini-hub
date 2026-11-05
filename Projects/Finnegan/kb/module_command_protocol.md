# Pluggable Module Command Protocol & Universal Two-Stage Parameter Assembly

**Location**: `~/.gemini/Projects/Finnegan/kb/module_command_protocol.md`  
**Status**: Active / Production  
**Implemented In**: `core/module/command.go`, `app.go`, `modules/bugu/module.go`, `frontend/src/App.svelte`  

---

## 1. Architectural Philosophy: Zero-UI Extensibility

In Finnegan's consciousness stream sandbox, modules are autonomous feature extensions (e.g. `bugu` deep-web radar, `atproto` broadcast, future weaving synthesizers). Rather than hardcoding module-specific UI forms and buttons in the frontend, Finnegan introduces the **Pluggable Module Command Protocol**:

1. **Self-Contained Declaration**: Each module declares within its own Go package whether it supports user-triggered commands, what trigger syntax it binds to, and what parameters it requires.
2. **Zero-UI Requirement for Modules**: Modules write zero lines of frontend Svelte/CSS code. The central Omnibar runtime dynamically reads registered command metadata via Wails IPC and automatically generates interactive input palettes, candidate autocompletion, and keyboard workflows.
3. **Universal Parameter Assembly Pattern**: Complex parameter bindings (such as selecting a target card as an argument) follow a standardized platform-level two-stage keyboard state machine.

---

## 2. Go Core Specification (`core/module/command.go`)

### 2.1 Types and Data Models

```go
package module

import "context"

type ParamType string

const (
	ParamTypeNone ParamType = "none" // Parameterless command
	ParamTypeCard ParamType = "card" // Requires a card entity/ID as argument
	ParamTypeText ParamType = "text" // Requires a freeform text string
)

// ParamSpec defines an argument slot expected by a command
type ParamSpec struct {
	Name        string    `json:"name"`        // e.g. "card"
	Type        ParamType `json:"type"`        // "none" | "card" | "text"
	Description string    `json:"description"` // User-facing placeholder prompt
	DataSource  string    `json:"dataSource"`  // Candidate source, defaults to "local_cards"
}

// CommandDef encapsulates a user-invocable action exported by a module
type CommandDef struct {
	ID          string      `json:"id"`                    // Unique ID, e.g. "bugu:radar", "atproto:publish"
	Name        string      `json:"name"`                  // Human-friendly title, e.g. "布谷深网雷达"
	Trigger     string      `json:"trigger"`               // Trigger prefix, e.g. "bugu", "bsky-push"
	Description string      `json:"description"`           // Subtitle or documentation
	Params      []ParamSpec `json:"params"`                // Parameter specification slots
	Namespace   string      `json:"namespace,omitempty"`  // 模块专名 (Canonical namespace, e.g. "bugu", "bsky")
	IsPrimary   bool        `json:"isPrimary,omitempty"`  // 是否为模块专名主命令 (Flagship/most frequent operation)
	SubCommand  string      `json:"subCommand,omitempty"` // 子命令标识 (Sub-command slug, e.g. "push")
}

// CommandProvider is an optional interface implemented by command-capable modules
type CommandProvider interface {
	GetCommands() []CommandDef
	ExecuteCommand(ctx context.Context, cmdID string, params map[string]interface{}) (interface{}, error)
}
```

### 2.2 Global App Dispatcher (`app.go`)

The core application acts as a discovery and routing bus:
- **`GetRegisteredCommands() []module.CommandDef`**:
  Scans all registered modules in `module.GetRegistry()`. If a module implements `CommandProvider`, its command definitions are collected and delivered to the frontend.
- **`ExecuteModuleCommand(cmdID string, params map[string]interface{}) (interface{}, error)`**:
  Routes the invocation request to the owning module's `ExecuteCommand` handler, providing an active `context.Context`.

---

## 3. Module Implementation Example: Bugu Deep-Web Radar

In `modules/bugu/module.go`, the Bugu module implements `CommandProvider`:

```go
// Compile-time interface check
var _ module.CommandProvider = (*BuguModule)(nil)

func (b *BuguModule) GetCommands() []module.CommandDef {
	return []module.CommandDef{
		{
			ID:          "bugu:radar",
			Name:        "布谷深网雷达",
			Trigger:     "bugu",
			Description: "吾道不孤",
			Params: []module.ParamSpec{
				{
					Name:        "card",
					Type:        module.ParamTypeCard,
					Description: "吾道不孤",
					DataSource:  "local_cards",
				},
			},
		},
	}
}

func (b *BuguModule) ExecuteCommand(ctx context.Context, cmdID string, params map[string]interface{}) (interface{}, error) {
	if cmdID == "bugu:radar" {
		// Extracts card content and asynchronously launches deep-web search plan
		var content string
		if cardObj, ok := params["card"].(map[string]interface{}); ok {
			content, _ = cardObj["content"].(string)
		}
		go b.RunRadar(content)
		return map[string]string{"status": "dispatched"}, nil
	}
	return nil, fmt.Errorf("unknown command: %s", cmdID)
}
```

---

## 3.2 Canonical Namespace (专名) & Sub-Command Architecture

To prevent command clutter and create a clean mental model for users:
1. **Module Canonical Proper Name (`Namespace`)**:
   - Each module declares a concise user-facing namespace: e.g. `bugu`, `bsky`.
2. **Primary Flagship Command (`IsPrimary: true`)**:
   - The primary command binds directly to the module proper name (e.g. `/bugu`, `/bsky`).
   - It represents the module's most frequent and essential entry point (e.g. `/bugu` for deep-web radar, `/bsky` for ATProto inspiration echo).
3. **Sub-Commands (`IsPrimary: false`, `SubCommand: "..."`)**:
   - Ancillary operations are declared as sub-commands under the module's namespace (e.g. `push` -> `/bsky-push`).
   - **Dual Syntax Flexibility**: Users can invoke sub-commands either via hyphenated trigger (`/bsky-push`) or natural space-separated syntax (`/bsky push [args]`). The OmniBar parser (`resolveCommandInput` in `src/lib/commandEngine.ts`) automatically resolves both styles.
4. **Visual Hierarchy & Suggestion Dropdown**:
   - In `CommandDropdown.svelte`, commands display module-specific icons (`🦋` for Bluesky, `🕊️` for Bugu) and distinct badges (`bsky 专名` vs `bsky · push`), with primary commands ranked ahead of sub-commands.

---

## 4. Universal Two-Stage Keyboard Assembly Workflow

In `frontend/src/App.svelte`, the Omnibar enforces a standardized two-stage assembly flow for any command requiring entity arguments:

```
[Normal Input] ── (Type '/') ──► [Command Palette] ── (Enter/Tab) ──► [Param Assembly]
                                                                            │
      ┌─────────────────────────────────────────────────────────────────────┘
      ▼
1. Type Keyword (250ms debounced SearchLocalCards)
2. Dropdown suggests matching cards (ArrowUp / ArrowDown navigation)
      │
      ▼ 【First Enter: Pick / Lock】
3. Lock card into parameter slot: [🔭 /bugu] [📄 Card Title ✕]
4. Helper Prompt: "按 Enter 发送命令，按 Esc 重新选择"
      │
      ▼ 【Second Enter: Submit / Dispatch】
5. Dispatches ExecuteModuleCommand via Wails IPC
6. Displays glass toast notification: "布谷深网雷达 已启动..."
7. Cleanses Omnibar back to normal write mode
```

### Safety & Backtracking:
- **`Esc` or `Backspace` (while locked)**: Unlocks the card argument slot without abandoning the command, letting the user immediately re-search or choose a different card.
- **`Esc` or `Backspace` (when input is empty)**: Dismantles the command badge and returns the user cleanly to freeform thought writing.

### 4.1 Candidate Card Palette UX & Search Hit Excerpting
To keep the parameter selection experience lightweight and distraction-free:
1. **Reverse Chronological Sorting**:
   - Both Go backend storage (`storage.go:LoadLocalCards`, `core/search/search.go:SearchCards`) and the frontend candidate pool (`OmniBar.svelte`) enforce `CreatedAt` descending order, ensuring newly captured thoughts appear at the very top.
2. **Single-Line Raycast Style**:
   - The candidate dropdown displays a compact single-line item (`padding: 9px 16px`, `white-space: nowrap`, `text-overflow: ellipsis`). Verbose body previews (`.card-item-snippet`) are stripped from the DOM.
3. **Contextual Excerpting for Long Content (`src/lib/cardTitle.ts`)**:
   - When searching with a query, if the card has a generic placeholder title (`Thought`, `Card`, etc.) or if the match occurs inside the body text, the title dynamically displays a centered contextual window (`...preceding_text match_word following_text...`) around the first hit.
   - **Zero Data Loss**: This excerpting is strictly a presentation-layer transform. The card's underlying `.content` remains 100% complete and untouched, ensuring modules (such as Bugu radar) receive full context.
