"""A small Pygame demo for Computer Graphics Programming.

The game features keyboard movement, enemy obstacles, scoring, lives,
invincibility after a hit, restart/quit prompts, and procedural audio.
"""
import math
import os
import struct
import sys
from dataclasses import dataclass
from random import randint

# Remove the script directory from sys.path to avoid importing a local pygame.py file
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)

import pygame


@dataclass
class Enemy:
    """Represents one moving enemy block in the game."""

    rect: pygame.Rect
    speed: int
    direction: int


@dataclass
class GameConfig:
    """Configuration values used throughout the game."""
    screen_width: int = 800
    screen_height: int = 600
    player_width: int = 50
    player_height: int = 50
    player_speed: int = 6
    enemy_count: int = 5
    invincible_ms: int = 2000
    flash_interval_ms: int = 150
    timer_seconds: int = 30


class AudioManager:
    """Handles procedural sound effects and the looping background music."""

    def __init__(self) -> None:
        self.background_music = None
        self.movement_loop = None
        self.background_channel = None
        self.movement_channel = None
        self.music_enabled = False
        self._load_sounds()

    def _make_sound_sweep(self, start_freq: float, end_freq: float, duration_ms: int = 150, volume: float = 0.5) -> pygame.mixer.Sound:
        sample_rate = 44100
        sample_count = int(sample_rate * duration_ms / 1000)
        buffer = bytearray()
        for index in range(sample_count):
            fraction = index / sample_count
            # Linear frequency interpolation
            current_freq = start_freq + (end_freq - start_freq) * fraction
            # Phase accumulation to prevent clicks
            time_val = index / sample_rate
            value = int(32767 * volume * math.sin(2 * math.pi * current_freq * time_val))
            buffer.extend(struct.pack('<h', value))
        return pygame.mixer.Sound(buffer=bytes(buffer))

    def _load_sounds(self) -> None:
        try:
            self.collect_sound = self._make_sound(880, 120, 0.5)
            self.hit_sound = self._make_sound(220, 180, 0.7)
            # tuned game over/lose sound: descending frequency sweep for disappointment feel
            self.game_over_sound = self._make_sound_sweep(300, 80, 600, 0.7)
            # Distinct death sound played when the player loses their last life
            # tuned death sound: lower pitch and longer duration for impact
            self.death_sound = self._make_sound(100, 700, 1.0)
            self.restart_sound = self._make_sound(660, 120, 0.5)
            # small navigation/click sound for end-screen choices
            self.menu_nav = self._make_sound(1200, 70, 0.6)
            
            # Procedural Thunder sound (low rumble with white noise crackle)
            self.thunder_sound = self._make_thunder_sound()
            
            self.background_music = self._make_background_music()
            self.movement_loop = self._make_movement_sound()
            self.background_channel = pygame.mixer.Channel(0)
            self.movement_channel = pygame.mixer.Channel(1)
            # track mute state and default volumes
            self.muted_all = False
            self.muted_music = False
            self.muted_sfx = False
            self.master_volume = 1.0
            self.bgm_volume = 1.0
            self.sfx_volume = 1.0
            self._background_vol = 1.0
            self._movement_vol = 1.0
            self.music_enabled = True
            self.apply_volumes()
        except pygame.error:
            self.music_enabled = False

    def apply_volumes(self) -> None:
        """Recalculate and apply volume levels to all background and sound effect channels."""
        if not self.music_enabled:
            return
        eff_bgm = 0.0 if (self.muted_all or self.muted_music) else (self.master_volume * self.bgm_volume)
        eff_sfx = 0.0 if (self.muted_all or self.muted_sfx) else (self.master_volume * self.sfx_volume)

        try:
            if hasattr(self, 'background_channel') and self.background_channel:
                self.background_channel.set_volume(eff_bgm * self._background_vol)
                if eff_bgm > 0.0:
                    if not self.background_channel.get_busy() and hasattr(self, 'background_music'):
                        self.background_channel.play(self.background_music, loops=-1)
                else:
                    if self.background_channel.get_busy():
                        self.background_channel.set_volume(0.0)

            if hasattr(self, 'movement_channel') and self.movement_channel:
                self.movement_channel.set_volume(eff_sfx * self._movement_vol)

            sound_list = ['collect_sound', 'hit_sound', 'game_over_sound', 'death_sound', 'restart_sound', 'menu_nav', 'thunder_sound']
            for snd_name in sound_list:
                if hasattr(self, snd_name):
                    snd = getattr(self, snd_name)
                    if hasattr(snd, 'set_volume'):
                        snd.set_volume(eff_sfx)
        except Exception:
            pass

    def set_master_volume(self, vol: float) -> None:
        self.master_volume = max(0.0, min(1.0, round(vol, 2)))
        self.apply_volumes()

    def set_bgm_volume(self, vol: float) -> None:
        self.bgm_volume = max(0.0, min(1.0, round(vol, 2)))
        self.apply_volumes()

    def set_sfx_volume(self, vol: float) -> None:
        self.sfx_volume = max(0.0, min(1.0, round(vol, 2)))
        self.apply_volumes()

    def _make_sound(self, frequency: float, duration_ms: int = 150, volume: float = 0.5) -> pygame.mixer.Sound:
        sample_rate = 44100
        sample_count = int(sample_rate * duration_ms / 1000)
        buffer = bytearray()
        for index in range(sample_count):
            value = int(32767 * volume * math.sin(2 * math.pi * frequency * index / sample_rate))
            buffer.extend(struct.pack('<h', value))
        return pygame.mixer.Sound(buffer=bytes(buffer))

    def _make_background_music(self, loop_seconds: float = 2.2, volume: float = 0.18) -> pygame.mixer.Sound:
        sample_rate = 44100
        loop_samples = int(sample_rate * loop_seconds)
        buffer = bytearray()
        note_pattern = [
            (261.63, 0.24),
            (329.63, 0.24),
            (392.00, 0.24),
            (523.25, 0.24),
            (392.00, 0.24),
            (329.63, 0.24),
            (261.63, 0.24),
            (196.00, 0.24),
        ]
        for note_freq, note_len in note_pattern:
            note_samples = int(sample_rate * note_len)
            for index in range(note_samples):
                time_value = index / sample_rate
                primary = math.sin(2 * math.pi * note_freq * time_value)
                bass = 0.35 * math.sin(2 * math.pi * (note_freq * 0.5) * time_value)
                fade_in = min(index / (sample_rate * 0.03), 1.0)
                fade_out = (note_samples - index) / (sample_rate * 0.03)
                fade = min(fade_in, max(0.0, fade_out))
                sample = int(32767 * volume * fade * (0.75 * primary + 0.25 * bass))
                buffer.extend(struct.pack('<h', sample))
        while len(buffer) < loop_samples * 2:
            buffer.extend(buffer)
        return pygame.mixer.Sound(buffer=bytes(buffer[:loop_samples * 2]))

    def _make_movement_sound(self, volume: float = 0.12) -> pygame.mixer.Sound:
        return self._make_sound(720, 120, volume)

    def _make_thunder_sound(self, duration_ms: int = 1500, volume: float = 0.85) -> pygame.mixer.Sound:
        import random
        sample_rate = 44100
        sample_count = int(sample_rate * duration_ms / 1000)
        buffer = bytearray()
        
        for index in range(sample_count):
            time_val = index / sample_rate
            # 1. Low frequency earthquake rumble (30Hz - 85Hz dynamic modulation)
            rumble_freq = 45 + 15 * math.sin(2 * math.pi * 3.5 * time_val)
            rumble = math.sin(2 * math.pi * rumble_freq * time_val)
            
            # 2. Crackling electricity / white noise component
            noise = random.uniform(-1.0, 1.0)
            
            # 3. Dynamic envelope (sharp strike, crackling decay, fading rumble)
            strike_end = int(sample_rate * 0.15)
            if index < strike_end:
                # Initial lightning strike
                envelope = 1.0
                mix = 0.5 * rumble + 0.5 * noise
            else:
                # Decaying thunder rumble
                progress = (index - strike_end) / (sample_count - strike_end)
                envelope = (1.0 - progress) ** 2.0
                # crackle dissipates, leaving low sub-bass rumble
                crackle_fade = max(0.0, 1.0 - progress * 3.0)
                mix = 0.85 * rumble + 0.15 * noise * crackle_fade
            
            value = int(32767 * volume * envelope * mix)
            buffer.extend(struct.pack('<h', value))
            
        return pygame.mixer.Sound(buffer=bytes(buffer))

    def play_thunder(self) -> None:
        """Play the procedural thunder strike sound effect."""
        if self.music_enabled and not self.muted_all:
            self.thunder_sound.play()

    def start_background_music(self) -> None:
        if self.music_enabled and not self.muted:
            self.apply_volumes()

    def set_muted_all(self, muted: bool) -> None:
        """Mute or unmute ALL sounds and music."""
        if not self.music_enabled:
            return
        self.muted_all = bool(muted)
        self.apply_volumes()

    def set_muted_music(self, muted: bool) -> None:
        """Mute or unmute ONLY background music."""
        if not self.music_enabled:
            return
        self.muted_music = bool(muted)
        self.apply_volumes()

    @property
    def muted(self) -> bool:
        return self.muted_all

    def set_muted(self, muted: bool) -> None:
        self.set_muted_all(muted)

    def stop_movement_audio(self) -> None:
        """Explicitly stop any playing movement loop sound."""
        if self.music_enabled and hasattr(self, 'movement_channel') and self.movement_channel:
            try:
                if self.movement_channel.get_busy():
                    self.movement_channel.stop()
            except Exception:
                pass

    def play_collect(self) -> None:
        if self.music_enabled and not self.muted_all and not self.muted_sfx:
            self.collect_sound.play()

    def play_hit(self) -> None:
        if self.music_enabled and not self.muted_all and not self.muted_sfx:
            self.hit_sound.play()

    def play_game_over(self) -> None:
        if self.music_enabled and not self.muted_all and not self.muted_sfx:
            self.game_over_sound.play()

    def play_death(self) -> None:
        """Play the death sound (used when the player loses their last life)."""
        if self.music_enabled and not self.muted_all and not self.muted_sfx:
            # play immediately
            self.death_sound.play()

    def play_menu_nav(self) -> None:
        """Play a small nav/click sound when the user moves or selects in menus."""
        if self.music_enabled and hasattr(self, 'menu_nav') and not self.muted_all and not self.muted_sfx:
            self.menu_nav.play()

    def play_restart(self) -> None:
        if self.music_enabled and not self.muted_all and not self.muted_sfx:
            self.restart_sound.play()

    def update_movement_audio(self, is_moving: bool) -> None:
        if not self.music_enabled or self.muted or self.muted_sfx:
            if hasattr(self, 'movement_channel') and self.movement_channel and self.movement_channel.get_busy():
                self.movement_channel.stop()
            return
        if is_moving and not self.movement_channel.get_busy():
            self.movement_channel.play(self.movement_loop, loops=-1)
        elif not is_moving and self.movement_channel.get_busy():
            self.movement_channel.stop()


