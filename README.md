# Pygame Demo — Computer Graphics Programming

## Overview

This project is a small Pygame demo for a Computer Graphics Programming assignment. The player controls a blue square with the arrow keys or WASD, collects a yellow star to gain score, and avoids red moving enemy blocks. The game includes a 30-second timer, 3 lives, brief invincibility after a hit, restart/quit prompts, and procedural audio effects.

## Controls

- Move: Arrow keys or WASD
- Restart after game over/time up: R
- Quit after game over/time up: Q

## Features

- Player movement with keyboard input
- Moving enemy obstacles
- Collectible star that increases score
- 30-second countdown timer
- Lives system with respawn and invincibility
- End screen that lets the player restart or quit
- Procedurally generated background music and movement sound
- Simple sound effects for collecting stars, getting hit, and game over

## Project structure

- `main_game.py` — the complete game implementation
- `README.md` — project documentation
- `requirements.txt` — Python dependency list
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

- Add an on-screen “Invincible” indicator
- Replace the text lives display with heart icons
- Split the game into multiple modules such as `audio.py`, `config.py`, and `game.py`
