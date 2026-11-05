---
date: 2026-11-02
status: tentative (user confirmed 3 decisions on 2026-11-02; parallel run with Jules before cleanup)
---

# Descartes + EnginEdge 看门狗：替代 Jules 的落地设计

## 用户已确认的决策
1. **交付方式**：默认停在独立分支 `descartes/<Task_ID>`，由主 Agent 验收后合并；仅当传 `--auto-merge`（夜间模式）才自动 squash 合并回原分支。
2. **运行位置**：先只支持 PVE（`/root/Projects/<project>`）。Mac 本地运行以后再说。（PVE 上跑 `enginedge` 不触碰 Antigravity Project ID 路由，见 `kb/pve_cross_env_sync_issue.md`。）
3. **技能组织**：新建独立技能 `descartes-dispatch`；**暂不修改** `pve-dispatch` / `night-shift` / `jules_watchdog.sh`，与 Jules 并行运行一段时间后再统一清理。

## 交付物
| 交付物 | 路径 |
| :--- | :--- |
| 看门狗脚本 | `~/.gemini/config/scripts/descartes_watchdog.sh` |
| 技能 | `~/.gemini/config/plugins/dev-team/skills/descartes-dispatch/SKILL.md` |

## 与现有看门狗共用的契约（必须保持）
- 参数：`-t <Task_ID>` `-d <Project_Dir>` `-p <Prompt>`。
- 完成信号文件：`/tmp/<Task_ID>.signal`，内容以 `IN_PROGRESS` / `DONE` / `FAILED` 开头（night-shift 循环用 `grep -c DONE` 判断）。
- 日志：`/tmp/descartes_<Task_ID>.log`。
- 脚本运行在 PVE 上，由 Mac 通过 `ssh Antigravity 'bash -s' <<'EOF' ... EOF` 后台触发。

## 脚本流程（descartes_watchdog.sh）
参数：`-t -d -p`，可选 `-b <base_branch>`（默认项目目录当前分支）、`--auto-merge`、`--profile <llm_profile>`、`--hub-url <url>`、`--verify "<cmd>"`、`--timeout <秒，默认 3600>`、`--keep-worktree`。环境变量 `ENGINEDGE_BIN` 可覆盖二进制路径（便于用桩脚本测试）。

1. 参数校验；清理旧 signal；写 `IN_PROGRESS`；`source ~/.config/descartes/env`（若存在，提供 `HUB_AUTH_TOKEN` / `DESCARTES_WS_URL`）。
2. 前置检查：`enginedge`（`$ENGINEDGE_BIN` 或 PATH 或 `~/.cargo/bin`）存在；`-d` 是 git 仓库；分支 `descartes/<Task_ID>` 不存在。任何失败写 `FAILED: <CODE>`。
3. **不依赖 GitHub**：不 push、不 pull。若项目主工作区有未提交改动，在日志里警告“worktree 只包含已提交内容，未提交改动对 Agent 不可见”，但不中止。
4. 创建 worktree：`git worktree add -b descartes/<Task_ID> /tmp/descartes_worktrees/<project>/<Task_ID> <base>`（放在 `/tmp`，避免污染被 Mutagen 同步的项目目录）。
5. `cd` 进 worktree（它就是 EnginEdge 的 `$PWD` 安全围栏），执行 `enginedge run --task "$PROMPT" [--profile ..]`（若有 `timeout`/`gtimeout` 则包裹），stdout/stderr 均 tee 到日志。退出码非 0 → `FAILED: ENGINEDGE_EXIT_<code>`，**保留 worktree** 以便排查。
6. 独立验证：若传 `--verify`，在 worktree 内运行；失败 → `FAILED: VERIFY_FAILED`，保留 worktree 和分支。（不能只信 Agent 自述“完成”。）
7. 无改动 → `DONE: NO_CHANGES`，清理 worktree 与分支。
8. 有改动：`git add -A && git commit -m "feat(descartes): <Task_ID>"`，清理 worktree（保留分支）。
9. 默认：`DONE: BRANCH_READY descartes/<Task_ID> (<commit数>, <diffstat 摘要>)`。
10. `--auto-merge`：仅当项目主工作区干净且位于 base 分支时，`git merge --squash` + commit，删除 `descartes/<Task_ID>` 分支，写 `DONE: MERGED <task> <sha>`；主工作区不干净或不在 base 分支 → 不合并，写 `DONE: BRANCH_READY ... (auto-merge skipped: <原因>)`；合并冲突 → `git merge --abort`/`reset --hard`（仅回滚本次合并）并写 `FAILED: MERGE_CONFLICT descartes/<Task_ID>`，保留分支。
11. `trap` 保证意外退出也会写 `FAILED: UNEXPECTED_EXIT`。

## 失败码
`BAD_ARGS` `ENGINEDGE_NOT_FOUND` `NOT_A_GIT_REPO` `BRANCH_EXISTS` `WORKTREE_FAILED` `ENGINEDGE_EXIT_<n>` `TIMEOUT` `VERIFY_FAILED` `COMMIT_FAILED` `MERGE_CONFLICT` `UNEXPECTED_EXIT`

## 技能 descartes-dispatch 必须覆盖
- 何时使用：与 Jules / `pve_watchdog.sh` agy / 本地 dev 子代理的选择对照表（并行期内 Jules 仍可用）。
- PVE 前置条件：`enginedge` 已安装到 PVE、`~/.config/descartes/env`、项目位于 `/root/Projects/<project>` 且是 git 仓库、Mutagen 同步。
- 触发命令（ssh heredoc + nohup 后台）、参数说明、signal 契约、失败码与处置、日志查看、验收流程（`git diff <base>...descartes/<Task_ID>` → 跑测试 → 合并 → 清理）。
- night-shift 串行循环示例（带 `--auto-merge`，失败即停）。
- **任务粒度准则**：云端 ReAct 单次最多 30 轮；模型为 deepseek-v4.1-flash（弱于 Jules 的 Gemini 3.1 Pro）。因此每个任务限定单一模块、列出相关文件、给出验收命令和范围外说明，禁止跨仓库、禁止一次性大重构。
- 能力边界：本地工具仅 `list_files / read_file / grep_search / write_file / get_outline / read_symbol / replace_symbol / run_verification`；`run_verification` 白名单为 `cargo`、`npm|pnpm|yarn|bun`、`pytest`、`python -m`、`bundle exec`、`go test|vet`、`make test|check`，且禁止 `& | ; > < \` $` 与换行；敏感文件（`.env*`、`*.pem`、`*.key`、`id_rsa*`、`.ssh`、`.aws`）不可读写；无 git 与任意 shell 能力；无人工计划审批环节。
- Hub 是共享实例：并行派发需限流，夜间串行。
