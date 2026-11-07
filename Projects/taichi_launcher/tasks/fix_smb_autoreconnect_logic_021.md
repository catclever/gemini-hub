---
id: fix_smb_autoreconnect_logic_021
title: 修复 SMB 挂载与自动重连逻辑缺陷
status: completed
priority: high
tags:
- smb
- disk_monitor
- bugfix
session: c6bce0a6-6556-4fa7-b40e-1af53e0bfc56
---

# 修复 SMB 挂载与自动重连逻辑缺陷

## 任务目标与背景
修复 DiskMonitorManager 中因休眠/意外断开导致 isActive 自动重连被永久关闭、TCP 探活超时过短 (0.5s) 以及开关切换未触发即时连接的逻辑缺陷。

## 实施要点
<!-- 涉及的核心模块、关键逻辑或接口定义 -->

## 交付验收清单
- [ ] 核心实现步骤 1
