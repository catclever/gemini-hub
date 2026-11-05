---
title: Botanist Studio 优化与备选植物确认系统
status: completed
priority: medium
tags:
- interaction
- workflow
session: conversation://37b05991-ab00-4528-b3ff-63fbdea2f6fd
id: task_003_studio_optimizations
---
## 任务背景与修正
1. **中文别名支持**: 在入库植物时提供中文别名输入项，保存至 `metadata.json` 的 `display_name` 字段，并在资产画廊与图层检视器中直观展示。
2. **备选植物选中/确认 (重点修正)**: 
   - 之前误放至资产画廊，现已正确定位至【📥 备选审批区 (Candidates)】；
   - 用户单击备选图片/卡片即可标记为“已确认”，卡片高亮金色边框（`#f2cc60`）并附带 `★ 已确认` 金星徽章；再次单击取消确认；
   - 点击卡片上的“入库”或“删除”按钮已做事件隔离，不会误触选中；
   - 备选区顶部实时显示已选中计数（`已确认: N`）；
   - 后台自动持久化保存已确认备选植物清单至 `tools/confirmed_candidates.json`（并同步兼容 `tools/confirmed_plants.json`），供后续批处理与切片打包自动化脚本直接调用；
   - 当草稿被入库或删除时，自动从确认清单中清理。
3. **图层检视器交互精简**: 去除冗余厚重的“🔍 查看图层”按钮，直接将“🧩 N 个独立图层 ↗”作为轻量级标牌按钮，点击直达图层拆解面板。

## 变更文件
- `tools/botanist_studio.py`:
  - 修正植物确认交互至左侧备选区，右侧资产区恢复为常规画廊；
  - 提供 `GET /api/confirmed_candidates` 与 `POST /api/toggle_confirm_candidate`；
  - 在 `delete_candidate` 与 `process` 成功后自动同步清理确认池。
- `tools/confirmed_candidates.json` & `tools/confirmed_plants.json`:
  - 存储已确认选中的备选植物清单。
