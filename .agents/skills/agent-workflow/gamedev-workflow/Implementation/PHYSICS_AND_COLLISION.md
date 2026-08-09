# ⚡ Physics, Movement & Collision Systems

## Purpose

Enforce AABB bounding box collision checks, invincibility timers, smooth player movement, and developer testing controls.

---

## 1. Axis-Aligned Bounding Box (AABB) Collision

- **Bounding Box Collision**: Check rectangle overlaps between player and entities:
  $$\text{collides} = (A.x < B.x + B.w) \land (A.x + A.w > B.x) \land (A.y < B.y + B.h) \land (A.y + A.h > B.y)$$
- **Pygame Native Rect**: Utilize `pygame.Rect.colliderect()` for fast CPU collision checks.

---

## 2. Respawn & Invincibility Timers

- **Hit Response**: When a collision occurs with an enemy obstacle:
  1. Deduct 1 life.
  2. If lives remain, trigger a **Respawn Invincibility Timer** (e.g. 1.5 seconds) where the player blinks and ignores enemy collisions.
  3. Spawn a particle explosion and trigger a thunder/screen-flash effect.
  4. If lives reach 0 or game timer reaches 0, transition to `GAME_OVER`.

---

## 3. Developer Testing Controls Overlay (F12)

Always build developer testing controls behind an **F12 Toggle Hotkey**:
- **`F12`**: Toggle Developer Debug HUD.
- **`G`**: Toggle God Mode (Invincibility bypass).
- **`T`**: Add +10 seconds to game countdown timer.
- **`+ / =`**: Spawn extra enemy obstacle.
- **`-`**: Remove an enemy obstacle.
- **`[` / `]`**: Decrease / Increase player speed.
