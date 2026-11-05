---
title: 重构上传管线的底层调用，实现实时细颗粒度进度上报
status: backlog
priority: high
tags:
- backend
- refactor
- monitor
id: refactor_upload_progress
---
# 任务背景
目前所有的底层命令调用（包括针对微云的 `rclone copy` 以及针对天翼的 `zip` 压缩）使用的都是 `Open3.capture3`。
这是一个阻塞式的系统调用，在处理几千张照片的批量上传（耗时数小时）或大体积压缩时，Ruby 进程会被完全阻塞，只能在数据库中记录静态文案（如 `批量上传中... (共 3394 个文件)`）。
这导致前端 Web 控制台无法展示“正在上传具体哪张照片”、“当前进度比例是多少”。

# 改造方案
将 `rules/upload_rules.rb` 中的阻塞调用替换为**输出流劫持（流式读取）**。

1. **改造 `rclone` (例如 Weiyun raw 散文件上传)**：
   - 移除 `Open3.capture3(*rclone_cmd_args)`
   - 给 `rclone` 加上 `-v`（verbose）参数。
   - 使用 `Open3.popen3` 启动进程，并实时读取 `stderr` 输出流。
   - 捕获类似 `INFO  : xxx.jpg: Copied (new)` 或 `Unchanged skipping` 的日志，提取当前文件名。
   - 在循环中高频更新数据库（`SystemTaskModel.update`）：`上传中: {文件名} (已完成 {当前计数}/{总数})`。

2. **改造 `zip` (例如 天翼/115 的压缩任务)**：
   - 将 `zip_cmd_args` 的调用从 `capture3` 改为 `popen3`。
   - 劫持 `zip` 的标准输出（如 `adding: filename (stored 0%)`）。
   - 实时写入数据库进度：`正在压缩打包: XXX.zip (已压缩 {N} / {总文件数})`。

# 验收标准
- 微云的大批量上传不再长时间卡在“批量上传中”，能在 Web 面板上看到极速跳动的具体文件名和数字比例。
- 压缩包任务在打包阶段也能清晰看到压缩进度。
- 不影响原本的断点续传逻辑和 `LocationModel` 落库逻辑。
