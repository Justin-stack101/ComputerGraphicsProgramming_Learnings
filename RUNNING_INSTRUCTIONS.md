# Quick Run Guide — Star Catcher Demo

This document provides step-by-step instructions on how to set up, launch, and control the **Star Catcher** game demo.

---

## Step-by-Step Instructions

### Step 1: Open PowerShell or Command Prompt
Open your preferred terminal window (PowerShell, Command Prompt, or VS Code integrated terminal).

### Step 2: Navigate to the Project Directory
Run the following command to switch into the game project folder:

```powershell
cd "c:\Users\justi\Downloads\School Files\MainProjectCollection\Computer Graphics Programming"
```

### Step 3: Activate Virtual Environment (Optional)
If a Python virtual environment is set up in the folder, activate it:

- **PowerShell:**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Command Prompt:**
  ```cmd
  .venv\Scripts\activate.bat
  ```

### Step 4: Install Dependencies
Install required dependencies (`pygame-ce`) listed in `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

### Step 5: Launch the Game
Execute `main_game.py` to start the game window:

```powershell
python main_game.py
```

---

## Controls Summary

| Action | Control / Key |
| :--- | :--- |
| **Menu Navigation** | `Up` / `Down` or `W` / `S` |
| **Volume Adjustment (Settings)** | `Left` / `Right` or `A` / `D` |
| **Select / Confirm** | `Enter` or `Space` |
| **Move Player** | Arrow Keys or `W`, `A`, `S`, `D` |
| **Pause Game** | `ESC` |
| **Quick Resume** | `C` or `ESC` (during Pause) |
| **Master Mute Toggle** | `M` |
| **BGM Mute Toggle** | `B` |
| **Developer Tools HUD** | `F12` |
| **Quit Game** | `Q` |

---

## Troubleshooting & Crash Logs
- If `pygame` is missing, install it manually: `python -m pip install pygame-ce`.
- If an unhandled exception occurs during gameplay, a diagnostic report will be saved automatically to `crash_log.txt`.
