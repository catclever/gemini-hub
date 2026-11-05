---
id: fix_jsonl_loading_regex_backtracking_hang_023
title: Fix JSONL loading hang from unanchored boilerplate regex backtracking
status: completed
priority: high
tags:
- bugfix
- dataset
- performance
session: f89929c4-1b39-4cf5-b9cd-979e32cfc68f
---

# Fix JSONL loading hang from unanchored boilerplate regex backtracking

## 变更概述
Fix catastrophic O(L^2) regex backtracking in _REORDERED_BOILERPLATE_RE and redundant boilerplate cleaning / bigram extraction in dialogue_dataset.py and build_omni_knowledge_corpus.py that caused JSONL loading to hang on long texts. Add fast O(1) keyword guards, sentence-start regex anchoring, and trimmed-context caching.

## 验证结论
- [x] 核心逻辑已实现并通过验证
