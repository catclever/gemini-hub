---
id: eval_benchmark_runner_and_reporter_011
title: 自动化 Benchmark 测评套件与官方基准对比报告 (src/bench.rs)
status: completed
priority: high
tags:
- rust
- benchmark
- aider
- eval
- deepseek
session: conversation://8bc0e420-6a50-41a3-95a4-21f573d20bb0
---

# 自动化 Benchmark 测评套件与官方基准对比报告 (src/bench.rs)

## 任务目标与背景
实现 EnginEdge 官方编程 Benchmark 自动化测评与判分模块 (src/bench.rs 与 enginedge bench CLI 命令)：包含多语言评测题库加载（内置原生 Polyglot 金标题集与外部 Manifest 加载）、隔离沙箱执行、云端 Bridge 驱动、官方测试套件硬规则判分、遥测统计（耗时、思考轮数、AST工具使用率）以及生成与 DeepSeek-V4.1-Flash 官方基准（57.0% / 71.6%）的对比打分报告。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

### 交付与验证报告
1. **新建自动化 Benchmark 测评模块 (`src/bench.rs`)**：
   - 内置跨语言 Polyglot 金标题库（覆盖 Rust、Go、Python、JavaScript 典型数据结构与算法工程题）；
   - 支持从外部目录或 JSONL Manifest 加载标准题库（如 `Aider-AI/polyglot-benchmark` 或自定义测试集）；
   - 自动化隔离沙箱执行：为每道题创建独立临时沙箱，挂载源码与初始单测，自动初始化 `PolicyMode::Eval`（最大权重 75）；
   - 遥测指标采集：精确记录耗时、思考步数、工具调用总数、AST 工具调用数与文件工具调用数；
   - 官方标准判卷（Grader）：直接执行官方自带单测（`cargo test`, `go test`, `pytest`, `node test.js`），以 Exit Code 严格判定 Pass / Fail；
   - 官方基准对标报告生成器（Reporter）：自动输出 Markdown 与 JSON 双格式报告，计算 Pass@1 通过率并与 DeepSeek-V4.1-Flash 官方公布分数（初始版 57.0% / -1017 最新版 71.6%）计算 Score Delta。
2. **新增 CLI 子命令 `enginedge bench` (`src/main.rs`)**：
   - 提供 `--dataset`, `--langs`, `--limit`, `--output`, `--profile`, `--dry-run`, `--timeout` 等灵活参数。
3. **测试与质量验证**：
   - PVE 运行 `cargo test`：29 项单元测试全部通过（100% Pass）；
   - PVE 运行 `cargo clippy -- -D warnings`：零警告通过；
   - PVE 运行 `cargo run -- bench --dry-run`：完整走通 4 语言沙箱初始化、测试判分与对比报告生成流水线；
   - 提交推送至 GitHub `catclever/EnginEdge.git` (`e5375f7`)。
