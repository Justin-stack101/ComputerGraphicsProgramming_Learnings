# Master Download & Learning Checklist — IT2012 & IT2202 Success Kit

This checklist covers all software systems to download/install and key core concepts to learn for your **Game Development (IT2012)** and **Computer Graphics Programming (IT2202)** courses.

---

## 🛠️ Section 1: Software Systems & Downloads Checklist

### 1. Core Development Engine (Priority 1)
- [x] **Python 3.10+ (Installed: Python 3.14.2)**: Core programming language for Pygame 2D graphics math.
- [x] **Pygame-CE (Installed: pygame-ce 2.5.7)**: 2D rendering engine, delta-time physics, audio buffer synthesis.
- [x] **Antigravity IDE**: Primary AI pair programming workspace and terminal environment.

### 2. Editor & Version Control (Priority 1)
- [x] **VS Code (Visual Studio Code)**: IDE for Python, C#, and Markdown.
  - [x] Python Extension (`ms-python.python`)
  - [x] GitLens Extension (`eamodio.gitlens`)
  - [x] Markdown All in One (`yzhang.markdown-all-in-one`)
- [x] **Git for Windows**: Source control tool to push code to GitHub repositories.

### 3. Industry Engine & 3D Tools (Priority 2 - In Progress)
- [x] **Unity Hub**: Management dashboard for licenses, Unity Editor versions, and projects.
- [ ] **Unity Editor 2022.3 LTS (or Unity 6)**: 2D/3D visual game editor with C# scripting.
  - [ ] Android / Windows Build Support Module
  - [ ] Documentation Module
- [ ] **Blender 3D**: Free open-source 3D mesh modeling and texture mapping suite (for IT2202 3D Graphics).

---

## 🧠 Section 2: Core Concepts & Skills Learning Checklist

### 1. Game Architecture & Physics (Syllabus Weeks 1–4)
- [x] **Frame-Rate Independent Physics (`dt`)**:
  - Understand why multiplying movement by `dt` (`position += velocity * dt`) makes games run at identical speeds on low-spec and high-spec PCs.
- [x] **Finite State Machines (FSM)**:
  - Understand how to structure game flow using states (`StartMenuState` ➔ `PlayingState` ➔ `SettingsState` ➔ `PauseState` ➔ `GameOverState`) without main thread freezes.
- [ ] **2D Collision Math & Vector Trajectories**:
  - AABB bounding box collision (`colliderect`) and particle radial explosions (`dx = cos(angle)*speed`).

### 2. Audio & Visual Graphics Engineering (Syllabus Weeks 6–13)
- [x] **Interactive Volume Control & Settings**:
  - Master, Music, and SFX volume sliders (0%–100%) and reactive audio previews.
- [ ] **Procedural Audio Buffer Synthesis**:
  - Understanding how trigonometric sine waves (`math.sin`) generate sound frequencies in memory without external audio files.
- [ ] **Developer Exception Diagnostics & Crash Logging**:
  - How styled error screens (`_show_error_screen`) log trace reports to `crash_log.txt`.

### 3. Unity & C# Engine Fundamentals (Secondary Engine)
- [ ] **GameObjects & Component System**:
  - How Unity attaches components (`SpriteRenderer`, `Rigidbody2D`, `BoxCollider2D`, `C# Scripts`) to GameObjects.
- [ ] **C# Scripting (`Start` vs `Update`)**:
  - Writing C# scripts using `void Start()` for initialization and `void Update()` for frame updates (`Input.GetAxis`, `Time.deltaTime`).
- [ ] **Unity Tilemaps & Cinemachine**:
  - Painting 2D levels and setting up smooth camera tracking.

### 4. Systems Architecture & Security Foundations
- [x] **Architectural Mindset**:
  - Acting as Software Architect, defining project vision, and guiding AI agents.
- [ ] **Cybersecurity & Secure Coding Practices**:
  - Understanding threat modeling, input sanitization, API security, and keeping secret keys out of public Git repos.
- [ ] **Web System Porting Concepts**:
  - Understanding how HTML5 Canvas, Web Audio API, and WebSockets bring games to web browsers.
