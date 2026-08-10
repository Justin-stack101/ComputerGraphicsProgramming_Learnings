# Future Development Roadmap — Star Catcher & Web Ecosystem

This roadmap outlines planned future expansions, web system integrations, and gameplay improvements for the **Star Catcher** ecosystem.

---

## 🌐 1. Web System Port & Browser Ecosystem

- [ ] **HTML5 Canvas & JavaScript Web Port**:
  - Port the Pygame game engine to HTML5 Canvas & Web Audio API so it runs natively in any web browser without requiring Python installation.
- [ ] **Web-Based Online Leaderboard**:
  - Connect the game to a web database backend (e.g. Node.js / PostgreSQL / Firebase) to track global high scores and player stats online.
- [ ] **WebSockets Online Multiplayer**:
  - Upgrade the 2-Player local mode to real-time online multiplayer over WebSockets.
- [ ] **Customer & Player Web Portal Integration**:
  - Embed the game into web portals as a mini-game or interactive waiting-room entertainment system.

---

## 🎮 2. Multi-Game Modes & 2-Player Local Co-Op

- [ ] **2-Player Local Versus Mode**:
  - Player 1 (`WASD`, Cyan `#00BFFF`) vs Player 2 (`Arrow Keys`, Green `#00FF7F`) competing simultaneously for star captures on a single screen.
- [ ] **5 Distinct Game Modes**:
  - 🌟 **Classic Mode**: Standard 30s timer, 3 lives, 5 enemies.
  - 👥 **2-Player Versus Mode**: Simultaneous WASD vs Arrow Keys competition.
  - 🛡️ **Survival Mode**: Endless timer, 1 life only, progressive enemy count scaling over time.
  - ⏱️ **Time Attack Mode**: 60s extended timer, fast star spawns.
  - 🧘 **Zen / Practice Mode**: No enemies, no damage, relaxing star collection.
  - 💀 **Nightmare Mode**: 8 fast enemies, 2 lives, 2x Score Multiplier.

---

## 🚨 3. Developer Runtime Exception Diagnostics Portal

- [ ] **In-Game Diagnostic Recovery Screen**:
  - Styled error boundary modal featuring exception details, monospace stack trace output, session runtime metrics (FPS, State, Score), and interactive recovery buttons (`RELOAD GAME`, `MAIN MENU`, `EXPORT LOG`).

---

## 🎨 4. Graphics, Sound & Power-Ups

- [ ] **Pixel Art Sprites & Animations**: Replace color rectangles with custom animated sprites for Player, Enemies, and Stars.
- [ ] **Power-Up Items**: Add temporary drops (Shield 🛡️, Speed Boost ⚡, Star Magnet 🧲, Time Freeze ❄️).
- [ ] **Dynamic Soundtracks**: Selectable procedural background music tracks and combo pitch shifts.
