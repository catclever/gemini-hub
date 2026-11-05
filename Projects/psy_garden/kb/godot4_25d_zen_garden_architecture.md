# Godot 4 2.5D Zen Garden Architecture & Lighting Specification

- **Last Updated**: 2026-10-23
- **Engine**: Godot 4.3 (`gl_compatibility` renderer for universal WebAssembly/WebGL2 + macOS Metal support)
- **Project Root**: `godot/` (with relative symlink `godot/assets/plants -> ../../src/assets/plants` so `Botanist Studio` assets are 100% shared without duplication)
- **Web Export Path**: `src/godot_web/` (or served at `http://172.16.51.19:18088/` with single-threaded Web export `variant/thread_support = false` so no COOP/COEP HTTPS headers are required on LAN IPs)

## 1. Core Technical Solutions for the 4 Historical Pain Points

### 1.1 Exact Root Pixel Calibration (消除植物与影子根部脱节)
- Sliced plant PNGs (`layer_red.png`, `layer_green.png`, `layer_blue.png`) often have bottom transparent padding (`alpha == 0`) or slightly off-center stems.
- **Mandatory Algorithm**:
  - Upon loading a plant's layers, combine or inspect the alpha channel of `layer_green.png` and `layer_red.png` via `Texture2D.get_image()`.
  - Find the lowest non-transparent row `bottom_y = used_rect.position.y + used_rect.size.y - 1`.
  - Scan pixels in the bottom 8 rows (`[bottom_y - 7, bottom_y]`) where `alpha > 0.15` and compute the average horizontal coordinate `root_x`.
  - Define `root_anchor = Vector2(root_x, bottom_y)`.
  - Every `Sprite2D` (both upright plant layers and ground shadow sprites) sets `centered = false` and `offset = -root_anchor`.
  - This guarantees that local `(0, 0)` of the `Plant` node is **mathematically locked to the exact lowest visible stem pixel**, completely eliminating any gap between the plant and its shadows at any angle.

### 1.2 True 360° Isometric Shadow Rotation (真实 2D 旋转与等距透视接地)
- Do NOT use 1D vertex shearing.
- Use a 3-tier `Node2D` transform hierarchy anchored at `(0, 0)` (with `z_index` placed on the ground layer beneath all plant trunks):
  ```text
  GroundShadow Plane (Node2D, position = (0, 0), scale = Vector2(1.0, 0.55))  <-- Isometric ground foreshortening
  ├── ContactShadow (Sprite2D: soft radial AO ellipse at (0, 0))
  ├── SunShadowPivot (Node2D, position = (0, 0), rotation = sun_shadow_angle, scale = Vector2(1.0, sun_shadow_len))
  │   └── SunShadowSprite (Sprite2D, offset = -root_anchor, Shader: ink-wash vertical fade + weather shadow tint)
  └── LanternShadowPivot (Node2D, position = (0, 0), rotation = lantern_shadow_angle, scale = Vector2(1.0, lantern_shadow_len))
      └── LanternShadowSprite (Sprite2D, offset = -root_anchor, Shader: ink-wash vertical fade + dynamic opacity)
  ```
- Because `SunShadowPivot` and `LanternShadowPivot` rotate inside `GroundShadowPlane (scale = Vector2(1.0, 0.55))`, rotating `rotation` from `0` to `TAU` ($0^\circ \sim 360^\circ$) smoothly orbits the shadow around the root in a true isometric ellipse on the ground plane.
- Include an interactive **Sun Azimuth Angle Slider ($0^\circ \sim 360^\circ$)** in the HUD so the user can both select weather presets AND freely drag the sun direction around the compass.

### 1.3 Dynamic Flashlight / Mouse Lantern & Incense Point-Light Shadows (手电筒与燃香动态放射甩影)
- **Mouse Lantern (`PointLight2D` + `LanternShadowPivot`)**:
  - Follows cursor in world space.
  - For every plant within `lantern_radius` (e.g., `420px`):
    - Compute ground-space vector `vec = (plant.global_position - mouse_world_pos) / Vector2(1.0, 0.55)`.
    - Set `LanternShadowPivot.rotation = vec.angle() + PI / 2.0` so the shadow projects radially outward away from the flashlight cursor.
    - Set `LanternShadowPivot.scale.y = lerp(0.55, 1.85, clamp(1.0 - dist / lantern_radius, 0.0, 1.0))` and modulate shadow alpha by proximity and lantern intensity.
- **Center Incense Burner (`PointLight2D`)**:
  - Placed at garden center `(0, 0)` with warm ember flicker (`#ff6611`) and `GPUParticles2D` rising smoke wisps.

### 1.5 Synthesized Single-Vector Shadow (消除多光源双影分叉与视觉冲突)
- **Problem**: When both the weather directional sunlight and the localized mouse lantern/incense burner cast distinct shadows, each plant casts two or more separate shadow tails branching in different directions, causing visual clutter in a 2.5D zen watercolor aesthetic.
- **Solution (Vector Synthesis)**:
  - Synthesize all active light source forces in isometric ground space into a single cohesive shadow vector:
    `V_combined = V_sun + V_lantern + V_incense`
  - Compute unified pivot rotation: `rotation = V_combined.angle() + PI / 2.0`.
  - Compute unified shadow length: `scale.y = clamp(V_combined.length(), 0.15, 2.2)`.
  - Modulate primary shadow alpha and conceal secondary shadow pivots (`visible = false`).
  - Result: Plants smoothly sweep and rotate their single shadow toward the dominant light source as the lantern approaches, maintaining a calm, clean, single-shadow composition without split forks.
  - The inter-plant canopy occlusion corridor dynamically tracks this synthesized vector in real time.

### 1.4 Inter-Plant Canopy Shadow Darkening (前树影子让后方植物变暗)
- Combine **Godot Native `Light2D` + `LightOccluder2D`** with **Canopy Shadow Reception Shader**:
  1. Each plant has a `LightOccluder2D` at its trunk/base so `DirectionalLight2D` and `PointLight2D` cast native 2D soft shadows (`SHADOW_FILTER_PCF13`).
  2. In `Garden.gd`, each frame (or on light/mouse update), evaluate directional shadow overlap between plants:
     - For each caster plant `A` and receiver plant `B`:
     - Project `B.global_position - A.global_position` onto the active shadow direction vector (both Sun shadow vector and Mouse Lantern shadow vector).
     - If `B` lies within `A`'s shadow corridor (`0 < along_dist < shadow_world_len` and `perp_dist < shadow_half_width`), compute how high up `B`'s body the shadow of `A` reaches: `cover_ratio = clamp((1.0 - along_dist / shadow_world_len) * (A.height / B.height), 0.0, 1.0)`.
     - Pass `shadow_cover_height` and `shadow_cover_strength` (and horizontal overlap offset) to `B`'s `Plant.gdshader`.
     - In `Plant.gdshader`, pixels below `shadow_cover_height` are smoothly darkened by `45%–65%` into cool deep forest shade and their rim-light is attenuated, producing an unmistakable visual darkening whenever a front plant's shadow sweeps across a rear plant!
