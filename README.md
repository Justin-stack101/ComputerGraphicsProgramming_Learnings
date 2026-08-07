Pygame Demo — VS Code Pygame Demo

Overview

This is a small Pygame demo where the player (blue square) moves with arrow keys or WASD, collects a yellow star to increase score, and must avoid red moving enemy blocks. The game has a 30-second timer. When time runs out the game ends. Colliding with an enemy reduces lives; when lives reach 0 the player is shown a "Game Over" screen with options to try again or quit. The demo also includes simple sound effects for collecting stars, taking hits, and ending the game.

Controls

- Move: Arrow keys or WASD
- On end screen: R = Try again (restart the game), Q = Quit

Features implemented

- Player movement (arrow keys / WASD)
- Moving enemy blocks
- Collectible star that increases Score
- 30-second timer
- Lives (start with 3) and respawn on hit
- Brief invincibility after respawn, player flashes while invincible
- Simple sound effects for collecting stars, taking hits, and game over/restart events
- Procedurally generated background music and a looping movement sound effect while the player moves
- End screen offering R (restart) or Q (quit) so you can play nonstop by pressing R

How to run (Windows)

1. Open PowerShell or Command Prompt.
2. Change directory to the project folder:
   cd "C:\Users\justi\Downloads\School Files\MainProjectCollection\Computer Graphics Programming"
3. (Optional) Activate the virtual environment if present:
   In PowerShell: .\.venv\Scripts\Activate
   In cmd.exe: .venv\Scripts\activate.bat
4. Install dependencies if necessary (pygame-ce was used during development):
   python -m pip install pygame-ce
   or
   python -m pip install pygame
5. Run the game:
   python main_game.py

Project files

- main_game.py — The playable demo (updated with restart and invincibility)
- requirements.txt — Python dependency list for installing pygame-ce
- .gitignore — ignore generated files and local environment artifacts
- .venv — Optional virtual environment (if created)
- tools/ — helper and debug scripts for installing or diagnosing pygame and environment issues

How the restart/quit works

When the player runs out of lives or the timer reaches 0, an end-screen is displayed showing a message and a prompt: "Press R to try again or Q to quit." Pressing R resets the game state (score, lives, player position, star and enemies) so you can play again immediately. Pressing Q closes the game.

Tips for debugging and extending

- To see Python errors, run main_game.py from a terminal instead of double-clicking it — error tracebacks will remain visible in the terminal.
- To change the number of lives, edit the initial lives value in main_game.py.
- To increase invincibility duration after respawn, adjust INVINCIBLE_MS in main_game.py.

If you'd like, I can:
- Add on-screen "Invincible" indicator during the invincibility period
- Replace the text lives display with heart icons
- Tidy up or move debug files into a `tools/` folder

Enjoy — press R at the end screen to play nonstop!