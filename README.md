# Pygame Demo — Computer Graphics Programming

## Overview

This project is a small Pygame demo for a Computer Graphics Programming assignment. The player controls a blue square with the arrow keys or WASD, collects a yellow star to gain score, and avoids red moving enemy blocks. The game includes a 30-second timer, 3 lives, brief invincibility after a hit, restart/quit prompts, and procedural audio effects.

## Controls

- Move: Arrow keys or WASD
- Pause / Settings menu: ESC
- Restart after game over/time up: R
- Quit after game over/time up: Q

### Arcade-Style Vertical List Menus
- **Up / Down or W / S**: Navigate options vertically with pulsing pointer selection
- **Left / Right or A / D**: Adjust volume sliders (0% to 100%) in the **Settings & Audio** menu
- **ENTER / SPACE**: Confirm active selection
- **Shortcut Keys**:
  - `M`: Toggle Master Mute (all audio)
  - `B`: Toggle BGM Mute (background music only)
  - `C`: Continue / Resume (during Pause)
  - `R`: Play Again (at Game Over)
  - `Q`: Quit Game

### Developer Testing Controls
Toggle Developer Mode during play by pressing **F12**. An status HUD overlay will appear with the following active key commands:
- G: Toggle God Mode (Invincibility bypass)
- T: Add 10 seconds to game timer
- + / =: Spawn an extra red enemy block
- -: Remove a red enemy block
- ]: Increase player movement speed
- [: Decrease player movement speed

## Features

- **Finite State Machine (FSM) Architecture**: Modular state handling via `StartMenuState`, `PlayingState`, `PauseState`, `SettingsState`, and `GameOverState`.
- **Interactive Settings & Volume Controls**: Dedicated `SettingsState` submenu with real-time reactive volume sliders (`Master`, `Music`, `SFX`) and audio preview cues.
- **Frame-Rate Independent Physics (`dt`)**: Movement, timers, and particle physics scale dynamically with delta-time (`dt`) for identical gameplay speed regardless of FPS.
- **Arcade-Style Vertical List Menus**: Clean vertical menu layout featuring neon blue/pink borders, animated selection pointers, and pulsing text prompts.
- **Granular Audio System**: Procedurally synthesized background music, movement loops, hit sweeps, and feedback sound cues.
- **HUD Indicator Panel**: Reflects master audio status and BGM controls.
- **Global Error Boundary & Logging**: Protects the program from abrupt crashes, printing styled trace details on an error screen and logging to `crash_log.txt`.
- **Fire Debris Particle Explosion Engine**: Renders 35 dynamic, color-blending, physics-simulated fire particles at collision points.
- **Synchronized Thunder & Lightning Storm Effects**: Screen flashes bright blue/white accompanied by a custom procedurally synthesized cracking thunder strike on collisions.
- **Losing Sound Sweep**: Plays a custom synthesized descending pitch frequency sweep representing disappointment upon Game Over.
- **Lives & Invincibility**: Respawn invincibility timer with visual flashing indicator.

## Project structure

- `main_game.py` — the complete game implementation
- `README.md` — project documentation
- `RUNNING_INSTRUCTIONS.md` — step-by-step setup and execution guide
- `FUTURE_ROADMAP.md` — future development roadmap and web system porting plans
- `requirements.txt` — Python dependency list
- `crash_log.txt` — generated log containing timestamps and trace data of unhandled exceptions
- `.gitignore` — files to ignore in Git
- `tools/` — helper/debug scripts used during setup and troubleshooting

## How to run on Windows

For full details, see [RUNNING_INSTRUCTIONS.md](file:///c:/Users/justi/Downloads/School%20Files/MainProjectCollection/Computer%20Graphics%20Programming/RUNNING_INSTRUCTIONS.md).

1. Open PowerShell or Command Prompt.
2. Change into the project folder:
   `cd "C:\Users\justi\Downloads\School Files\MainProjectCollection\Computer Graphics Programming"`
3. (Optional) Activate the virtual environment if present:
   - PowerShell: `.\.venv\Scripts\Activate`
   - Command Prompt: `.venv\Scripts\activate.bat`
4. Install dependencies if needed:
   `python -m pip install -r requirements.txt`
5. Run the game:
   `python main_game.py`

## How the game works

- The player moves around the screen and tries to collect the star.
- Each collected star increases the score.
- Red enemies move horizontally and can collide with the player.
- A collision costs one life.
- If the player still has lives, they briefly respawn with invincibility.
- If the player loses all lives, or the timer reaches zero, the game displays an end screen with restart/quit options.

## Notes for debugging

- Run the game from a terminal so Python errors are visible.
- If you change gameplay values, edit `main_game.py` directly.
- If pygame is missing, install it with `python -m pip install pygame-ce`.

## Future Roadmap

For full details on web porting, multi-game modes, and 2-Player modes, see [FUTURE_ROADMAP.md](file:///c:/Users/justi/Downloads/School%20Files/MainProjectCollection/Computer%20Graphics%20Programming/FUTURE_ROADMAP.md).


