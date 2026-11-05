---
title: "Implement Lazy Management for Cyber Apps"
status: completed
priority: high
tags: [backend, cyber, alfred]
---

# Task: Implement Lazy Management for Cyber Apps

## Description
Replace the current heavy `discoverRunningInjectedApps` (system-wide `ps grep`) with a lightweight Lazy Management (按需刷新) mechanism. 
When a Cyber app is launched, persist its PID and connection details. When Alfred queries `/api/launcher/filter`, perform a lightweight OS ping (`kill -0`) on persisted PIDs. If dead, remove them. If alive, use them.

## Requirements
1. **Model Update**: Update `MonitoredApp` struct in `Models.swift` to include `pid: pid_t?` and `port: Int?`. Make it `Codable` if not already.
2. **Persistence**: Add a method in `TaiChiSettings` to save and load `activeInjectedApps` to/from `UserDefaults` or a local JSON file whenever it changes.
3. **Launch Update**: In `ServerManager.swift` (`handleLauncherAction`), when launching an app via CDP, record its `pid` and `targetPort` into the `MonitoredApp` object before appending to `activeInjectedApps`.
4. **On-Demand Refresh**: 
   - Remove or deprecate the heavy `discoverRunningInjectedApps()` call on startup.
   - Create a `refreshCyberAppsStatus()` function in `ServerManager.swift`.
   - This function will iterate through `activeInjectedApps`. For each app, check if its `pid` is still alive (e.g., using `kill(pid, 0) == 0`).
   - If dead, remove it from `activeInjectedApps`.
   - If alive but needs reinjecting (e.g., Taichi just restarted), fire the reinjection worker.
5. **API Integration**: Call `refreshCyberAppsStatus()` at the beginning of `handleLauncherFilter` (which is triggered by Alfred), so the state is accurately refreshed right before the user sees it.
