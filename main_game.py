# Simple pygame demo: avoid moving enemies and collect stars
import os
import sys
import struct
import math
from random import randint

# Remove the script directory from sys.path to avoid importing a local pygame.py file
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)

import pygame

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('VS Code Pygame Demo')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

player = pygame.Rect(100, 100, 50, 50)
player_speed = 6

enemies = []
for i in range(5):
    x = randint(200, SCREEN_WIDTH - 100)
    y = randint(50, SCREEN_HEIGHT - 100)
    speed = randint(2, 5)
    direction = 1 if i % 2 == 0 else -1
    enemies.append({'rect': pygame.Rect(x, y, 60, 60), 'speed': speed, 'dir': direction})

star = pygame.Rect(randint(150, SCREEN_WIDTH - 70), randint(150, SCREEN_HEIGHT - 70), 20, 20)
score = 0
lives = 3
# Invincibility after respawn (ms)
invincible = False
invincible_end = 0
INVINCIBLE_MS = 2000
FLASH_INTERVAL = 150
running = True
start_ticks = pygame.time.get_ticks()

# Build a small procedural sound effect using raw PCM samples
# This avoids requiring separate sound asset files.
def make_sound(frequency, duration_ms=150, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buffer = bytearray()
    for i in range(n_samples):
        value = int(32767 * volume * math.sin(2 * math.pi * frequency * i / sample_rate))
        buffer.extend(struct.pack('<h', value))
    return pygame.mixer.Sound(buffer=bytes(buffer))

collect_sound = make_sound(880, 120, 0.5)
hit_sound = make_sound(220, 180, 0.7)
game_over_sound = make_sound(110, 250, 0.7)
restart_sound = make_sound(660, 120, 0.5)

# Generate a simple looping background melody using sine waves.
def make_background_music(loop_seconds=2.2, volume=0.18):
    sample_rate = 44100
    total_samples = int(sample_rate * loop_seconds)
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
        for i in range(note_samples):
            t = i / sample_rate
            primary = math.sin(2 * math.pi * note_freq * t)
            bass = 0.35 * math.sin(2 * math.pi * (note_freq * 0.5) * t)
            # Gentle fade in/out to avoid clicks.
            fade = min(i / (sample_rate * 0.03), 1.0)
            fade = min(fade, 1.0 - ((i - (note_samples - int(sample_rate * 0.03))) / (sample_rate * 0.03)) if i > note_samples - int(sample_rate * 0.03) else 1.0)
            sample = int(32767 * volume * fade * (0.75 * primary + 0.25 * bass))
            buffer.extend(struct.pack('<h', sample))
    # Repeat the generated loop so the audio can be played indefinitely.
    while len(buffer) < total_samples * 2:
        buffer.extend(buffer)
    return pygame.mixer.Sound(buffer=bytes(buffer[:total_samples * 2]))

# A looping movement sound that plays while the player is moving.
def make_movement_sound(volume=0.12):
    return make_sound(720, 120, volume)

background_music = None
movement_loop = None
background_channel = None
movement_channel = None
music_enabled = False

try:
    background_music = make_background_music()
    movement_loop = make_movement_sound()
    background_channel = pygame.mixer.Channel(0)
    movement_channel = pygame.mixer.Channel(1)
    music_enabled = True
except pygame.error:
    music_enabled = False

if music_enabled:
    background_channel.play(background_music, loops=-1)

# Helper to reset the game state for a fresh try
def reset_game():
    global score, lives, player, star, enemies, start_ticks, invincible, invincible_end
    score = 0
    lives = 3
    player.x, player.y = 100, 100
    star.x = randint(150, SCREEN_WIDTH - 70)
    star.y = randint(150, SCREEN_HEIGHT - 70)
    # Reposition enemies
    enemies.clear()
    for i in range(5):
        x = randint(200, SCREEN_WIDTH - 100)
        y = randint(50, SCREEN_HEIGHT - 100)
        speed = randint(2, 5)
        direction = 1 if i % 2 == 0 else -1
        enemies.append({'rect': pygame.Rect(x, y, 60, 60), 'speed': speed, 'dir': direction})
    invincible = False
    invincible_end = 0
    start_ticks = pygame.time.get_ticks()

# End-screen that allows the player to restart (R) or quit (Q)
def end_screen(message_text):
    # Short delay so any previous flip is visible
    pygame.time.delay(200)
    prompt = message_text + '  Press R to try again or Q to quit.'
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'restart'
                if event.key == pygame.K_q:
                    return 'quit'
        screen.fill((20, 20, 40))
        msg = font.render(prompt, True, (255, 255, 255))
        screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        pygame.display.flip()
        clock.tick(15)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    now = pygame.time.get_ticks()
    # turn off invincibility when the timer expires
    if invincible and now > invincible_end:
        invincible = False
    is_moving = False
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= player_speed
        is_moving = True
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += player_speed
        is_moving = True
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= player_speed
        is_moving = True
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += player_speed
        is_moving = True

    player.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    if music_enabled:
        if is_moving and not movement_channel.get_busy():
            movement_channel.play(movement_loop, loops=-1)
        elif not is_moving and movement_channel.get_busy():
            movement_channel.stop()

    for enemy in enemies:
        enemy['rect'].x += enemy['speed'] * enemy['dir']
        if enemy['rect'].left < 0 or enemy['rect'].right > SCREEN_WIDTH:
            enemy['dir'] *= -1
            enemy['rect'].x += enemy['speed'] * enemy['dir'] * 2

    if player.colliderect(star):
        score += 1
        collect_sound.play()
        star.x = randint(50, SCREEN_WIDTH - 50)
        star.y = randint(50, SCREEN_HEIGHT - 50)

    # Only check collisions when not invincible
    if (not invincible) and any(player.colliderect(enemy['rect']) for enemy in enemies):
        lives -= 1
        hit_sound.play()
        if lives > 0:
            # Show hit message, respawn player and continue
            message = font.render('Hit! Respawning...', True, (255, 180, 50))
            screen.fill((20, 20, 40))
            screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
            pygame.display.flip()
            pygame.time.delay(1000)
            # Reset player position
            player.x, player.y = 100, 100
            # Reposition the star so player doesn't immediately collect it
            star.x = randint(50, SCREEN_WIDTH - 50)
            star.y = randint(50, SCREEN_HEIGHT - 50)
            # Enable brief invincibility after respawn
            invincible = True
            invincible_end = now + INVINCIBLE_MS
            continue
        else:
            game_over_sound.play()
            result = end_screen('Game Over! No lives left.')
            if result == 'restart':
                restart_sound.play()
                reset_game()
                continue
            else:
                running = False
                break

    screen.fill((30, 40, 60))
    # Flash the player while invincible
    if (not invincible) or ((now // FLASH_INTERVAL) % 2 == 0):
        pygame.draw.rect(screen, (80, 180, 240), player)
    pygame.draw.rect(screen, (255, 255, 0), star)
    for enemy in enemies:
        pygame.draw.rect(screen, (220, 50, 50), enemy['rect'])

    text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text, (20, 20))
    lives_text = font.render(f'Lives: {lives}', True, (255, 255, 255))
    screen.blit(lives_text, (20, 60))
    time_left = max(0, 30 - (now - start_ticks) // 1000)
    timer_text = font.render(f'Time left: {time_left}', True, (255, 255, 255))
    screen.blit(timer_text, (SCREEN_WIDTH - 240, 20))

    if time_left == 0:
        game_over_sound.play()
        result = end_screen('Time up! Well done.')
        if result == 'restart':
            restart_sound.play()
            reset_game()
            continue
        else:
            running = False
            break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()