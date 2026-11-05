# Gemini System Configuration Iron Rules

## [Global]
- **Project**: gemini
- **Workspace**: `/Users/kael/Library/XDG_Exile/gemini` (backed by symlink `~/.gemini`)
- **Role**: System-Wide Central Configuration Hub (Skills, Plugins, MCP Servers, Global Rules, Utility Scripts).
- **Self-Project Awareness (核心自我认知)**: 
  当前工作区不仅是系统配置中枢，**其本身即是一个在中央仓库注册的正规项目（Project: gemini）**。
  在此工作区内对全局 Skills、MCP 脚本（`config/scripts/`）、Plugins、全局宪法规则（`GEMINI.md`）的所有研发、重构与 Bugfix，均属于 `gemini` 项目的系统级研发任务，**绝对禁止脱离看板管理**，必须严格通过 `kanban-task-manager` MCP 工具记入 `gemini` 看板。
- **Directory Hygiene (目录纯洁性)**: 
  `tasks/` 目录专供看板任务卡片使用。严禁将技术调研报告、架构设计沉淀、排查总结随意倾倒至 `tasks/` 目录，此类文档必须全部存放于 `kb/` 或 `docs/`。

## [Main Agent]
- **Atomic Task Logging (原子化挂单)**: 在修改任何系统级配置或脚本时，必须将 `create_task` 纳入同批次执行，严禁“干完活不留痕”。
- **Definition of Done (DoD 门禁)**: 结束回答前必须自检：本轮交付的所有修改是否已 100% 同步在 `gemini` 任务看板中。
