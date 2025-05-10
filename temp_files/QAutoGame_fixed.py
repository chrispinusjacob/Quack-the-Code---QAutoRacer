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

#-------------------------------------------------------
# BUTTON CLASS
#-------------------------------------------------------
class Button:
    def __init__(self, x, y, width, height, text, font, 
                 text_color=WHITE,
                 bg_color=(0, 0, 0, 0),
                 hover_color=NEON_BLUE,
                 border_color=WHITE,
                 border_width=2,
                 sound_manager=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_width = border_width
        self.sound_manager = sound_manager
        
        self.rect = pygame.Rect(x, y, width, height)
        self.is_hovered = False
        self.was_hovered = False
        self.animation_time = 0
        
        # Pre-render text
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Play hover sound when first hovering
        if self.is_hovered and not self.was_hovered:
            if self.sound_manager:
                self.sound_manager.play("hover")
        
        # Update animation time
        self.animation_time += dt
    
    def draw(self, surface):
        # Create button surface with transparency
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Determine colors based on hover state
        if self.is_hovered:
            # Pulsating effect when hovered
            pulse = math.sin(self.animation_time * 5) * 0.2 + 0.8
            hover_color = [min(255, c * pulse) for c in self.hover_color]
            
            # Draw background with hover color
            pygame.draw.rect(button_surface, (*hover_color, 150), 
                           (0, 0, self.width, self.height), 0, 10)
            
            # Draw border with glow effect
            for i in range(3, 0, -1):
                alpha = 100 if i == 1 else 50
                pygame.draw.rect(button_surface, (*self.border_color, alpha),
                               (0-i, 0-i, self.width+i*2, self.height+i*2), 
                               self.border_width, 10+i)
        else:
            # Draw normal background
            pygame.draw.rect(button_surface, self.bg_color, 
                           (0, 0, self.width, self.height), 0, 10)
        
        # Always draw border
        pygame.draw.rect(button_surface, self.border_color, 
                       (0, 0, self.width, self.height), 
                       self.border_width, 10)
        
        # Blit button to surface
        surface.blit(button_surface, (self.x, self.y))
        
        # Draw text
        surface.blit(self.text_surface, self.text_rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.sound_manager:
                    self.sound_manager.play("click")
                return True
        return False