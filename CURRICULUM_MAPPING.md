# STI Curriculum Mapping & Course Compliance Guide
**Course Codes**: `IT2012` (Game Development/Game Programming) & `IT2202` (Computer Graphics Programming)  
**Project**: Star Catcher Interactive Engine  
**Repository**: [`Computer Graphics Programming`](file:///c:/Users/justi/Downloads/School%20Files/MainProjectCollection/Computer%20Graphics%20Programming/)

---

## 🎓 Course Outcomes (CO) Compliance Matrix

| Course | Code | Course Outcome Description | Implementation Evidence in Codebase |
| :--- | :--- | :--- | :--- |
| **IT2012** | **CO1** | Evaluate game development process from concept to production | [`GAME_DESIGN_DOCUMENT.md`](file:///c:/Users/justi/Downloads/School%20Files/MainProjectCollection/Computer%20Graphics%20Programming/GAME_DESIGN_DOCUMENT.md) (Concept, 3-Act Story, Production Pipeline) |
| **IT2012** | **CO2** | Examine concepts behind game development (Goals, Genres, Motivation, Balance, Level Design) | [`main_game.py`](file:///c:/Users/justi/Downloads/School%20Files/MainProjectCollection/Computer%20Graphics%20Programming/main_game.py) (`ModeSelectState`, `PlayingState` challenge curves, FSM balance) |
| **IT2012** | **CO3** | Apply game concepts & techniques in creating a working prototype | [`main_game.py`](file:///c:/Users/justi/Downloads/School%20Files/MainProjectCollection/Computer%20Graphics%20Programming/main_game.py) (Full playable Pygame engine, 2-Player mode, procedural audio, particle physics) |
| **IT2202** | **CO1** | Examine concepts & data structures to represent & manipulate geometry | [`main_game.py`](file:///c:/Users/justi/Downloads/School%20Files/MainProjectCollection/Computer%20Graphics%20Programming/main_game.py) (`pygame.Rect`, particle vector trajectories `dx`/`dy`, trigonometric screen flashes) |
| **IT2202** | **CO2** | Develop 2D and 3D computer graphics programs | 2D Pygame rendering pipeline, particle physics engine, custom procedural RGB sweeps |
| **IT2202** | **CO3** | Implement various approaches and techniques in creating interactive applications | Finite State Machine (`GameState`), Frame-Rate Independent Physics (`dt`), Developer Runtime Diagnostics Portal |

---

## 📅 Weekly Syllabus Alignment (Weeks 1 – 18)

### Weeks 1–2: Platforms, Time Intervals & Player Modes
- **Syllabus LO**: Distinguish time intervals & player modes.
- **Codebase Mapping**: 
  - Real-time delta-time physics (`dt` in `main_game.py:L976`).
  - Single-Player & 2-Player Local Co-Op/Versus (`P1 WASD` vs `P2 Arrows`).

### Weeks 3–4: Goals, Genres & Microgames
- **Syllabus LO**: Compare game genres, goals & microgame assets.
- **Codebase Mapping**: Arcade Action / Microgame mechanics (30-second timer challenge, star collection goal, red enemy avoidance).

### Weeks 6–7: Player Elements & Motivation
- **Syllabus LO**: Determine reasons for playing games & market context.
- **Codebase Mapping**: Score tracking, high score incentives, difficulty scaling (Survival vs Nightmare mode), audio feedback cues.

### Weeks 8–9: Story & Character Development (Pre-Production)
- **Syllabus LO**: Describe 3-act plot structure & character archetypes.
- **Codebase Mapping**: Detailed in [`GAME_DESIGN_DOCUMENT.md`](file:///c:/Users/justi/Downloads/School%20Files/MainProjectCollection/Computer%20Graphics%20Programming/GAME_DESIGN_DOCUMENT.md).

### Weeks 11–12: Gameplay Fundamentals & Challenge Balance
- **Syllabus LO**: Identify gameplay impact, challenges & balance.
- **Codebase Mapping**: `ModeSelectState` with 5 distinct balanced modes (Classic, 2-Player, Survival, Time Attack, Zen, Nightmare).

### Weeks 13: Level Design, Time & Space
- **Syllabus LO**: Design a gameplay level & physical environment space.
- **Codebase Mapping**: Screen boundary clamping (`clamp_ip`), enemy spawn bounds, star repositioning logic.

### Weeks 15–18: Project Development, Prototype & Final Presentation
- **Syllabus LO**: Create working prototype game & present final output.
- **Codebase Mapping**: Fully functional, modular `main_game.py` with `RUNNING_INSTRUCTIONS.md`, developer HUD (`F12`), and error boundary crash logging.
