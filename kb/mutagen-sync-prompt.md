# 跨端同步开启指令 (Mutagen Sync Prompt)

当你被要求为新项目“开启同步”或“建立 Mutagen 隧道”时，请**务必**使用以下带有完整忽略清单（Ignore Flags）的模板。这能防止跨端同步把海量的依赖包、缓存和编译产物传到 PVE，导致网络堵塞或两端环境冲突。

### 标准创建命令模板

```bash
mutagen sync create \
  --name="<填写项目简称>" \
  --ignore-vcs -i ".DS_Store" \
  -i ".venv" -i "venv" -i "__pycache__" -i "*.pyc" -i ".pytest_cache" \
  -i "node_modules" -i "dist" -i "build" -i "out" -i ".next" -i ".nuxt" \
  -i "vendor" -i "target" -i ".gradle" \
  -i ".idea" -i ".vscode" \
  -i "*.log" -i "tmp/" -i "temp/" -i "coverage/" \
  "<填写Mac本地绝对路径>" \
  "Antigravity:<填写PVE远程相对路径>"
```

### 使用准则
1. **命名规范**：`--name` 请使用简短的英文连字符格式（如 `ai-agent`）。
2. **语言覆盖**：上述忽略列表已涵盖 Python(`.venv`/`__pycache__`)、Node.js(`node_modules`/`dist`)、Go/PHP(`vendor`)、Java/Rust(`target`) 以及常规 IDE 和系统缓存。
3. **环境隔离**：测试环境或运行环境生成的临时数据（如 `tmp`、`*.log`）绝不需要在 Mac 和 PVE 之间来回搬运，必须被 Mutagen 忽略。
