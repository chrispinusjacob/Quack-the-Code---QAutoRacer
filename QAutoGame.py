import pygame
import sys
import os
import math
import random
import json
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "QAutoGame"
# Copyright 2025 by Chrispinus Jacob
# Powered by Amazon Q

# Game speeds - Adding these constants to fix the error
PLAYER_SPEED = 5
INITIAL_ENEMY_SPEED = 3
INITIAL_SCROLL_SPEED = 5

# Neon 80s color palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (0, 191, 255)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (138, 43, 226)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)
NEON_CYAN = (0, 255, 255)

# Game settings
ROAD_WIDTH = 400
LANE_COUNT = 3
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")
FONT_DIR = os.path.join(ASSET_DIR, "fonts")
SPRITE_DIR = os.path.join(ASSET_DIR, "sprites")

# Create directories if they don't exist
os.makedirs(SOUND_DIR, exist_ok=True)
os.makedirs(FONT_DIR, exist_ok=True)
os.makedirs(SPRITE_DIR, exist_ok=True)

# Create pixel fonts
def get_font(size):
    try:
        return pygame.font.Font(os.path.join(FONT_DIR, "pixel.ttf"), size)
    except:
        return pygame.font.SysFont("Arial", size)