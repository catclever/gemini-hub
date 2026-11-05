---
id: expose_append_file_and_sync_prompts_024
title: 暴露独立 append_file 工具、打通 max_turns 参数并同步分块提示词
status: completed
priority: high
tags:
- tools
- headless
- prompts
session: 7bcc4e71-1830-415f-a436-44cffb3b1aa2
---

# 暴露独立 append_file 工具、打通 max_turns 参数并同步分块提示词

## 任务目标与背景
暴露独立 append_file 工具，打通 main.rs run 入口的 max_turns 透传，并在 main.rs 与 bench.rs 中同步大文件分块写入提示词，避免大模型生成长代码时的 token 截断。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

### 交付与验证总结

1. **`append_file` 独立工具定义与分发 (`src/tools.rs`, `src/server.rs`)**:
   - 暴露独立的 `append_file_tool_def` 工具，参数为 `path` 和 `content`（必选）。
   - 实现 `execute_append_file`，在复用底层的追加与安全牢笼路径的同时，保证 `write_file` 的 `append: bool` 向下兼容。
   - 注册至 `all_local_tool_schemas`（13项本地工具）、`all_mcp_tools`（17项MCP工具）、`tool_by_name`，以及 `src/server.rs` 的 `tools/call` JSON-RPC 消息分发中。
2. **打通无头模式 `--max-turns` 透传 (`src/main.rs`)**:
   - `Commands::Run` 新增 `--max-turns` 参数（默认 50 轮）。
   - `run_headless_agent` 组装 `init_payload` 时透传 `"max_turns"`，彻底杜绝复杂长任务在云端 30 轮被提前掐断的问题。
3. **系统提示词同步大文件防截断指引 (`src/main.rs`, `src/bench.rs`)**:
   - 在 `main.rs` 的 `default_system_prompt` 中加入 `>3KB` 大文件分块指引（推荐先写骨架，再通过 `append_file` 或 `replace_symbol` 追加与替换）。
   - 在 `bench.rs` 中同步优化提示词，明确推荐使用 `append_file`。
4. **验证与部署**:
   - 新增 `test_append_file_tool_execution` 单元测试，更新 Preset 全量测试断言（17 tools）。
   - 35 项单测在 PVE 上全绿通过 (`cargo test` 35 passed, 0 failed)。
   - Release 二进制重新编译并成功覆盖安装至 PVE 生产路径 `/root/.cargo/bin/enginedge`。
   - Git 变更已提交并推送到 GitHub `origin/main` (`41de07f`)。
