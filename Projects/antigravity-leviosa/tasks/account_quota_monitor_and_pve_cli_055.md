---
id: account_quota_monitor_and_pve_cli_055
title: 新增多账号 Gemini/Claude 分组额度监控面板与 PVE agy-account quota 命令
status: in_review
priority: high
tags:
- quota
- account-switcher
- pve
session: 6647124a-b312-40df-9900-1be74adcf62a
---

# 新增多账号 Gemini/Claude 分组额度监控面板与 PVE agy-account quota 命令

## 任务目标与背景
1. 后端 `worker/account_manager.js` 新增账号配额拉取能力（调用 `daily-cloudcode-pa.googleapis.com/v1internal:retrieveUserQuotaSummary` 与 `v1internal:retrieveUserQuota`），解析 Gemini 组与 Claude 组的周额度（weekly）及 5 小时额度（5h）与重置时间，缓存至 `~/.gemini/.accounts/<email>.json` 的 `quota` 字段，并提供 `action=refresh_quota`（支持单账号或全部账号刷新）及在 `action=list` 中返回缓存配额。
2. 前端 `web/account_login_inject.js` 账号选择面板：
   - 每个账号卡片简洁展示 **Gemini** 与 **Claude** 两个分组的剩余额度百分比（取周额度/主额度，无需等级徽章、具体模型名称或重置时间）。
   - 打开面板时先展示缓存配额，后台静默调用 `action=refresh_quota` 异步更新 UI，并在面板右上角增加刷新配额小图标按钮。
3. PVE 端 `/usr/local/bin/agy-account` 新增 `quota` 子命令：
   - 并发/逐个读取 PVE 优先账号目录（`/root/.gemini/antigravity-cli/accounts/` 与 `/root/.gemini/.accounts/`）中的账号，刷新并打印详细配额表（包含 Gemini 剩余比例与重置时间、Claude 周额度剩余比例与重置时间、Claude 5h 额度剩余比例与重置时间）。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
