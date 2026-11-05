---
name: stop-pve-web
description: 停止 PVE 上的 PhotoSync 监控服务
---

# /stop-pve-web

当你收到此指令时，请直接执行以下命令连接到 PVE 服务器 (PhotoFactory) 并停止监控服务：

```bash
ssh PhotoFactory "pkill -f 'ruby web/app.rb'"
```
