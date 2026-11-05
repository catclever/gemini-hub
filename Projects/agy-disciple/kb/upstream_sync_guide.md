---
description: 'SOP and Meta-Prompt for synchronizing local dev-team updates to the agy-disciple open-source repository with diff auditing and sanitization.'
---

# Upstream Sync SOP: Local dev-team to agy-disciple

本知识库文档定义了如何将本地私有插件 `dev-team`（上游源）的迭代改动，规范化、差异化并脱敏同步至开源仓库 `agy-disciple`（下游公开版）的标准作业程序。

---

## 🧭 核心路径定位

* **私有上游源 (Upstream Private)**: `~/.gemini/config/plugins/dev-team/`
* **开源发布端 (Downstream Public)**: `/Users/kael/Projects/agy-disciple/`
* **元数据集中目录 (Metadata)**: `~/.gemini/Projects/agy-disciple/`

---

## 🔄 四步同步工作流 (The 4-Step Sync Protocol)

### 步骤一：差异比对审计 (Diff Comparison First)

在进行任何复制或修改前，**必须先执行结构化差异比对**，定位具体有哪些文件新增、修改或删除：

```bash
# 1. 快速概览文件差异树
diff -rq --exclude=".git" --exclude="__pycache__" ~/.gemini/config/plugins/dev-team/ /Users/kael/Projects/agy-disciple/

# 2. 对特定修改的文件进行具体代码比对
diff -u ~/.gemini/config/plugins/dev-team/skills/dev-manager/SKILL.md /Users/kael/Projects/agy-disciple/skills/dev-manager/SKILL.server.md
```

**分类归纳变更**：
* [ ] 新增技能 (New Skills)
* [ ] Agent 提示词优化 (Agent YAMLs)
* [ ] 看门狗或自动化脚本改进 (Watchdogs/Scripts)
* [ ] 现有技能逻辑调整 (Skill Logic Tweaks)

---

### 步骤二：脱敏与架构适配准则 (Sanitization & Adaptation Filter)

将上游改动迁移到 `agy-disciple` 时，**严禁生搬硬套**，必须通过以下 4 道适配过滤器：

1. **绝对路径动态化**：
   * 严禁出现 `/Users/kael` 等私人绝对路径。
   * 替换为 `~/.gemini/...`、`$HOME` 或工作区相对路径。
2. **硬件/主机别名参数化**：
   * 严禁硬编码 SSH 别名 `Antigravity`，统一替换为 `<REMOTE_HOST>` 或环境读取 `${AGY_REMOTE_HOST:-remote-host}`。
   * 严禁硬编码远端路径 `/root/Projects`，替换为 `<remote_dir>` 或 `${AGY_REMOTE_BASE:-~/Projects}`。
3. **双版本文件对齐 (Dual-Variant Preservation)**：
   * 若修改了涉及双模的技能（`dev-manager`, `project-manager`, `test-environment`, `night-shift`, `extract-knowledge`）：
   * 必须明确该改动属于 **Local/In-Repo** 还是 **Server/Centralized**；
   * 针对性更新对应的变体文件（如 `SKILL.server.md`），若当前生效的是该模式，同步更新 `SKILL.md`。
4. **人设与私有工具脱敏**：
   * 移除“Princess/公主”等个人私有称谓，统一使用通用的中立工程术语。
   * 移除个人专用的私有本地工具名称（如 Hammerspoon）。

---

### 步骤三：验证与健康检查 (Doctor & Integrity Check)

同步完成后，运行内置工具确保插件完整性：

```bash
# 1. 验证双模映射是否完好
python configure.py --status

# 2. 运行环境诊断确保依赖声明准确
python configure.py --doctor

# 3. 审查工作区改动，确保没有意外带入敏感信息
git diff
```

---

### 步骤四：原子提交并推送

```bash
git add .
git commit -m "sync(upstream): synchronize updates from dev-team with open-source adaptations"
git push origin main
```

---

## 📋 随时可用的 Agent Meta-Prompt (指令模版)

> **使用方式**：以后在 `agy-disciple` 对话中，若想让 AI 自动同步，直接将以下提示词发给 Agent 即可：

```markdown
请帮我把本地私有上游 `~/.gemini/config/plugins/dev-team/` 的最新改动同步到当前的 `agy-disciple` 开源仓库中。

【执行准则】
1. 先比较差异：先用 diff 工具全面审查上游与当前仓库的区别，列出差异清单供我确认，不要盲目覆盖。
2. 架构与脱敏适配：
   - 彻底移除所有 `/Users/kael` 绝对路径与私有称谓。
   - 保持本项目特有的双模结构（Local vs Server，In-Repo vs Centralized），将远端特性的改动正确分流到对应的 `.server.md` 或 `.centralized.md`。
   - 保留公共看门狗脚本 `scripts/watchdogs/` 中的通用参数结构。
3. 检查与验证：同步完成后运行 `python configure.py --status` 和 `python configure.py --doctor` 验证完整性。
```
