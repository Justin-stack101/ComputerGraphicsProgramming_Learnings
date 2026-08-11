# Environment & Software Setup Guide — IT2012 & IT2202 Success Kit

This guide outlines the exact software tools, environment setups, and hands-on practical exercises required to excel in **IT2012 (Game Development)** and **IT2202 (Computer Graphics Programming)**.

---

## 🛠️ Required Software & Installation Guide

### 1. Python 3.10+ & Pygame-CE (Primary 2D Graphics Engine)
- **Purpose**: Powers our 2D Graphics Math, Delta-Time physics, FSM Game Architecture, and Procedural Audio.
- **Download**: [python.org/downloads](https://www.python.org/downloads/)
- **Installation Check**:
  ```powershell
  python --version
  python -m pip install pygame-ce
  ```

---

### 2. VS Code (Visual Studio Code) & Recommended Extensions
- **Purpose**: Industry-standard IDE for writing Python scripts, inspecting Markdown documentation, and managing Git pushes.
- **Download**: [code.visualstudio.com](https://code.visualstudio.com/)
- **Recommended Extensions**:
  - `ms-python.python` (Python Language Support)
  - `eamodio.gitlens` (Git repository visualization)
  - `yzhang.markdown-all-in-one` (Markdown documentation tools)

---

### 3. Git & GitHub (Version Control & Portfolio)
- **Purpose**: Automatically track changes, stage commits, push to GitHub (`origin main`), and build an online portfolio for employers.
- **Download**: [git-scm.com/downloads](https://git-scm.com/downloads/)
- **Configuration Check**:
  ```powershell
  git --version
  git config --global user.name "Your Name"
  git config --global user.email "your.email@users.noreply.github.com"
  ```

---

### 4. Unity Engine & Unity Hub (IT2012 Syllabus Reference Software)
- **Purpose**: Referenced in syllabus books (*Unity Game Development Cookbook* & *2D Game Development with Unity*). Used for 2D/3D component-based game design.
- **Download**: [unity.com/download](https://unity.com/download) (Install **Unity Hub**, then add **Unity 2022.3 LTS** or **Unity 6** with 2D/3D modules).

---

### 5. Blender 3D (3D Modeling & Computer Graphics for IT2202)
- **Purpose**: Free, open-source 3D graphics creation suite for 3D mesh modeling, UV unwrapping, and asset creation.
- **Download**: [blender.org/download](https://www.blender.org/download/)

---

## 🎯 5 Hands-On Practical Exercises to Guarantee Success

To gain real-world experience and guarantee passing your major exams and laboratory assessments:

1. **Run & Inspect `main_game.py`**:
   - Execute `python main_game.py` from PowerShell.
   - Test the FSM state transitions, volume sliders in **SETTINGS**, and `F12` Developer HUD.
2. **Experiment with Frame-Rate Delta Time (`dt`)**:
   - Change `player_speed` in `main_game.py` and observe how movement vector math maintains smooth motion regardless of frame rate.
3. **Practice Git Workflow**:
   - Make a minor edit to documentation and run `git add .`, `git commit -m "docs: minor update"`, `git push origin main`.
4. **Inspect Procedural Audio Buffer Generation**:
   - Examine `_make_sound_sweep` in `main_game.py` to understand how trigonometric sine waves (`math.sin`) synthesize sound frequencies.
5. **Review Syllabus Mapping**:
   - Read [`CURRICULUM_MAPPING.md`](file:///c:/Users/justi/Downloads/School%20Files/MainProjectCollection/Computer%20Graphics%20Programming/CURRICULUM_MAPPING.md) and [`GAME_DESIGN_DOCUMENT.md`](file:///c:/Users/justi/Downloads/School%20Files/MainProjectCollection/Computer%20Graphics%20Programming/GAME_DESIGN_DOCUMENT.md) before your lab submissions.
