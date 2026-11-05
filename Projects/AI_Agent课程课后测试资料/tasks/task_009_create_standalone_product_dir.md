---
title: Create standalone product directory and isolate course/design materials
status: completed
priority: high
tags:
- package
- refactor
- product_dir
id: task_009_create_standalone_product_dir
---
## Description
1. Create standalone product directory `procurement_agent/`.
2. Move all runtime, source, test, eval, skills, contracts, policies, config, and data files into `procurement_agent/`.
3. Keep course exam docs (`实操题.docx`, `AI_Agent课程最终考试试卷.docx`, `实操题材料/`, `实操题材料.zip`), architecture plans (`架构设计与实现计划.md`), and handoff scripts outside in the root.
4. Set up `.venv` inside `procurement_agent/` and verify all tests pass.
