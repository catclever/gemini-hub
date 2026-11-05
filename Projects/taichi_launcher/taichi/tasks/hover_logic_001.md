---
title: "Optimize non-playing notch hover logic"
status: active
priority: high
tags: [frontend, interaction, notch]
---
# Granular Requirement
Implement the 2-stage hover logic for the notch in non-playing state:
1. Hovering over the short native notch expands left/right icons (without expanding title).
2. Staying in the center native notch area for 3s (with a cooldown to prevent rapid toggling) expands the control panel.
3. Moving to left/right icons cancels the 3s timer.
4. Leaving the notch entirely restores it to the short native state.
