---
title: Ignore real environment configuration files in git
status: completed
priority: high
tags:
- git
- security
- gitignore
- env
id: task_010_gitignore_real_env_configs
---
## Description
1. Update `.gitignore` to explicitly ignore real environment/gateway configuration files:
   - `config/model_config.json`
   - `model_config.json`
   - `.env`
   - `*.env`
2. Ensure `config/model_config.example.json` remains tracked in git as a template.
3. Untrack `config/model_config.json` from git index if currently tracked.
