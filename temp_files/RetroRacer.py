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
TITLE = "QAutoGame '90"

# Game speeds
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

#-------------------------------------------------------
# SOUND MANAGER
#-------------------------------------------------------
class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.sound_enabled = True
        self.music_enabled = True
        self.volume = 0.7
        self.music_volume = 0.5
        
        # Load sounds
        self.load_sounds()
    
    def load_sounds(self):
        sound_files = {
            "engine": "engine.mp3",
            "crash": "crash.mp3",
            "pickup": "score.mp3",
            "click": "click.mp3",
            "hover": "hover.mp3"
        }
        
        for sound_name, filename in sound_files.items():
            filepath = os.path.join(SOUND_DIR, filename)
            try:
                if os.path.exists(filepath):
                    self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                    self.sounds[sound_name].set_volume(self.volume)
            except:
                print(f"Could not load sound: {filepath}")
    
    def play(self, sound_name, loops=0):
        if not self.sound_enabled:
            return
            
        if sound_name in self.sounds:
            self.sounds[sound_name].play(loops)
    
    def stop(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
    
    def stop_all(self):
        pygame.mixer.stop()
    
    def play_music(self, filename):
        if not self.music_enabled:
            return
            
        filepath = os.path.join(SOUND_DIR, filename)
        if os.path.exists(filepath):
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
            self.music_playing = True
    
    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False
    
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        if not self.sound_enabled:
            self.stop_all()
        return self.sound_enabled
    
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if not self.music_enabled and self.music_playing:
            self.stop_music()
        return self.music_enabled