# 🎮 Game Development & Graphics Programming Skill Set

A modular suite of specialized agent guidelines for Game Development, Computer Graphics, Engine Loops, Procedural Audio Synthesis, and Physics Simulation.

---

## 📂 Directory Structure

```text
gamedev-workflow/
├── SKILL.md                          # Root Router & Game Dev Principles
├── project-profile/
│   └── GAME_PROJECT_PROFILE.md       # Game Engine Stack Profile (Pygame-ce, F12 HUD, Crash Logger)
├── Implementation/
│   ├── GAME_LOOP_ARCHITECTURE.md     # Game loop passes, delta time (dt), FSM state separation
│   ├── GRAPHICS_AND_PARTICLES.md     # Alpha blending, particle pool explosion engines, color interpolation
│   ├── AUDIO_SYNTHESIS.md            # Procedural PCM audio generation, sound sweeps, mute channels
│   └── PHYSICS_AND_COLLISION.md      # AABB collision bounds, invincibility timers, F12 debug overlay
└── README.md                         # Skill Set documentation
```

---

## 💡 What Problems Does This Skill Set Solve?

1. **Stops Stutter & Performance Drops**: Teaches the agent to use delta-time calculations (`dt`) and particle recycling pools to prevent garbage collection stutters.
2. **Eliminates Messy Code**: Replaces giant nested `if/else` state logic with Finite State Machines (FSM).
3. **Asset-Free Audio & Visuals**: Provides algorithms for generating procedural 8-bit sound sweeps and particle explosion visual effects in code.
4. **Resilient Crash Logging**: Ensures games don't abruptly close without rendering an in-game graphical crash screen and writing to `crash_log.txt`.
