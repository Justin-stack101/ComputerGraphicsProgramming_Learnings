# System Architecture & Technical Diagrams — Star Catcher Engine

This document provides visual architectural diagrams, state machine flows, and data models to present to Senior Software Architects, Lead Developers, and Project Evaluators.

---

## 1. Finite State Machine (FSM) State Diagram

The diagram below illustrates how `main_game.py` routes user inputs, game loops, menu transitions, and error boundaries without blocking the main execution thread:

```mermaid
stateDiagram-v2
    [*] --> StartMenuState
    
    StartMenuState --> PlayingState: Select START GAME [Enter / Space]
    StartMenuState --> SettingsState: Select SETTINGS [Enter / Space]
    StartMenuState --> [*]: Select QUIT [Q]
    
    SettingsState --> StartMenuState: Press BACK or ESC
    SettingsState --> PauseState: Press BACK or ESC (if opened from Pause)

    PlayingState --> PauseState: Press ESC
    PlayingState --> GameOverState: Lives == 0 or Time Expired
    
    PauseState --> PlayingState: Select CONTINUE / Press ESC
    PauseState --> SettingsState: Select SETTINGS
    PauseState --> [*]: Select QUIT GAME [Q]
    
    GameOverState --> PlayingState: Select PLAY AGAIN [R]
    GameOverState --> [*]: Select QUIT [Q]
    
    PlayingState --> CrashBoundary: Unhandled Exception
    CrashBoundary --> [*]: Export Log & Exit
```

---

## 2. Audio & Physics Rendering Pipeline

The diagram below outlines how player input events flow through delta-time physics calculation, collision detection, and procedural sound synthesis:

```mermaid
flowchart TD
    Input[User Input: WASD / Arrow Keys] --> Movement[Physics Engine: pos += vel * dt]
    Movement --> Clamping[Viewport Clamping: clamp_ip]
    Clamping --> CollisionCheck{Collision Detected?}
    
    CollisionCheck -- Star Collided --> Score[Score += 1]
    Score --> CollectAudio[AudioManager: play_collect]
    
    CollisionCheck -- Enemy Collided --> Damage[Lives -= 1]
    Damage --> ParticleSystem[Trigger Explosion: 35 Particles]
    ParticleSystem --> FlashStorm[Flash Screen + Play Thunder Sweep]
    
    CollisionCheck -- No Collision --> Render[Pygame Surface Render & Flip]
    CollectAudio --> Render
    FlashStorm --> Render
```

---

## 3. Future Web System Port & API Architecture

The diagram below illustrates the future web system architecture connecting the HTML5 game client, WebSockets server, and online leaderboard database:

```mermaid
flowchart LR
    subgraph Client Browser
        Canvas[HTML5 Canvas Game Engine]
        WebAudio[Web Audio API Synthesizer]
        WSClient[WebSocket Client / REST Engine]
    end
    
    subgraph Backend Server
        APIGateway[Node.js / Python API Gateway]
        Security[OAuth2 Auth & Rate Limiter]
        WSServer[WebSocket Multiplayer Hub]
    end
    
    subgraph Storage Layer
        DB[(PostgreSQL / Redis Leaderboard)]
        Logs[(Crash Diagnostics Log Bucket)]
    end
    
    Canvas --> WSClient
    WebAudio --> Canvas
    WSClient <--> APIGateway
    APIGateway --> Security
    Security <--> WSServer
    WSServer <--> DB
    APIGateway --> Logs
```

---

## 4. Developer Technical Summary for Architect Review

- **Architecture Pattern**: Finite State Machine (FSM) with decoupled Component-like State Handlers.
- **Physics Engine**: Frame-Rate Independent Delta-Time (`dt`) Physics Engine.
- **Audio Engine**: Buffer-level Sinusoidal Frequency & White Noise Synthesizer (`struct` / `bytearray`).
- **Resilience Boundary**: Global Exception Handler with structured logging (`crash_log.txt`).