class GameState:
    """Base interface for all distinct game states in the FSM."""
    def handle_event(self, game: 'Game', event: pygame.event.Event) -> None:
        pass
    def update(self, game: 'Game', dt: float) -> None:
        pass
    def render(self, game: 'Game', surface: pygame.Surface) -> None:
        pass


class SettingsState(GameState):
    """Submenu for configuring master/music/SFX volume and audio settings."""
    def __init__(self, return_state: GameState) -> None:
        self.return_state = return_state
        self.selected_idx = 0
        self.start_time = pygame.time.get_ticks()

    def handle_event(self, game: 'Game', event: pygame.event.Event) -> None:
        options = ['master', 'bgm', 'sfx', 'audio_toggle', 'back']

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_idx = (self.selected_idx - 1) % len(options)
                game.audio.play_menu_nav()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_idx = (self.selected_idx + 1) % len(options)
                game.audio.play_menu_nav()
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self._adjust(game, options[self.selected_idx], -0.1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._adjust(game, options[self.selected_idx], 0.1)
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                opt = options[self.selected_idx]
                if opt == 'audio_toggle':
                    game.audio.set_muted_all(not game.audio.muted_all)
                    game.audio.play_menu_nav()
                elif opt == 'back':
                    game.audio.play_menu_nav()
                    game.state = self.return_state
            elif event.key == pygame.K_ESCAPE:
                game.audio.play_menu_nav()
                game.state = self.return_state

    def _adjust(self, game: 'Game', option_id: str, delta: float) -> None:
        if option_id == 'master':
            game.audio.set_master_volume(game.audio.master_volume + delta)
            game.audio.play_menu_nav()
        elif option_id == 'bgm':
            game.audio.set_bgm_volume(game.audio.bgm_volume + delta)
            game.audio.play_menu_nav()
        elif option_id == 'sfx':
            game.audio.set_sfx_volume(game.audio.sfx_volume + delta)
            game.audio.play_menu_nav()
        elif option_id == 'audio_toggle':
            game.audio.set_muted_all(not game.audio.muted_all)
            game.audio.play_menu_nav()

    def update(self, game: 'Game', dt: float) -> None:
        if isinstance(self.return_state, PauseState):
            self.return_state.update(game, dt)

    def render(self, game: 'Game', surface: pygame.Surface) -> None:
        if isinstance(self.return_state, PauseState):
            self.return_state.render(game, surface)
        else:
            surface.fill((10, 14, 26))

        now = pygame.time.get_ticks()
        elapsed = (now - self.start_time) / 1000.0

        panel_w, panel_h = 580, 420
        panel_x = (game.config.screen_width - panel_w) // 2
        panel_y = (game.config.screen_height - panel_h) // 2

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (15, 20, 35, 245), (0, 0, panel_w, panel_h), border_radius=16)
        pygame.draw.rect(panel, (0, 191, 255), (0, 0, panel_w, panel_h), width=4, border_radius=16)
        pygame.draw.rect(panel, (255, 20, 147), (5, 5, panel_w - 10, panel_h - 10), width=2, border_radius=12)

        title_font = pygame.font.SysFont('Arial', 40, bold=True)
        option_font = pygame.font.SysFont('Arial', 22, bold=True)
        val_font = pygame.font.SysFont('Arial', 20, bold=True)
        footer_font = pygame.font.SysFont('Arial', 14, bold=True)

        title = title_font.render('SETTINGS & AUDIO', True, (0, 255, 255))
        panel.blit(title, ((panel_w - title.get_width()) // 2, 25))

        items = [
            ('master', 'MASTER VOL', game.audio.master_volume),
            ('bgm', 'MUSIC VOL', game.audio.bgm_volume),
            ('sfx', 'SFX VOL', game.audio.sfx_volume),
            ('audio_toggle', 'ALL AUDIO', 'MUTED' if game.audio.muted_all else 'ENABLED'),
            ('back', 'BACK TO MENU', None),
        ]

        start_y = 95
        row_gap = 55
        for idx, (item_id, label, value) in enumerate(items):
            is_selected = (idx == self.selected_idx)
            text_color = (255, 215, 0) if is_selected else (160, 185, 215)

            if is_selected:
                px = 35 + int(math.sin(elapsed * 10) * 3)
                py = start_y + idx * row_gap + 12
                points = [(px, py - 7), (px + 10, py), (px, py + 7)]
                pygame.draw.polygon(panel, (255, 215, 0), points)

            lbl_txt = option_font.render(label, True, text_color)
            panel.blit(lbl_txt, (55, start_y + idx * row_gap))

            if isinstance(value, float):
                pct = int(round(value * 100))
                filled_blocks = int(round(value * 10))
                bar_str = '█' * filled_blocks + '░' * (10 - filled_blocks)
                slider_txt = val_font.render(f"[{bar_str}] {pct}%", True, (0, 255, 255) if is_selected else (120, 160, 190))
                panel.blit(slider_txt, (250, start_y + idx * row_gap + 2))
            elif isinstance(value, str):
                t_color = (255, 80, 80) if value == 'MUTED' else (0, 255, 128)
                val_txt = val_font.render(f"[ {value} ]", True, t_color if is_selected else (120, 160, 190))
                panel.blit(val_txt, (250, start_y + idx * row_gap + 2))

        blink = int(elapsed * 2) % 2 == 0
        if blink:
            footer_text = footer_font.render('USE LEFT / RIGHT ARROWS TO ADJUST VOLUME', True, (255, 20, 147))
        else:
            footer_text = footer_font.render('PRESS ENTER OR ESC TO RETURN', True, (0, 255, 128))
        panel.blit(footer_text, ((panel_w - footer_text.get_width()) // 2, 375))

        surface.blit(panel, (panel_x, panel_y))


class StartMenuState(GameState):
    """Intro start menu screen driven by keyboard navigation."""
    def __init__(self) -> None:
        self.selected_idx = 0
        self.start_time = pygame.time.get_ticks()

    def handle_event(self, game: 'Game', event: pygame.event.Event) -> None:
        options = [
            {'id': 'start', 'label': 'START GAME'},
            {'id': 'settings', 'label': 'SETTINGS'},
            {'id': 'quit', 'label': 'QUIT'}
        ]

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_idx = (self.selected_idx - 1) % len(options)
                game.audio.play_menu_nav()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_idx = (self.selected_idx + 1) % len(options)
                game.audio.play_menu_nav()
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                game.audio.play_menu_nav()
                opt_id = options[self.selected_idx]['id']
                if opt_id == 'start':
                    game.reset()
                    game.state = PlayingState()
                elif opt_id == 'settings':
                    game.state = SettingsState(return_state=self)
                elif opt_id == 'quit':
                    game.running = False
            # Direct shortcuts
            elif event.key == pygame.K_m:
                game.audio.set_muted_all(not game.audio.muted_all)
                game.audio.play_menu_nav()
            elif event.key == pygame.K_b:
                game.audio.set_muted_music(not game.audio.muted_music)
                game.audio.play_menu_nav()
            elif event.key == pygame.K_q:
                game.running = False

    def update(self, game: 'Game', dt: float) -> None:
        pass

    def render(self, game: 'Game', surface: pygame.Surface) -> None:
        now = pygame.time.get_ticks()
        elapsed = (now - self.start_time) / 1000.0

        options = [
            {'id': 'start', 'label': 'START GAME'},
            {'id': 'settings', 'label': 'SETTINGS'},
            {'id': 'quit', 'label': 'QUIT'}
        ]

        # Animated Background
        surface.fill((10, 14, 26))
        for i in range(15):
            px = (int(i * 65 + elapsed * 25)) % game.config.screen_width
            py = (int(i * 45 + math.sin(elapsed + i) * 25)) % game.config.screen_height
            pygame.draw.rect(surface, (28, 42, 68), (px, py, 10, 10), border_radius=2)

        # Center Card Modal
        panel_w, panel_h = 560, 400
        panel_x = (game.config.screen_width - panel_w) // 2
        panel_y = (game.config.screen_height - panel_h) // 2

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (15, 20, 35, 240), (0, 0, panel_w, panel_h), border_radius=16)
        
        # Neon Borders
        pygame.draw.rect(panel, (0, 191, 255), (0, 0, panel_w, panel_h), width=4, border_radius=16)
        pygame.draw.rect(panel, (255, 20, 147), (5, 5, panel_w - 10, panel_h - 10), width=2, border_radius=12)

        title_font = pygame.font.SysFont('Arial', 48, bold=True)
        subtitle_font = pygame.font.SysFont('Arial', 20)
        option_font = pygame.font.SysFont('Arial', 24, bold=True)
        footer_font = pygame.font.SysFont('Arial', 16, bold=True)

        # Draw shadow
        title_shadow = title_font.render('STAR CATCHER DEMO', True, (120, 0, 120))
        panel.blit(title_shadow, ((panel_w - title_shadow.get_width()) // 2 + 3, 30 + 3))
        
        title = title_font.render('STAR CATCHER DEMO', True, (0, 255, 255))
        panel.blit(title, ((panel_w - title.get_width()) // 2, 30))

        sub = subtitle_font.render('Avoid red obstacles & collect stars!', True, (160, 185, 215))
        panel.blit(sub, ((panel_w - sub.get_width()) // 2, 95))

        # Vertical List
        start_y = 150
        row_gap = 45
        for idx, opt in enumerate(options):
            is_selected = (idx == self.selected_idx)
            if is_selected:
                text_color = (255, 215, 0)
                px = 120 + int(math.sin(elapsed * 10) * 4)
                py = start_y + idx * row_gap + 15
                points = [(px, py - 8), (px + 12, py), (px, py + 8)]
                pygame.draw.polygon(panel, (255, 215, 0), points)
                pygame.draw.polygon(panel, (255, 255, 200), points, width=1)
            else:
                text_color = (150, 175, 205)

            opt_text = option_font.render(opt['label'], True, text_color)
            panel.blit(opt_text, (150, start_y + idx * row_gap))

        blink = int(elapsed * 2) % 2 == 0
        if blink:
            footer_text = footer_font.render('PRESS ENTER OR SPACE TO START', True, (255, 20, 147))
        else:
            footer_text = footer_font.render('USE WASD / ARROWS TO NAVIGATE', True, (0, 255, 128))
        panel.blit(footer_text, ((panel_w - footer_text.get_width()) // 2, 345))

        surface.blit(panel, (panel_x, panel_y))


class PlayingState(GameState):
    """Main gameplay loop driven by frame-rate independent updates."""
    def handle_event(self, game: 'Game', event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.state = PauseState(self)
            elif event.key == pygame.K_F12:
                game.dev_mode = not game.dev_mode
                game.audio.play_menu_nav()
            elif game.dev_mode:
                if event.key == pygame.K_g:
                    game.god_mode = not game.god_mode
                    game.audio.play_menu_nav()
                elif event.key == pygame.K_t:
                    game.timer_bonus += 10.0
                    game.audio.play_collect()
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS):
                    x = randint(200, game.config.screen_width - 100)
                    y = randint(50, game.config.screen_height - 100)
                    speed = randint(2, 5)
                    direction = 1 if len(game.enemies) % 2 == 0 else -1
                    game.enemies.append(Enemy(rect=pygame.Rect(x, y, 60, 60), speed=speed, direction=direction))
                    game.audio.play_menu_nav()
                elif event.key in (pygame.K_MINUS, pygame.K_UNDERSCORE):
                    if game.enemies:
                        game.enemies.pop()
                        game.audio.play_menu_nav()
                elif event.key == pygame.K_RIGHTBRACKET:
                    game.config.player_speed = min(20, game.config.player_speed + 1)
                    game.audio.play_menu_nav()
                elif event.key == pygame.K_LEFTBRACKET:
                    game.config.player_speed = max(1, game.config.player_speed - 1)
                    game.audio.play_menu_nav()

    def update(self, game: 'Game', dt: float) -> None:
        now = pygame.time.get_ticks()
        
        if game.invincible and now > game.invincible_end:
            game.invincible = False

        # Move player using dt
        keys = pygame.key.get_pressed()
        is_moving = False
        speed_pps = game.config.player_speed * 60
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game.player.x -= speed_pps * dt
            is_moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game.player.x += speed_pps * dt
            is_moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            game.player.y -= speed_pps * dt
            is_moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            game.player.y += speed_pps * dt
            is_moving = True

        game.player.clamp_ip(pygame.Rect(0, 0, game.config.screen_width, game.config.screen_height))
        game.audio.update_movement_audio(is_moving)

        # Move enemies using dt
        for enemy in game.enemies:
            enemy.rect.x += enemy.speed * 60 * enemy.direction * dt
            if enemy.rect.left < 0 or enemy.rect.right > game.config.screen_width:
                enemy.direction *= -1
                enemy.rect.x += enemy.speed * 60 * enemy.direction * dt * 2

        # Collect star
        if game.player.colliderect(game.star):
            game.score += 1
            game.audio.play_collect()
            game.star.x = randint(50, game.config.screen_width - 50)
            game.star.y = randint(50, game.config.screen_height - 50)

        # Particles update
        active_particles = []
        for p in game.particles:
            p['x'] += p['dx'] * 60 * dt
            p['y'] += p['dy'] * 60 * dt
            p['dx'] *= math.pow(0.96, 60 * dt)
            p['dy'] *= math.pow(0.96, 60 * dt)
            p['life'] -= 60 * dt
            if p['life'] > 0:
                active_particles.append(p)
        game.particles = active_particles

        # Hit detection
        if not (game.invincible or game.god_mode):
            collided_enemy = None
            for enemy in game.enemies:
                if game.player.colliderect(enemy.rect):
                    collided_enemy = enemy
                    break
            
            if collided_enemy:
                mid_x = (game.player.centerx + collided_enemy.rect.centerx) // 2
                mid_y = (game.player.centery + collided_enemy.rect.centery) // 2
                game._trigger_explosion(mid_x, mid_y)
                game.audio.stop_movement_audio()
                game.lives -= 1
                
                game.audio.play_thunder()
                game._flash_screen((240, 245, 255), duration_ms=250)
                game.audio.play_hit()

                if game.lives > 0:
                    game.state = PauseState(self, is_collision_pause=True)
                else:
                    game.audio.play_death()
                    game.audio.play_game_over()
                    game._flash_screen()
                    game.state = GameOverState('Game Over! No lives left.')
                    
        # Countdowns
        game.time_elapsed += dt
        time_left = max(0, game.config.timer_seconds + game.timer_bonus - game.time_elapsed)
        if time_left <= 0:
            game.audio.play_death()
            game._flash_screen()
            game.state = GameOverState('Time up! Well done.')

    def render(self, game: 'Game', surface: pygame.Surface) -> None:
        now = pygame.time.get_ticks()
        surface.fill((30, 40, 60))

        if (not game.invincible) or ((now // game.config.flash_interval_ms) % 2 == 0):
            pygame.draw.rect(surface, (80, 180, 240), game.player)

        pygame.draw.rect(surface, (255, 255, 0), game.star)

        for enemy in game.enemies:
            pygame.draw.rect(surface, (220, 50, 50), enemy.rect)

        for p in game.particles:
            current_size = max(1, int(p['size'] * (p['life'] / p['max_life'])))
            pygame.draw.circle(surface, p['color'], (int(p['x']), int(p['y'])), current_size)

        # HUD Text
        score_text = game.font.render(f'Score: {game.score}', True, (255, 255, 255))
        surface.blit(score_text, (20, 20))
        lives_text = game.font.render(f'Lives: {game.lives}', True, (255, 255, 255))
        surface.blit(lives_text, (20, 60))
        
        time_left = int(max(0, game.config.timer_seconds + game.timer_bonus - game.time_elapsed))
        timer_text = game.font.render(f'Time left: {time_left}', True, (255, 255, 255))
        surface.blit(timer_text, (game.config.screen_width - 240, 20))

        small_font = pygame.font.SysFont('Arial', 14, bold=True)
        if game.audio:
            if game.audio.muted_all:
                txt = small_font.render('AUDIO: MUTED (M)', True, (240, 100, 100))
                surface.blit(txt, (20, 100))
            elif game.audio.muted_music:
                txt = small_font.render('BGM: MUTED (B)', True, (240, 180, 100))
                surface.blit(txt, (20, 100))

        if game.dev_mode:
            dev_title = small_font.render('--- DEVELOPER MODE ACTIVE ---', True, (0, 255, 128))
            surface.blit(dev_title, (game.config.screen_width - 240, 60))
            god_status = 'ON (Press G)' if game.god_mode else 'OFF (Press G)'
            god_txt = small_font.render(f'God Mode: {god_status}', True, (0, 255, 128) if game.god_mode else (180, 180, 180))
            surface.blit(god_txt, (game.config.screen_width - 240, 80))
            enemies_txt = small_font.render(f'Enemies: {len(game.enemies)} (Press +/- to tune)', True, (180, 180, 180))
            surface.blit(enemies_txt, (game.config.screen_width - 240, 100))
            speed_txt = small_font.render(f'Player Speed: {game.config.player_speed} (Press [ / ])', True, (180, 180, 180))
            surface.blit(speed_txt, (game.config.screen_width - 240, 120))
            time_txt = small_font.render('Press T to Add 10 Seconds', True, (180, 180, 180))
            surface.blit(time_txt, (game.config.screen_width - 240, 140))
        else:
            dev_txt = small_font.render('Press F12 for Developer Tools', True, (120, 130, 150))
            surface.blit(dev_txt, (game.config.screen_width - 240, 60))


class PauseState(GameState):
    """Pause menu state overlaying the previous playing state."""
    def __init__(self, previous_state: GameState, is_collision_pause: bool = False) -> None:
        self.previous_state = previous_state
        self.is_collision_pause = is_collision_pause
        self.selected_idx = 0
        self.start_time = pygame.time.get_ticks()

    def handle_event(self, game: 'Game', event: pygame.event.Event) -> None:
        options = [
            {'id': 'continue', 'label': 'CONTINUE'},
            {'id': 'settings', 'label': 'SETTINGS'},
            {'id': 'quit', 'label': 'QUIT GAME'}
        ]

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_idx = (self.selected_idx - 1) % len(options)
                game.audio.play_menu_nav()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_idx = (self.selected_idx + 1) % len(options)
                game.audio.play_menu_nav()
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                game.audio.play_menu_nav()
                opt_id = options[self.selected_idx]['id']
                if opt_id == 'continue':
                    self._resume(game)
                elif opt_id == 'settings':
                    game.state = SettingsState(return_state=self)
                elif opt_id == 'quit':
                    game.running = False
            elif event.key in (pygame.K_c, pygame.K_ESCAPE):
                self._resume(game)
            elif event.key == pygame.K_m:
                game.audio.set_muted_all(not game.audio.muted_all)
                game.audio.play_menu_nav()
            elif event.key == pygame.K_b:
                game.audio.set_muted_music(not game.audio.muted_music)
                game.audio.play_menu_nav()
            elif event.key == pygame.K_q:
                game.running = False

    def _resume(self, game: 'Game') -> None:
        if self.is_collision_pause:
            game.player.x, game.player.y = 100, 100
            game.star.x = randint(50, game.config.screen_width - 50)
            game.star.y = randint(50, game.config.screen_height - 50)
            game.invincible = True
            game.invincible_end = pygame.time.get_ticks() + game.config.invincible_ms
        game.state = self.previous_state

    def update(self, game: 'Game', dt: float) -> None:
        # Keep background particles animating during pause
        active_particles = []
        for p in game.particles:
            p['x'] += p['dx'] * 60 * dt
            p['y'] += p['dy'] * 60 * dt
            p['dx'] *= math.pow(0.96, 60 * dt)
            p['dy'] *= math.pow(0.96, 60 * dt)
            p['life'] -= 60 * dt
            if p['life'] > 0:
                active_particles.append(p)
        game.particles = active_particles

    def render(self, game: 'Game', surface: pygame.Surface) -> None:
        self.previous_state.render(game, surface)

        now = pygame.time.get_ticks()
        elapsed = (now - self.start_time) / 1000.0

        options = [
            {'id': 'continue', 'label': 'CONTINUE'},
            {'id': 'settings', 'label': 'SETTINGS'},
            {'id': 'quit', 'label': 'QUIT GAME'}
        ]

        overlay = pygame.Surface((game.config.screen_width, game.config.screen_height), pygame.SRCALPHA)
        overlay.fill((10, 14, 26, 180))
        surface.blit(overlay, (0, 0))

        panel_w = 540
        panel_h = 320
        panel_x = (game.config.screen_width - panel_w) // 2
        panel_y = (game.config.screen_height - panel_h) // 2

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (15, 20, 35, 240), (0, 0, panel_w, panel_h), border_radius=16)
        
        pygame.draw.rect(panel, (0, 191, 255), (0, 0, panel_w, panel_h), width=4, border_radius=16)
        pygame.draw.rect(panel, (255, 20, 147), (5, 5, panel_w - 10, panel_h - 10), width=2, border_radius=12)

        title_font = pygame.font.SysFont('Arial', 38, bold=True)
        subtitle_font = pygame.font.SysFont('Arial', 18)
        option_font = pygame.font.SysFont('Arial', 22, bold=True)
        footer_font = pygame.font.SysFont('Arial', 14, bold=True)

        title = title_font.render('GAME PAUSED', True, (255, 215, 0))
        panel.blit(title, ((panel_w - title.get_width()) // 2, 22))

        sub = subtitle_font.render('Select action to resume:', True, (160, 185, 215))
        panel.blit(sub, ((panel_w - sub.get_width()) // 2, 68))

        start_y = 105
        row_gap = 40
        for idx, opt in enumerate(options):
            is_selected = (idx == self.selected_idx)
            if is_selected:
                text_color = (0, 255, 255)
                px = 140 + int(math.sin(elapsed * 10) * 4)
                py = start_y + idx * row_gap + 13
                points = [(px, py - 7), (px + 10, py), (px, py + 7)]
                pygame.draw.polygon(panel, (0, 255, 255), points)
            else:
                text_color = (150, 175, 205)

            opt_text = option_font.render(opt['label'], True, text_color)
            panel.blit(opt_text, (170, start_y + idx * row_gap))

        blink = int(elapsed * 2) % 2 == 0
        if blink:
            footer_text = footer_font.render('PRESS ENTER OR SPACE TO SELECT', True, (255, 20, 147))
        else:
            footer_text = footer_font.render('PRESS ESC OR C TO RESUME', True, (0, 255, 128))
        panel.blit(footer_text, ((panel_w - footer_text.get_width()) // 2, 275))

        surface.blit(panel, (panel_x, panel_y))


class GameOverState(GameState):
    """Game over / end screen state showing final results."""
    def __init__(self, message_text: str) -> None:
        self.message_text = message_text
        self.selected_idx = 0
        self.start_time = pygame.time.get_ticks()

    def handle_event(self, game: 'Game', event: pygame.event.Event) -> None:
        options = [
            {'id': 'restart', 'label': 'PLAY AGAIN'},
            {'id': 'quit', 'label': 'QUIT GAME'}
        ]

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_idx = (self.selected_idx - 1) % len(options)
                game.audio.play_menu_nav()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_idx = (self.selected_idx + 1) % len(options)
                game.audio.play_menu_nav()
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                game.audio.play_menu_nav()
                opt_id = options[self.selected_idx]['id']
                if opt_id == 'restart':
                    game.reset()
                    game.state = PlayingState()
                elif opt_id == 'quit':
                    game.running = False
            elif event.key == pygame.K_r:
                game.audio.play_menu_nav()
                game.reset()
                game.state = PlayingState()
            elif event.key == pygame.K_q:
                game.running = False

    def update(self, game: 'Game', dt: float) -> None:
        # Keep background particles animating during Game Over
        active_particles = []
        for p in game.particles:
            p['x'] += p['dx'] * 60 * dt
            p['y'] += p['dy'] * 60 * dt
            p['dx'] *= math.pow(0.96, 60 * dt)
            p['dy'] *= math.pow(0.96, 60 * dt)
            p['life'] -= 60 * dt
            if p['life'] > 0:
                active_particles.append(p)
        game.particles = active_particles

    def render(self, game: 'Game', surface: pygame.Surface) -> None:
        surface.fill((30, 40, 60))
        pygame.draw.rect(surface, (255, 255, 0), game.star)
        for enemy in game.enemies:
            pygame.draw.rect(surface, (220, 50, 50), enemy.rect)
        for p in game.particles:
            current_size = max(1, int(p['size'] * (p['life'] / p['max_life'])))
            pygame.draw.circle(surface, p['color'], (int(p['x']), int(p['y'])), current_size)

        now = pygame.time.get_ticks()
        elapsed = (now - self.start_time) / 1000.0

        overlay = pygame.Surface((game.config.screen_width, game.config.screen_height), pygame.SRCALPHA)
        overlay.fill((10, 14, 26, 200))
        surface.blit(overlay, (0, 0))

        panel_w = 500
        panel_h = 280
        panel_x = (game.config.screen_width - panel_w) // 2
        panel_y = (game.config.screen_height - panel_h) // 2

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (15, 20, 35, 240), (0, 0, panel_w, panel_h), border_radius=16)
        
        pygame.draw.rect(panel, (0, 191, 255), (0, 0, panel_w, panel_h), width=4, border_radius=16)
        pygame.draw.rect(panel, (255, 20, 147), (5, 5, panel_w - 10, panel_h - 10), width=2, border_radius=12)

        title_font = pygame.font.SysFont('Arial', 34, bold=True)
        subtitle_font = pygame.font.SysFont('Arial', 18)
        option_font = pygame.font.SysFont('Arial', 22, bold=True)
        footer_font = pygame.font.SysFont('Arial', 14, bold=True)

        is_time_up = 'TIME' in self.message_text.upper()
        title_color = (255, 215, 0) if is_time_up else (255, 90, 90)
        
        title_shadow = title_font.render(self.message_text.upper(), True, (60, 10, 10) if not is_time_up else (100, 75, 0))
        panel.blit(title_shadow, ((panel_w - title_shadow.get_width()) // 2 + 2, 22 + 2))
        
        title = title_font.render(self.message_text.upper(), True, title_color)
        panel.blit(title, ((panel_w - title.get_width()) // 2, 22))

        sub = subtitle_font.render('Game round concluded:', True, (160, 185, 215))
        panel.blit(sub, ((panel_w - sub.get_width()) // 2, 68))

        options = [
            {'id': 'restart', 'label': 'PLAY AGAIN'},
            {'id': 'quit', 'label': 'QUIT GAME'}
        ]
        start_y = 115
        row_gap = 42
        for idx, opt in enumerate(options):
            is_selected = (idx == self.selected_idx)
            if is_selected:
                text_color = (0, 255, 255)
                px = 120 + int(math.sin(elapsed * 10) * 4)
                py = start_y + idx * row_gap + 13
                points = [(px, py - 7), (px + 10, py), (px, py + 7)]
                pygame.draw.polygon(panel, (0, 255, 255), points)
            else:
                text_color = (150, 175, 205)

            opt_text = option_font.render(opt['label'], True, text_color)
            panel.blit(opt_text, (150, start_y + idx * row_gap))

        blink = int(elapsed * 2) % 2 == 0
        if blink:
            footer_text = footer_font.render('PRESS ENTER OR SPACE TO SELECT', True, (255, 20, 147))
        else:
            footer_text = footer_font.render('PRESS R TO RETRY | Q TO QUIT', True, (0, 255, 128))
        panel.blit(footer_text, ((panel_w - footer_text.get_width()) // 2, 235))

        surface.blit(panel, (panel_x, panel_y))


class Game:
    """Main game loop and state container for the demo."""

    def __init__(self) -> None:
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.config = GameConfig()
        self.screen = pygame.display.set_mode((self.config.screen_width, self.config.screen_height))
        pygame.display.set_caption('VS Code Pygame Demo')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.audio = AudioManager()
        self.audio.start_background_music()
        
        # Developer Mode parameters
        self.dev_mode = False
        self.god_mode = False
        self.state: GameState = StartMenuState()
        self.running = False
        
        self.reset()

    def reset(self) -> None:
        """Reset the game state so the player can start a fresh round."""
        self.score = 0
        self.lives = 3
        self.player = pygame.Rect(100, 100, self.config.player_width, self.config.player_height)
        self.star = pygame.Rect(
            randint(150, self.config.screen_width - 70),
            randint(150, self.config.screen_height - 70),
            20,
            20,
        )
        self.enemies = self._create_enemies()
        self.particles = []
        self.invincible = False
        self.invincible_end = 0
        self.time_elapsed = 0.0
        self.timer_bonus = 0.0

    def _create_enemies(self) -> list[Enemy]:
        """Create the enemy blocks for a new round."""
        enemies: list[Enemy] = []
        for index in range(self.config.enemy_count):
            x = randint(200, self.config.screen_width - 100)
            y = randint(50, self.config.screen_height - 100)
            speed = randint(2, 5)
            direction = 1 if index % 2 == 0 else -1
            enemies.append(Enemy(rect=pygame.Rect(x, y, 60, 60), speed=speed, direction=direction))
        return enemies

    def _flash_screen(self, color: tuple[int, int, int] = (255, 255, 255), duration_ms: int = 160) -> None:
        """Flash the screen with a color for a short duration to emphasize events (e.g., death)."""
        try:
            overlay = pygame.Surface((self.config.screen_width, self.config.screen_height))
            overlay.fill(color)
            overlay.set_alpha(200)
            self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            pygame.time.delay(duration_ms)
        except Exception:
            pass

    def _trigger_explosion(self, x: int, y: int) -> None:
        """Create a cluster of particle effects to simulate an explosion."""
        import random
        for _ in range(35):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            color = random.choice([
                (255, 69, 0),    # OrangeRed
                (255, 140, 0),   # DarkOrange
                (255, 215, 0),   # Gold
                (220, 20, 60)    # Crimson
            ])
            size = random.randint(3, 8)
            life = random.randint(20, 45)
            self.particles.append({
                'x': float(x),
                'y': float(y),
                'dx': dx,
                'dy': dy,
                'color': color,
                'size': size,
                'life': float(life),
                'max_life': float(life)
            })

    def _show_error_screen(self, error: Exception, tb_str: str) -> None:
        """Display an error boundary screen when an unhandled exception occurs."""
        log_file = os.path.join(script_dir, 'crash_log.txt')
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] CRASH REPORT:\nError: {type(error).__name__}: {error}\nTraceback:\n{tb_str}\n{'='*60}\n"

        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception:
            pass

        title_font = pygame.font.SysFont('Arial', 28, bold=True)
        sub_font = pygame.font.SysFont('Arial', 16)
        code_font = pygame.font.SysFont('Consolas', 14)

        panel_w, panel_h = 700, 420
        panel_x = (self.config.screen_width - panel_w) // 2
        panel_y = (self.config.screen_height - panel_h) // 2

        tb_lines = [line.strip() for line in tb_str.split('\n') if line.strip()][-6:]

        while True:
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.KEYDOWN):
                    return

            self.screen.fill((15, 10, 15))
            panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            pygame.draw.rect(panel, (30, 18, 22, 250), (0, 0, panel_w, panel_h), border_radius=12)
            pygame.draw.rect(panel, (220, 60, 60), (0, 0, panel_w, panel_h), width=2, border_radius=12)

            title = title_font.render('GAME ENCOUNTERED A PROBLEM', True, (255, 80, 80))
            panel.blit(title, (20, 20))

            desc = sub_font.render(f"Reason: {type(error).__name__} - {error}", True, (240, 210, 210))
            panel.blit(desc, (20, 60))

            log_lbl = sub_font.render(f"Saved to: crash_log.txt  |  Trace Details:", True, (180, 180, 180))
            panel.blit(log_lbl, (20, 95))

            pygame.draw.rect(panel, (18, 10, 12), (20, 125, panel_w - 40, 220), border_radius=6)
            for idx, line in enumerate(tb_lines):
                txt = code_font.render(line[:85], True, (230, 160, 160))
                panel.blit(txt, (30, 135 + idx * 30))

            close_hint = sub_font.render("Press any key or close window to exit...", True, (200, 200, 200))
            panel.blit(close_hint, ((panel_w - close_hint.get_width()) // 2, 370))

            self.screen.blit(panel, (panel_x, panel_y))
            pygame.display.flip()
            self.clock.tick(15)

    def run(self) -> None:
        """Run the main game loop wrapped in a crash error boundary."""
        import traceback
        try:
            self.state = StartMenuState()
            self.running = True
            while self.running:
                dt = min(0.1, self.clock.tick(60) / 1000.0)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                    self.state.handle_event(self, event)
                
                if not self.running:
                    break
                    
                self.state.update(self, dt)
                self.state.render(self, self.screen)
                pygame.display.flip()

        except Exception as e:
            tb_str = traceback.format_exc()
            print(f"\n[GAME CRASH DETECTED]\n{tb_str}", file=sys.stderr)
            try:
                self._show_error_screen(e, tb_str)
            except Exception:
                pass
        finally:
            pygame.quit()


if __name__ == '__main__':
    Game().run()
