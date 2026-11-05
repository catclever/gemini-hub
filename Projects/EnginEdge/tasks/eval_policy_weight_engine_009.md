---
id: eval_policy_weight_engine_009
title: 命令安全权重与评测模式控制模块 (src/policy.rs)
status: completed
priority: high
tags:
- rust
- policy
- security
- benchmark
- eval
session: conversation://8bc0e420-6a50-41a3-95a4-21f573d20bb0
---

# 命令安全权重与评测模式控制模块 (src/policy.rs)

## 任务目标与背景
实现基于固定硬规则的 0~100 命令安全权重评估引擎 (src/policy.rs)，区分日常开发 (dev/40) 与评测扩展 (eval/75) 模式；升级 run_verification 支持权重放行与受控 && 串联，get_status 输出当前策略状态，全面增加单元测试覆盖。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

### 交付与验证报告
1. **新建命令安全权重引擎 (`src/policy.rs`)**：
   - 0~100 分级评估体系：Level 1 (0~20 只读/自检)、Level 2 (21~40 开发单测)、Level 3 (41~75 评测扩展)、Level 4 (100 绝对熔断)；
   - 固定硬规则计算：严禁 Shell 元字符（`|`, `;`, `>`, `<`, `` ` ``, `$`）、路径逃逸（`..`）及高危程序（`rm`, `curl` 等）；
   - 支持受控 `&&` 链式组合与测评专属命令（`cmake`, `ctest`, `make`, `mvn`, `gradle`, `go build`, `git restore/checkout --` 单文件回滚）；
   - 支持 `dev` 模式（默认 40 权重）与 `eval` 模式（75 权重）及 `--max-weight` 覆盖。
2. **重构终端验证工具 (`src/tools.rs`)**：
   - 接入 `policy::evaluate_command`，执行受控 `&&` 顺序执行；
   - 动态更新 `run_verification` 工具描述提示当前生效策略；
   - `get_status` 返回当前 policy 遥测信息。
3. **修复与测试验证**：
   - PVE 运行 `cargo test`：25 项单元测试 100% 通过；
   - PVE 运行 `cargo clippy -- -D warnings`：零警告通过；
   - 提交已同步推送至 GitHub `catclever/EnginEdge.git` (`3e0c17b`)。
