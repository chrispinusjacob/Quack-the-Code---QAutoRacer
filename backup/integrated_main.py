import pygame
import sys
import math
import random
import os
import json
from pygame.locals import *
from config import *  # Import all constants and configurations

# Game states
STATE_MAIN_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_PAUSED = 3
STATE_SETTINGS = 4
STATE_HIGH_SCORES = 5
STATE_INSTRUCTIONS = 6

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("QAutoGame '90")
clock = pygame.time.Clock()

# Asset paths
FONT_DIR = os.path.join(ASSET_DIR, "fonts")
SPRITE_DIR = os.path.join(ASSET_DIR, "sprites")

# Create directories if they don't exist
os.makedirs(FONT_DIR, exist_ok=True)
os.makedirs(SPRITE_DIR, exist_ok=True)

# Create pixel fonts
def get_font(size):
    try:
        return pygame.font.Font(os.path.join(FONT_DIR, "pixel.ttf"), size)
    except:
        return pygame.font.SysFont("Arial", size)

# Load or create sounds
try:
    engine_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "engine.mp3"))
    crash_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "crash.mp3"))
    pickup_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "score.mp3"))
    click_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "click.mp3"))
    hover_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "hover.mp3"))
    menu_music = pygame.mixer.Sound(os.path.join(SOUND_DIR, "menu_music.mp3"))
    has_sound = True
except:
    has_sound = False
    print("Sound files not found. Creating placeholder sounds.")
    
    # Create simple sounds
    engine_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(
        pygame.surfarray.array3d(pygame.Surface((10, 10)))))
    crash_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(
        pygame.surfarray.array3d(pygame.Surface((10, 10)))))
    pickup_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(
        pygame.surfarray.array3d(pygame.Surface((10, 10)))))
    click_sound = engine_sound
    hover_sound = engine_sound
    menu_music = engine_sound