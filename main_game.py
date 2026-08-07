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

    def _load_sounds(self) -> None:
        try:
            self.collect_sound = self._make_sound(880, 120, 0.5)
            self.hit_sound = self._make_sound(220, 180, 0.7)
            self.game_over_sound = self._make_sound(110, 250, 0.7)
            # Distinct death sound played when the player loses their last life
            # tuned death sound: lower pitch and longer duration for impact
            self.death_sound = self._make_sound(100, 700, 1.0)
            self.restart_sound = self._make_sound(660, 120, 0.5)
            # small navigation/click sound for end-screen choices
            self.menu_nav = self._make_sound(1200, 70, 0.6)
            self.background_music = self._make_background_music()
            self.movement_loop = self._make_movement_sound()
            self.background_channel = pygame.mixer.Channel(0)
            self.movement_channel = pygame.mixer.Channel(1)
            # track mute state and default volumes
            self.muted = False
            self._background_vol = 1.0
            self._movement_vol = 1.0
            self.music_enabled = True
        except pygame.error:
            self.music_enabled = False

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

    def start_background_music(self) -> None:
        if self.music_enabled and not self.muted:
            self.background_channel.play(self.background_music, loops=-1)

    def set_muted(self, muted: bool) -> None:
        """Mute or unmute all audio managed here."""
        if not self.music_enabled:
            return
        self.muted = bool(muted)
        try:
            if self.muted:
                # pause background and stop movement loop
                self.background_channel.set_volume(0.0)
                self.movement_channel.set_volume(0.0)
                if self.movement_channel.get_busy():
                    self.movement_channel.stop()
            else:
                self.background_channel.set_volume(self._background_vol)
                self.movement_channel.set_volume(self._movement_vol)
                # ensure background is playing
                if not self.background_channel.get_busy():
                    self.background_channel.play(self.background_music, loops=-1)
        except Exception:
            pass

    def play_collect(self) -> None:
        if self.music_enabled:
            self.collect_sound.play()

    def play_hit(self) -> None:
        if self.music_enabled:
            self.hit_sound.play()

    def play_game_over(self) -> None:
        if self.music_enabled:
            self.game_over_sound.play()

    def play_death(self) -> None:
        """Play the death sound (used when the player loses their last life)."""
        if self.music_enabled:
            # play immediately
            self.death_sound.play()

    def play_menu_nav(self) -> None:
        """Play a small nav/click sound when the user moves or selects in menus."""
        if self.music_enabled and hasattr(self, 'menu_nav'):
            self.menu_nav.play()

    def play_restart(self) -> None:
        if self.music_enabled:
            self.restart_sound.play()

    def update_movement_audio(self, is_moving: bool) -> None:
        if not self.music_enabled or self.muted:
            return
        if is_moving and not self.movement_channel.get_busy():
            self.movement_channel.play(self.movement_loop, loops=-1)
        elif not is_moving and self.movement_channel.get_busy():
            self.movement_channel.stop()


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
        self.invincible = False
        self.invincible_end = 0
        self.start_ticks = pygame.time.get_ticks()

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

    def _move_player(self, keys: pygame.key.ScancodeWrapper) -> bool:
        """Move the player based on the currently pressed keys."""
        is_moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= self.config.player_speed
            is_moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += self.config.player_speed
            is_moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.y -= self.config.player_speed
            is_moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.y += self.config.player_speed
            is_moving = True

        self.player.clamp_ip(pygame.Rect(0, 0, self.config.screen_width, self.config.screen_height))
        return is_moving

    def _update_enemies(self) -> None:
        """Move each enemy and bounce them off the screen edges."""
        for enemy in self.enemies:
            enemy.rect.x += enemy.speed * enemy.direction
            if enemy.rect.left < 0 or enemy.rect.right > self.config.screen_width:
                enemy.direction *= -1
                enemy.rect.x += enemy.speed * enemy.direction * 2

    def _collect_star(self) -> None:
        """Increase score when the player collects the star."""
        if self.player.colliderect(self.star):
            self.score += 1
            self.audio.play_collect()
            self.star.x = randint(50, self.config.screen_width - 50)
            self.star.y = randint(50, self.config.screen_height - 50)

    def _update_invincibility(self, now: int) -> None:
        if self.invincible and now > self.invincible_end:
            self.invincible = False

    def _show_message(self, message_text: str, color: tuple[int, int, int], delay_ms: int = 1000) -> None:
        message = self.font.render(message_text, True, color)
        self.screen.fill((20, 20, 40))
        self.screen.blit(message, (self.config.screen_width // 2 - message.get_width() // 2, self.config.screen_height // 2 - 20))
        pygame.display.flip()
        pygame.time.delay(delay_ms)

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
            # If anything goes wrong with the visual effect, silently ignore it.
            pass

    def _handle_enemy_collision(self, now: int) -> str | None:
        if self.invincible:
            return None
        if not any(self.player.colliderect(enemy.rect) for enemy in self.enemies):
            return None

        self.lives -= 1
        self.audio.play_hit()
        if self.lives > 0:
            # play hit sound and show a pause menu so the user can choose what to do
            self.audio.play_hit()
            action = self._show_pause_menu()
            if action == 'continue':
                # respawn
                self.player.x, self.player.y = 100, 100
                self.star.x = randint(50, self.config.screen_width - 50)
                self.star.y = randint(50, self.config.screen_height - 50)
                self.invincible = True
                self.invincible_end = now + self.config.invincible_ms
                return 'respawn'
            else:
                # treat as quit
                self.audio.play_game_over()
                return 'game_over'

        # Play a death sound then indicate game over
        self.audio.play_death()
        self._flash_screen()
        return 'game_over'

    def _show_pause_menu(self) -> str:
        """Show a pause menu when the player is hit with options:
        Continue (C), Toggle Mute (M), Quit (Q).
        Returns 'continue' or 'quit'. M toggles mute and keeps the menu open."""
        pygame.time.delay(100)
        prompt = 'You were hit! Press C to continue, M to toggle mute, or Q to quit.'
        # modal styling
        panel_w = 680
        panel_h = 200
        panel_x = (self.config.screen_width - panel_w) // 2
        panel_y = (self.config.screen_height - panel_h) // 2
        title_font = pygame.font.SysFont(None, 44)
        small_font = pygame.font.SysFont(None, 28)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    # play small nav sound for feedback
                    if self.audio:
                        self.audio.play_menu_nav()
                    if event.key == pygame.K_c:
                        return 'continue'
                    if event.key == pygame.K_m:
                        # toggle mute but remain in the menu
                        if self.audio:
                            self.audio.set_muted(not self.audio.muted)
                        continue
                    if event.key == pygame.K_q:
                        return 'quit'
            # draw semi-opaque overlay
            overlay = pygame.Surface((self.config.screen_width, self.config.screen_height))
            overlay.fill((10, 10, 14))
            overlay.set_alpha(190)
            self.screen.blit(overlay, (0, 0))
            # panel with shadow
            shadow = pygame.Surface((panel_w + 8, panel_h + 8))
            shadow.fill((0, 0, 0))
            shadow.set_alpha(120)
            self.screen.blit(shadow, (panel_x + 6, panel_y + 6))
            panel = pygame.Surface((panel_w, panel_h))
            panel.fill((30, 36, 48))
            # panel border
            pygame.draw.rect(panel, (60, 70, 90), panel.get_rect(), 2)
            # title
            title = title_font.render('You were hit!', True, (240, 240, 240))
            panel.blit(title, (20, 12))
            # instruction
            instruction = small_font.render('Press C to continue, M to toggle mute, or Q to quit', True, (200, 200, 200))
            panel.blit(instruction, (20, 60))
            # draw buttons
            btn_x = (panel_w - 220) // 2
            btn_y = 100
            # continue button
            pygame.draw.rect(panel, (80, 180, 240), (btn_x, btn_y, 60, 60))
            pygame.draw.rect(panel, (60, 150, 210), (btn_x, btn_y, 60, 60), 2)
            c_label = title_font.render('C', True, (8, 10, 14))
            panel.blit(c_label, (btn_x + 18, btn_y + 6))
            # mute button
            pygame.draw.rect(panel, (140, 255, 140) if not (self.audio and getattr(self.audio, 'muted', False)) else (180, 120, 120), (btn_x + 80, btn_y, 60, 60))
            pygame.draw.rect(panel, (100, 220, 100), (btn_x + 80, btn_y, 60, 60), 2)
            m_label = title_font.render('M', True, (8, 10, 14))
            panel.blit(m_label, (btn_x + 98, btn_y + 6))
            # quit button
            pygame.draw.rect(panel, (220, 50, 50), (btn_x + 160, btn_y, 60, 60))
            pygame.draw.rect(panel, (180, 40, 40), (btn_x + 160, btn_y, 60, 60), 2)
            q_label = title_font.render('Q', True, (8, 10, 14))
            panel.blit(q_label, (btn_x + 178, btn_y + 6))
            # labels
            lbl_continue = small_font.render('Continue', True, (200, 200, 200))
            lbl_mute = small_font.render('Toggle Mute', True, (200, 200, 200))
            lbl_quit = small_font.render('Quit', True, (200, 200, 200))
            panel.blit(lbl_continue, (btn_x, btn_y + 66))
            panel.blit(lbl_mute, (btn_x + 80, btn_y + 66))
            panel.blit(lbl_quit, (btn_x + 160, btn_y + 66))
            # mute indicator on panel
            if self.audio and getattr(self.audio, 'muted', False):
                muted_lbl = small_font.render('Muted', True, (240, 140, 140))
                panel.blit(muted_lbl, (panel_w - 110, 16))
            # blit panel
            self.screen.blit(panel, (panel_x, panel_y))
            pygame.display.flip()
            self.clock.tick(30)

    def _show_end_screen(self, message_text: str) -> str:
        """Show a restart/quit prompt after the game ends."""
        pygame.time.delay(200)
        prompt = message_text + '  Press R to try again or Q to quit.'
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    # play small nav sound for feedback
                    self.audio.play_menu_nav()
                    if event.key == pygame.K_r:
                        return 'restart'
                    if event.key == pygame.K_q:
                        return 'quit'
            # draw menu with simple option icons
            self.screen.fill((20, 20, 40))
            text = self.font.render(prompt, True, (255, 255, 255))
            self.screen.blit(text, (self.config.screen_width // 2 - text.get_width() // 2, self.config.screen_height // 2 - 20))
            # small icons
            pygame.draw.rect(self.screen, (80, 180, 240), (self.config.screen_width//2 - 140, self.config.screen_height//2 + 40, 40, 40))
            pygame.draw.rect(self.screen, (140, 255, 140), (self.config.screen_width//2 - 60, self.config.screen_height//2 + 40, 40, 40))
            pygame.draw.rect(self.screen, (220, 50, 50), (self.config.screen_width//2 + 20, self.config.screen_height//2 + 40, 40, 40))
            pygame.display.flip()
            self.clock.tick(15)

    def _draw(self, now: int) -> None:
        """Render the current frame of the game."""
        self.screen.fill((30, 40, 60))
        if (not self.invincible) or ((now // self.config.flash_interval_ms) % 2 == 0):
            pygame.draw.rect(self.screen, (80, 180, 240), self.player)
        pygame.draw.rect(self.screen, (255, 255, 0), self.star)
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, (220, 50, 50), enemy.rect)

        # HUD
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))
        lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(lives_text, (20, 60))
        time_left = self._time_left(now)
        timer_text = self.font.render(f'Time left: {time_left}', True, (255, 255, 255))
        self.screen.blit(timer_text, (self.config.screen_width - 240, 20))

        # small settings indicator (muted) as an icon
        if self.audio:
            if getattr(self.audio, 'muted', False):
                # muted icon (simple speaker with X)
                pygame.draw.polygon(self.screen, (200,200,200), [(18,110),(34,102),(34,118)])
                x1,x2=40,52
                pygame.draw.line(self.screen,(200,50,50),(x1,105),(x2,125),3)
                pygame.draw.line(self.screen,(200,50,50),(x1,125),(x2,105),3)
            else:
                # speaker icon (unmuted)
                pygame.draw.polygon(self.screen, (200,200,200), [(18,110),(34,102),(34,118)])
                pygame.draw.arc(self.screen, (180,220,180), (36,100,18,20), 3.9, 5.5, 2)

        pygame.display.flip()

    def _time_left(self, now: int) -> int:
        return max(0, self.config.timer_seconds - (now - self.start_ticks) // 1000)

    def run(self) -> None:
        """Run the main game loop until the player quits or ends the game."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            if not running:
                break

            keys = pygame.key.get_pressed()
            now = pygame.time.get_ticks()
            self._update_invincibility(now)

            is_moving = self._move_player(keys)
            self.audio.update_movement_audio(is_moving)
            self._update_enemies()
            self._collect_star()

            collision_result = self._handle_enemy_collision(now)
            if collision_result == 'respawn':
                continue
            if collision_result == 'game_over':
                action = self._show_end_screen('Game Over! No lives left.')
                if action == 'restart':
                    self.audio.play_restart()
                    self.reset()
                    continue
                running = False
                break

            self._draw(now)
            if self._time_left(now) == 0:
                # Play a death and flash effect then indicate game over
                self.audio.play_death()
                # brief screen flash to emphasize death
                self._flash_screen()
                action = self._show_end_screen('Time up! Well done.')
                if action == 'restart':
                    self.audio.play_restart()
                    self.reset()
                    continue
                running = False
                break

            self.clock.tick(60)

        pygame.quit()


if __name__ == '__main__':
    Game().run()
