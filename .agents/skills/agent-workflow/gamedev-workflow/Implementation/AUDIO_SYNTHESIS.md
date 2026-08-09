# 🔊 Procedural Audio & Sound Synthesis Guidelines

## Purpose

Enforce procedural audio generation, synthesized sound cues, channel pools, and master audio toggle controls.

---

## 1. Procedural Audio Synthesis (NumPy / PCM Arrays)

Generating audio dynamically in code eliminates the need for external `.wav` or `.mp3` assets while providing retro 8-bit sound effects.

### Common Procedural Waves:
- **Sine Wave**: Smooth tone for pickup sounds, star collectibles, and UI clicks.
- **Square / Sawtooth Wave**: Retro arcade sound for laser beams and engine loops.
- **White Noise**: Synthesized random noise for explosions, thunder cracks, and wind.

```python
import numpy as np
import pygame

def generate_tone(frequency, duration, sample_rate=44100):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    # Generate sine wave
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    # Convert to 16-bit PCM sound format
    audio = (wave * 32767).astype(np.int16)
    # Stereo formatting
    stereo_audio = np.column_stack((audio, audio))
    return pygame.sndarray.make_sound(stereo_audio)
```

---

## 2. Audio Channel Management & Mute Toggles

- **Separate BGM & SFX Channels**: Dedicate channel 0 for Background Music (BGM) loops and channels 1-7 for sound effect cues (explosions, pickups, hit sweeps).
- **Master Audio Controls**: Implement global keyboard shortcuts:
  - `M`: Toggle Master Mute (mutes all audio channels).
  - `B`: Toggle BGM Mute (mutes music loop while leaving sound effect cues audible).
