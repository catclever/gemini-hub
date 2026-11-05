---
id: bench_failure_logging_and_diagnostics_012
title: Benchmark 失败排障日志与详细诊断报告生成 (src/bench.rs)
status: completed
priority: medium
tags:
- rust
- benchmark
- logging
- eval
- diagnostics
session: conversation://8bc0e420-6a50-41a3-95a4-21f573d20bb0
---

# Benchmark 失败排障日志与详细诊断报告生成 (src/bench.rs)

## 任务目标与背景
为自动化 Benchmark 测评模块 (src/bench.rs) 补齐失败排障诊断体系：1. 自动生成单题完整交互轨迹日志 (bench_logs/<task_id>.log)，记录思考流、工具调用与报错；2. 在 Markdown 报告自动追加折叠式失败诊断区 (Failure Diagnostics)，直观呈现编译器/单测报错堆栈与退出码；3. CLI 新增 --log-dir 参数配置。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

### 交付与验证报告
1. **单题完整交互轨迹落盘 (`bench_logs/<task_id>.log`)**：
   - 记录 Task 基础信息、Prompt、模型各轮思考过程 (`[THOUGHT #n]`)、工具调用入参 (`[TOOL_CALL #n]`) 与结果 (`[TOOL_RESULT]`)、异常 (`[ERROR]`) 及最终验证命令的 STDOUT / STDERR；
   - 随 `--log-dir` 参数可自定义持久化路径。
2. **Markdown 报告新增折叠式失败排障区 (`## 🔍 Failure Diagnostics`)**：
   - 针对所有失败任务，渲染 HTML `<details>` 折叠卡片；
   - 一键展开直观查看编译器/单测框架的失败堆栈（代码行号、断言失败详情、Panic 堆栈等），附带对应轨迹日志路径链接。
3. **测试与质量验证**：
   - PVE 执行 `cargo test`：29 项单元测试全部通过（100% Pass）；
   - PVE 执行 `cargo clippy -- -D warnings`：零警告通过；
   - PVE 运行真实命令冒烟：成功生成包含详细失败堆栈与单题 trace 文件的完整报告；
   - 提交推送至 GitHub `catclever/EnginEdge.git` (`810c011`)。
