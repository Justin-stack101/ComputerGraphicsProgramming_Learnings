# 🎨 Graphics Rendering & Particle Explosion Systems

## Purpose

Provide guidelines for rendering visual graphics, surface alpha blending, color sweeps, and high-performance particle explosion systems.

---

## 1. Particle Explosion Systems & Pooling

Particle explosions (e.g. fire debris, sparks, dust, star sparkles) add dynamic juice to games.

### Key Rules:
1. **Particle Lifetime**: Each particle must have a defined lifespan (e.g. 0.5 to 1.2 seconds), shrinking radius, and fading alpha.
2. **Color Interpolation**: Blend colors over time (e.g. bright white ➔ yellow ➔ orange ➔ deep red ➔ transparent).
3. **Physics Simulation**: Give particles initial velocity vectors (`vx`, `vy`), gravity acceleration, and drag/friction coefficient.

```python
class Particle:
    def __init__(self, x, y, color_start, color_end, lifetime):
        self.x = x
        self.y = y
        self.vx = random.uniform(-150, 150)
        self.vy = random.uniform(-150, 150)
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color_start = color_start
        self.color_end = color_end

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt

    def is_dead(self):
        return self.lifetime <= 0
```

---

## 2. Surface Alpha Blending & Visual FX

- **Screen Flashes (Lightning / Hit Visuals)**: Render semi-transparent overlay surfaces (`pygame.Surface` with `set_alpha()`) to produce flash effects during collisions or thunder strikes.
- **Blending Modes**: Utilize additive blending (`BLEND_ADD`) for glowing energy effects and fire particles.
- **Double Buffering**: Perform all draw calls on off-screen surfaces before blitting to the primary screen display.
