---
id: eval_optimizations_dynamic_lease_and_test_isolation_016
title: 评测套件双重优化：动态进展续约与测试白名单隔离
status: completed
priority: high
tags:
- bench
- optimization
- lease-extension
session: 8bc0e420-6a50-41a3-95a4-21f573d20bb0
---

# 评测套件双重优化：动态进展续约与测试白名单隔离

## 任务目标与背景
实现方案二动态进展续约机制 (Activity Lease Extensions) 与 Python 测试文件白名单精确隔离 (避免草稿文件崩溃)，并进行针对性复测。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1

### 边缘端三项优化全部落地验证完毕
1. **动态进展续约机制 (Dynamic Lease Extensions)**：
   - 剩余时间 < 15s 且 30s 内有产出时，自动续约 +60s（最多 2 次，300s 封顶）。
   - 追踪字段 `lease_extensions` 贯穿 `TaskResult`、日志与报告。
   - 实测实证：`python_scale-generator` 耗时 195.98s 触发 `⏳ +1 (60s)` 续约，成功全绿通关！
2. **测试白名单隔离 (Test Whitelisting Isolation)**：
   - 将 Python 评测命令精确绑定为 `python3 -m unittest discover -s . -p {ex_slug}_test.py`。
   - 实测实证：成功屏蔽草稿文件干扰，`python_scale-generator` 100% 通过。
3. **边缘端 Max Turns 动态传参支持**：
   - `BenchOptions` 与 CLI `Commands::Bench` 增加 `--max-turns` 参数（默认 50 轮）。
   - 在 `init_payload` 中显式携带 `"max_turns": options.max_turns`，为云端 Hub 扩容提供协议支持。
