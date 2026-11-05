# Photo Sync - 管线操作文档 (Operations Manual)

本项目基于三层架构设计（规则层、核心层、脚本调度层）。管线的日常运维、监控和手动干预，均通过统一的 CLI 工具与监控面板完成。

## 1. 启动守护进程
管线守护进程负责轮询任务状态和派发 Worker 执行任务。
- **启动命令**: `./start_pipeline.sh`
- **说明**: 守护进程会在后台常驻执行 `bin/daemon.rb`，终端可直接关闭。运行日志保存在工作区根目录的 `scheduler.log`。

## 2. 实时状态监控
想要查看当前有多少任务正在排队、运行或报错，可以使用实时监控画板。
- **监控命令**: `bundle exec ruby bin/monitor.rb`
- **说明**: 该命令会清屏并每 2 秒刷新一次，展示 Pending、Running、Success 和 Error 状态的任务统计，以及最新的失败报错原因。按 `Ctrl+C` 退出。

## 3. 管线 CLI 运维 (bin/cli.rb)
所有对手动任务下发、状态重置，均通过统一入口 `bin/cli.rb` 执​​行。

### 3.1 查看任务状态汇总
```bash
bundle exec ruby bin/cli.rb status
```
一次性打印当前的各状态任务统计数据。

### 3.2 列出所有/特定状态的任务
```bash
# 列出所有任务
bundle exec ruby bin/cli.rb list

# 仅列出正在报错的任务
bundle exec ruby bin/cli.rb list error
```

### 3.3 一键重试失败任务
当任务报错，人工排查并修复原因后，可使用此命令将 `error` 状态重置回 `pending`，由守护进程自动重新拉起。
```bash
# 重置单个任务
bundle exec ruby bin/cli.rb retry "upload:115:/mnt/factory/Ingested/2026.07.09~24 德宏旅居"

# 重置所有错误任务
bundle exec ruby bin/cli.rb retry all
```

### 3.4 手动下发打包/上传任务 (Repack)
替代旧版的直接运行脚本方式，使用 CLI 向数据库注册一个新的上传任务。
```bash
# 基本用法
bundle exec ruby bin/cli.rb submit repack <目标目录> <网盘代号> [--repack=文件夹ID]

# 示例:
bundle exec ruby bin/cli.rb submit repack "/mnt/factory/Ingested/2026.07.09~24 德宏旅居" 115 --repack=11060721
```
任务注册成功后，处于后台的 Daemon 会自动将其取出并调度 `worker_upload.rb` 执行。

### 3.5 清理废弃/历史错误任务
如果确认某些错误任务已经无效（例如目录已被删除，或者属于旧版逻辑残留），可以将其从数据库中永久清理。
```bash
# 删除指定的无效任务
bundle exec ruby bin/cli.rb delete "upload:115:/mnt/factory/Ingested/2026.07.09~24 德宏旅居"

# 一键清空所有 error 状态的历史任务
bundle exec ruby bin/cli.rb delete error
```
