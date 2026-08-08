# Pygame Demo — Computer Graphics Programming

## Overview

This project is a small Pygame demo for a Computer Graphics Programming assignment. The player controls a blue square with the arrow keys or WASD, collects a yellow star to gain score, and avoids red moving enemy blocks. The game includes a 30-second timer, 3 lives, brief invincibility after a hit, restart/quit prompts, and procedural audio effects.

## Controls

- Move: Arrow keys or WASD
- Pause / Settings menu: ESC
- Restart after game over/time up: R
- Quit after game over/time up: Q

### Start Menu / Intro Screen
- SPACE / ENTER: Start game
- M: Mute all sounds
- B: Mute background music (BGM) only
- Q: Quit game

### Developer Testing Controls
Toggle Developer Mode during play by pressing **F12**. An status HUD overlay will appear with the following active key commands:
- G: Toggle God Mode (Invincibility bypass)
- T: Add 10 seconds to game timer
- + / =: Spawn an extra red enemy block
- -: Remove a red enemy block
- ]: Increase player movement speed
- [: Decrease player movement speed

## Features

- **Animated Start Menu & Intro Screen** with dynamic floating particles.
- **Granular Audio System** featuring procedural synthesised background music, movement loops, and feedback sound effect cues.
- **HUD Indicator Panel** reflecting master audio status and BGM controls.
- **Global Error boundary & Logging** protecting the program from abrupt closures, with styled callstack details printed on a Pygame error screen and saved locally to `crash_log.txt`.
- Player movement with keyboard input.
- Moving enemy obstacles.
- Collectible star that increases score.
- 30-second countdown timer.
- Lives system with respawn and invincibility.
- **Fire Debris Particle Explosion Engine**: Renders 35 dynamic, color-blending, physics-simulated fire particles at the collision point when the player hits a red block.
- **Synchronized Thunder & Lightning storm effects**: Screen flashes bright blue/white accompanied by a custom procedurally synthesized cracking thunder strike on *every* collision.
- **Losing sound sweep**: Plays a custom synthesized descending pitch frequency sweep representing disappointment upon Game Over.
- End screen that lets the player restart or quit.

## Project structure

- `main_game.py` — the complete game implementation
- `README.md` — project documentation
- `requirements.txt` — Python dependency list
- `crash_log.txt` — generated log containing timestamps and trace data of unhandled exceptions
- `.gitignore` — files to ignore in Git
- `tools/` — helper/debug scripts used during setup and troubleshooting

## How to run on Windows

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

## Future ideas

- Replace the text lives display with heart icons.
- Split the game into multiple modules such as `audio.py`, `config.py`, and `game.py`.

