# 🎮 Game Project Profile — Pygame Computer Graphics Demo

> **This is the game codebase-specific context document.** It captures concrete facts about the game stack, window settings, control keys, procedural audio engine, and debug overlays.

---

## 🏗️ Technology Stack

- **Game Engine / Framework**: Python 3.x with `pygame-ce` (Pygame Community Edition v2.5.7+).
- **Audio Engine**: Synthesized PCM audio waveforms generated via `numpy` and `pygame.mixer` / `pygame.sndarray`.
- **Main Entry Point**: `main_game.py`.
- **Dependencies**: Listed in `requirements.txt` (`pygame-ce==2.5.7`).

---

## 🎮 Game Mechanics & Features

- **Player Unit**: Controlled via Arrow keys or WASD.
- **Collectibles**: Yellow star (adds score).
- **Hazards**: Moving red enemy blocks (reduces lives upon collision).
- **Timers & Lives**: 30-second countdown timer, 3 lives system with 1.5s invincibility respawn.
- **Visual FX**: 35-particle fire explosion engine with color interpolation, screen flash lightning FX, and particle pooling.
- **Audio Cues**: Procedurally synthesized BGM loops, thunder strike sfx, movement sound cues, and pitch frequency sweep on Game Over.

---

## ⚙️ Controls & Developer Hotkeys

- **Movement**: Arrow Keys / WASD.
- **Start Menu**: `SPACE` / `ENTER` to start.
- **Mute Controls**: `M` (Mute All), `B` (Mute BGM Only).
- **System Controls**: `ESC` (Pause/Settings), `R` (Restart), `Q` (Quit).
- **F12 Developer Debug Overlay**:
  - `F12`: Toggle Developer Debug HUD.
  - `G`: Toggle God Mode (Invincibility).
  - `T`: Add +10 seconds.
  - `+` / `-`: Add / Remove enemy blocks.
  - `[` / `]`: Adjust movement speed.

---

## 🛡️ Exception Tracing & Crash Logging

- **Graphical Crash Screen**: Unhandled Pygame exceptions are caught by a top-level try/except block.
- **Trace Logger**: Exceptions render trace coordinates on screen and write detailed callstack timestamps to `crash_log.txt`.
