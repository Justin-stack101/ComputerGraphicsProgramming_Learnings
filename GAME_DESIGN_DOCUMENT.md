# Game Design Document (GDD) — Star Catcher
**Course**: IT2012 (Game Development/Game Programming) & IT2202 (Computer Graphics Programming)  
**Project Title**: Star Catcher Interactive Engine  
**Author**: Justin Nolasco  
**Version**: 1.0.0  

---

## 1. Executive Summary

- **Genre**: 2D Arcade Action / Microgame
- **Platform**: Desktop (Pygame / Python 3), Web Port Ready
- **Target Audience**: Casual Gamers, Arcade Enthusiasts, Academic Evaluators
- **Core Loop**: Move player square ➔ Avoid moving enemy obstacles ➔ Collect stars for high scores before timer expires.

---

## 2. Story & Character Development (Syllabus Weeks 8–9)

### 2.1 The 3-Act Plot Structure
1. **Act I: The Inciting Incident (Intake)**
   - The cosmic grid is invaded by unstable Red Plasma Blocks. The Blue Collector Vessel (Player) is deployed to rescue falling Star Core Energy.
2. **Act II: The Rising Action & Escalation (Gameplay)**
   - As time ticks down (or in Survival Mode as waves progress), Red Plasma Blocks multiply and accelerate. The player must navigate tight gaps while managing invincibility timers and position clamping.
3. **Act III: Resolution & Concluding Round (Game Over / Victory)**
   - The round timer expires or energy runs out. The System Exception Diagnostics and Results Portal displays final score performance, stats, and option to restart.

### 2.2 Character Archetypes
- **The Hero (Player 1 - Blue Collector `#00BFFF`)**: Highly agile, WASD/Arrow responsive, equipped with temporary respawn shield invincibility.
- **The Ally (Player 2 - Green Collector `#00FF7F`)**: Co-op partner competing or assisting in Star Energy collection.
- **The Hazard (Red Plasma Obstacles `#DC3232`)**: Unpredictable, rebounding kinetic blocks patrolling screen channels.
- **The Objective (Celestial Star `#FFFF00`)**: Pulsing energy source that teleports upon collection.

---

## 3. Gameplay Mechanics & Level Design (Syllabus Weeks 11–13)

### 3.1 Mechanics & Controls
- **Movement Physics**: Frame-rate independent delta-time calculation (`position += velocity * dt`).
- **Collision Detection**: AABB (Axis-Aligned Bounding Box) rectangle intersection using `pygame.Rect.colliderect`.
- **Particle System**: 35-particle radial debris explosion on collision using trigonometric vector trajectories (`dx = cos(angle)*speed`, `dy = sin(angle)*speed`).

### 3.2 Level Space & Time Mechanics
- **Screen Boundary**: Clamped 800x600 resolution viewport (`clamp_ip`).
- **Time Interval**: Real-time tick engine (`clock.tick(60)`).
- **Challenge Curve**: Multi-mode balancing (Classic 30s, Survival Endless, Time Attack 60s, Zen No-Hazard, Nightmare 8-Enemy 2x Multiplier).

---

## 4. Audio & Graphics Engineering (IT2202 Compliance)

- **Procedural Sound Synthesis**: Native Python `struct` audio buffer generation (sinusoidal frequency sweeps, thunder white noise rumble).
- **Graphical Rendering Pipeline**: Surface alpha blending, neon borders, dynamic color gradients, and particle life decay scaling.
- **Developer Diagnostics Boundary**: Global error boundary (`_show_error_screen`) logging to `crash_log.txt`.
