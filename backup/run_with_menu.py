import pygame
import sys
import math
import random
import os
import json
from pygame.locals import *
from config import *  # Import all constants and configurations

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game states
STATE_MAIN_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_PAUSED = 3
STATE_SETTINGS = 4
STATE_HIGH_SCORES = 5
STATE_INSTRUCTIONS = 6

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

# Simple Button class
class SimpleButton:
    def __init__(self, x, y, width, height, text, color=NEON_BLUE, hover_color=NEON_PINK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface, font):
        # Draw button with hover effect
        color = self.hover_color if self.is_hovered else self.color
        
        # Main button
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=5)  # Border
        
        # Button text
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos):
        # Check if hover state changed
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        # Check if button was clicked
        return self.rect.collidepoint(mouse_pos) and mouse_click

# Get font function
def get_font(size):
    try:
        return pygame.font.Font(os.path.join(FONT_DIR, "pixel.ttf"), size)
    except:
        return pygame.font.SysFont("Arial", size)

# Load sounds
try:
    engine_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "engine.mp3"))
    crash_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "crash.mp3"))
    pickup_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "score.mp3"))
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

# Create menu buttons
def create_main_menu_buttons():
    button_width = 200
    button_height = 50
    button_spacing = 20
    start_y = SCREEN_HEIGHT // 3
    
    buttons = {
        "start": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y,
            button_width, button_height,
            "START GAME", NEON_GREEN
        ),
        "settings": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + button_height + button_spacing,
            button_width, button_height,
            "SETTINGS", NEON_BLUE
        ),
        "high_scores": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + (button_height + button_spacing) * 2,
            button_width, button_height,
            "HIGH SCORES", NEON_PURPLE
        ),
        "instructions": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + (button_height + button_spacing) * 3,
            button_width, button_height,
            "INSTRUCTIONS", NEON_YELLOW
        ),
        "exit": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + (button_height + button_spacing) * 4,
            button_width, button_height,
            "EXIT", NEON_ORANGE
        )
    }
    
    return buttons

def create_pause_menu_buttons():
    button_width = 200
    button_height = 50
    button_spacing = 20
    start_y = SCREEN_HEIGHT // 3
    
    buttons = {
        "resume": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y,
            button_width, button_height,
            "RESUME", NEON_GREEN
        ),
        "restart": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + button_height + button_spacing,
            button_width, button_height,
            "RESTART", NEON_BLUE
        ),
        "main_menu": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + (button_height + button_spacing) * 2,
            button_width, button_height,
            "MAIN MENU", NEON_PURPLE
        ),
        "quit": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + (button_height + button_spacing) * 3,
            button_width, button_height,
            "QUIT GAME", NEON_ORANGE
        )
    }
    
    return buttons