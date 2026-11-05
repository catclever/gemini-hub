# Post-Mortem: Three.js 3D Billboard Shadow Mapping & Manual 1D Shader Shear (Deprecated)

- **Date**: 2026-10-23
- **Status**: Deprecated / Replaced by Godot 4 2.5D Architecture

## 1. Context & What Was Tried
We attempted to build a 2.5D dynamic lighting and shadow system for 2D AI-generated botanical illustrations (`layer_red.png`, `layer_green.png`, `layer_blue.png`) inside a web browser using Three.js (`src/light_demo.html`) via two iterations:
1. **Iteration 1 (3D ShadowMap + Pseudo-Normal SDF)**: Placed 2D plant textures onto tilted `THREE.PlaneGeometry` billboards facing an `OrthographicCamera`, generated puff/pillow normal maps via Euclidean Distance Transform (`distance_transform_edt`), and enabled `DirectionalLight.castShadow = true`.
2. **Iteration 2 (Plan A Manual GLSL Ground Wash)**: Disabled 3D shadow maps and wrote custom GLSL vertex/fragment shaders (`washVertexShader`) to skew a horizontal plane on the ground (`pos.x += shadowDirection.x * pos.y * shadowSkew`).

## 2. Why It Failed (Root Causes)
1. **Billboard Shadow Artifact (纸片人投影畸变)**:
   - Casting 3D depth shadows from a 2D quad tilted toward the camera onto a horizontal ground plane produces an affine-distorted trapezoid silhouette when lit from oblique angles, exposing the flat paper-card geometry.
2. **Pseudo-Normal Pillow Effect (伪法线气囊效应)**:
   - Distance-transform normal maps inflate the entire plant silhouette like a single convex balloon without knowing leaf-over-leaf depth ordering, clashing with existing 2D hand-drawn shading and making foliage look like muddy plastic.
3. **Root Disconnection (根部脱节)**:
   - Sliced plant PNGs have varying transparent padding at the bottom (`alpha == 0`) and off-center stems. Using the raw quad bottom-center as pivot caused visible gaps between the floating plant stem and its ground shadow.
4. **1D Shear vs. True 2D Rotation**:
   - Shearing `pos.x` by `pos.y` in a shader without a full 2D rotation matrix (`cos/sin`) ignored `shadowDirection.y` and failed to rotate shadows around the root across 360°.
5. **Lack of Point-Light Shadows & Rear-Plant Occlusion**:
   - Pure Three.js custom shaders required reinventing a complete 2D lighting engine from scratch to support radial point-light shadows (flashlight/lantern) and inter-plant canopy shadow darkening.

## 3. What NOT To Do
- **DO NOT** use 3D polygon shadow mapping (`DirectionalLight.castShadow`) on 2D tilted billboard sprites.
- **DO NOT** use geometric quad bottom-center pivots for 2D botanical sprites without first scanning the image's non-transparent bounding box (`get_used_rect()`) to find the exact stem root pixel.
- **DO NOT** use 1D horizontal vertex shearing (`pos.x += k * pos.y`) to simulate directional shadows on an isometric plane; use a true 2D pivot rotation inside an isometric squash transform (`scale = Vector2(1.0, 0.55)`).
