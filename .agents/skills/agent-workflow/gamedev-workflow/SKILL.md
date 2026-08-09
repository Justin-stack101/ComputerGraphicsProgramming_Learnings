---
name: gamedev-workflow
description: "Core operating workflow for Game Development & Computer Graphics programming (Pygame-ce, WebGL, OpenGL, Unity, Godot, Pygame). Guides game loop architecture, Finite State Machines (FSM), particle physics pools, procedural audio synthesis, AABB collision systems, and visual performance optimization. Consult this on game engine design, rendering passes, audio cues, or physics tasks."
---

# 🎮 Game Development & Graphics Programming Skill Set

This skill set defines the specialized workflows and architectural patterns required for high-performance Game Development and Computer Graphics programming.

---

## 🏛️ Core Principles of Game Development

1. **Frame-Rate Independence**:
   - Always decouple game logic calculations from render rates using delta-time (`dt = clock.tick(FPS) / 1000.0`).
   - Movement speed must be expressed in units-per-second (`speed * dt`) rather than units-per-frame.

2. **Object Pooling & Memory Discipline**:
   - Avoid instantiating and destroying thousands of dynamic objects (particles, bullets, debris) per second in Python/C#/C++.
   - Pre-allocate particle pools and recycle inactive particles to prevent garbage collection stutter.

3. **Finite State Machine (FSM)**:
   - Separate game operational modes (`START_MENU`, `PLAYING`, `PAUSED`, `SETTINGS`, `GAME_OVER`) into dedicated state handlers instead of complex, nested boolean flags.

4. **Procedural Audio & Synthesized Sound**:
   - Synthesize PCM audio buffers or use pre-allocated sound channel pools for immediate audio feedback.

5. **Graceful Crash Handling in Games**:
   - Intercept unhandled runtime exceptions with an in-game graphical error screen overlay that logs trace data to `crash_log.txt` before exiting.

---

## 🗺️ Skill Routing & Specialized Guides

```text
Game Dev Task Request
       │
       ▼
Game Loop Architecture ───► Implementation/GAME_LOOP_ARCHITECTURE.md
Graphics & Particles   ───► Implementation/GRAPHICS_AND_PARTICLES.md
Audio & Sound Synth    ───► Implementation/AUDIO_SYNTHESIS.md
Physics & Collision    ───► Implementation/PHYSICS_AND_COLLISION.md
Project Stack Profile  ───► project-profile/GAME_PROJECT_PROFILE.md
```

### 1. Game Loop & State Architecture
Read **`Implementation/GAME_LOOP_ARCHITECTURE.md`** whenever: structuring the main loop, handling game pause/resume, building state managers (Menu, Playing, GameOver), or optimizing fixed vs. variable time steps.

### 2. Graphics & Particle Rendering
Read **`Implementation/GRAPHICS_AND_PARTICLES.md`** whenever: rendering visual effects, alpha blending, particle explosion systems, surface caching, or custom lighting/shaders.

### 3. Audio & Sound Synthesis
Read **`Implementation/AUDIO_SYNTHESIS.md`** whenever: creating procedural sound effects (sine/square wave sweeps, explosions, thunder strikes), managing BGM channels, or controlling volume controls.

### 4. Physics & Collision Systems
Read **`Implementation/PHYSICS_AND_COLLISION.md`** whenever: implementing AABB bounding box collision checks, invincibility timers, player movement physics, or spatial grid partitioning.

### 5. Game Project Profile
Read **`project-profile/GAME_PROJECT_PROFILE.md`** for concrete facts about the specific game engine, framework (Pygame-ce, WebGL, Godot), keyboard shortcuts, and developer F12 test overlays.
