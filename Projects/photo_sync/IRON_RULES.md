## [Global]
- 项目架构采用严格的“三层架构”：规则层 (`rules/`)、核心领域层 (`src/`)、脚本调度层 (`bin/`)。不得破坏此分层。
- 所有日常运维命令、任务提交流程，请务必严格参照项目操作手册：`~/.gemini/Projects/photo_sync/kb/operations_manual.md`。

## [Main Agent]
- 当需要管理、查询或干预系统任务时，必须通过 `bin/cli.rb` 或查阅 `kb/operations_manual.md`，不要尝试直接修改 `sqlite3` 数据库内容。
- 系统出现报错时，使用 `bin/cli.rb list error` 获取错误详情。

## [Dev Agent]
- 在修改 Amber 规则或 Worker 脚本前，务必先在本地环境验证，并遵守三层架构的边界。
- 新增独立任务，请在 `bin/cli.rb` 中新增 subcommand 来统一收口，禁止创建散落的 shell 脚本。
