# Iron Rules for Taichi Project

[Global]
- Always run projects within virtual environments where applicable.
- Do not overwrite original files directly during development; use _task_name suffix for drafts.

[Ops Agent]
- You are allowed to package the project using build tools.
- **Packaging Command**: To package/build the project, execute `bash build_app.sh`.
- CRITICAL RULE (Packaging): DO NOT automatically kill existing application processes (e.g., using `killall`) and DO NOT automatically restart processes after packaging or building (e.g., using `open`). The user will handle restarting the application manually.
