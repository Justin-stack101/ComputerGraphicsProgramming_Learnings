# 🕹️ Game Loop Architecture & State Management

## Purpose

Enforce modular game loop design, delta-time physics calculations, and Finite State Machine (FSM) state separation.

---

## 1. The Standard Game Loop Pattern

All games must follow a 3-stage game loop sequence per frame:
1. **Process Input**: Capture keyboard, mouse, or controller events.
2. **Update State (`dt`)**: Update game physics, positions, timers, particle lifespans, and collision states using delta time.
3. **Render Pass (`surface`)**: Clear the screen buffer, render background, entities, particles, and HUD elements, and flip/update the display buffer.

```python
# Standard Pygame-ce Loop Pattern
dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

# 1. Process Input
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    current_state.handle_event(event)

# 2. Update
current_state.update(dt)

# 3. Render
screen.fill((20, 20, 30))
current_state.render(screen)
pygame.display.flip()
```

---

## 2. Finite State Machine (FSM) Pattern

Do not write messy, global `if/else` statements for game states inside the main loop. Implement an FSM pattern:

```python
class GameState:
    def handle_event(self, event): pass
    def update(self, dt): pass
    def render(self, surface): pass

class StartMenuState(GameState): ...
class PlayingState(GameState): ...
class PauseState(GameState): ...
class GameOverState(GameState): ...
```

- **State Transitions**: The `GameStateManager` maintains a stack or single reference to the `current_state`. State transitions (`change_state(PlayingState())`) cleanly reset state-specific variables.

---

## 3. Frame-Rate Independence (`dt`)

- **Rule**: Never add static integer pixel offsets (`x += 5`) per frame. If the frame rate drops from 60 FPS to 30 FPS, the game will run at half speed.
- **Enforcement**: Calculate all displacements using velocity vectors multiplied by delta time:
  $$\text{position\_x} += \text{velocity\_x} \times dt$$
