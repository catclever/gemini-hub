---
name: start-pve-web
description: 启动 PVE 上的 PhotoSync 监控服务
---

# /start-pve-web

当你收到此指令时，请直接执行以下命令连接到 PVE 服务器 (PhotoFactory) 并启动监控服务：

```bash
ssh PhotoFactory "cd ~/photo_sync && export PATH=\"\$HOME/.local/share/gem/ruby/3.3.0/bin:\$PATH\" && nohup bundle exec ruby web/app.rb > web.log 2>&1 < /dev/null &"
```
