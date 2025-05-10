import pygame
import sys
import math
import random
import os
import json
from pygame.locals import *
from config import *

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

# Additional colors
NEON_CYAN = (0, 255, 255)

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

# Game settings
ROAD_WIDTH = 400
LANE_COUNT = 3
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT
PLAYER_SPEED = 8
INITIAL_ENEMY_SPEED = 3
INITIAL_SCROLL_SPEED = 5
SPEED_INCREASE_RATE = 0.0001
ORB_SPAWN_RATE = 0.02
ENEMY_SPAWN_RATE = 0.03

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
    
    # Create simple sounds using empty sounds
    engine_sound = pygame.mixer.Sound(buffer=bytes([0]*44))
    crash_sound = pygame.mixer.Sound(buffer=bytes([0]*44))
    pickup_sound = pygame.mixer.Sound(buffer=bytes([0]*44))

# Helper functions for game objects
def create_car_sprite(color, width=40, height=60):
    """Create a simple pixel art car sprite"""
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Main body
    pygame.draw.rect(sprite, color, (5, 10, width-10, height-20))
    
    # Top part (cabin)
    pygame.draw.rect(sprite, color, (10, 5, width-20, 10))
    
    # Wheels
    wheel_color = (30, 30, 30)
    pygame.draw.rect(sprite, wheel_color, (2, 15, 6, 12))
    pygame.draw.rect(sprite, wheel_color, (width-8, 15, 6, 12))
    pygame.draw.rect(sprite, wheel_color, (2, height-27, 6, 12))
    pygame.draw.rect(sprite, wheel_color, (width-8, height-27, 6, 12))
    
    # Windshield
    pygame.draw.rect(sprite, (100, 200, 255), (12, 12, width-24, 8))
    
    # Headlights
    pygame.draw.rect(sprite, (255, 255, 200), (8, 5, 6, 4))
    pygame.draw.rect(sprite, (255, 255, 200), (width-14, 5, 6, 4))
    
    # Taillights
    pygame.draw.rect(sprite, (255, 0, 0), (8, height-9, 6, 4))
    pygame.draw.rect(sprite, (255, 0, 0), (width-14, height-9, 6, 4))
    
    return sprite

def create_orb_sprite(radius=15):
    """Create a glowing orb sprite"""
    size = radius * 2
    sprite = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Create glow effect with multiple circles
    for r in range(radius, 0, -2):
        alpha = 255 if r == radius else int(255 * (r / radius))
        color = (0, 255, 255, alpha)  # NEON_CYAN with alpha
        pygame.draw.circle(sprite, color, (radius, radius), r)
    
    return sprite

def create_road_segment(width, height):
    """Create a road segment with lane markings"""
    segment = pygame.Surface((width, height))
    segment.fill((50, 50, 50))  # Dark gray road
    
    # Add lane markings
    lane_width = width // LANE_COUNT
    for lane in range(1, LANE_COUNT):
        x = lane * lane_width
        pygame.draw.line(segment, (255, 255, 255), (x, 0), (x, height), 2)
    
    return segment

def create_stripe(width, height):
    """Create a road stripe for the sides"""
    stripe = pygame.Surface((width, height))
    stripe.fill((255, 255, 255))
    return stripe

# Game classes
class Car:
    def __init__(self, x, y, color=NEON_BLUE, is_player=False):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.color = color
        self.is_player = is_player
        self.speed = PLAYER_SPEED if is_player else INITIAL_ENEMY_SPEED
        self.sprite = create_car_sprite(color, self.width, self.height)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Animation variables
        self.frame = 0
        self.exhaust_particles = []
    
    def update(self, dt=1.0):
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Add exhaust particles for player
        if self.is_player and random.random() < 0.2:
            self.exhaust_particles.append({
                'x': self.x + self.width // 2,
                'y': self.y + self.height,
                'size': random.uniform(2, 5),
                'life': random.randint(10, 20),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(1, 2)
            })
        
        # Update exhaust particles
        new_particles = []
        for p in self.exhaust_particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1
            p['size'] *= 0.9
            
            if p['life'] > 0 and p['size'] > 0.5:
                new_particles.append(p)
        
        self.exhaust_particles = new_particles
        
        # Animation frame
        self.frame += 1
    
    def draw(self, surface):
        # Draw exhaust particles
        for p in self.exhaust_particles:
            alpha = min(255, int(p['life'] * 10))
            pygame.draw.circle(surface, (100, 100, 100, alpha), 
                             (int(p['x']), int(p['y'])), 
                             int(p['size']))
        
        # Draw car with slight animation
        y_offset = math.sin(self.frame * 0.2) * 2 if self.is_player else 0
        surface.blit(self.sprite, (self.x, self.y + y_offset))
        
        # Draw headlight glow for player
        if self.is_player:
            glow_size = 10 + math.sin(self.frame * 0.1) * 2
            glow_surf = pygame.Surface((int(glow_size*2), int(glow_size*2)), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 200, 50), (int(glow_size), int(glow_size)), int(glow_size))
            surface.blit(glow_surf, (self.x + 8 - glow_size, self.y + 5 - glow_size))
            surface.blit(glow_surf, (self.x + self.width - 8 - glow_size, self.y + 5 - glow_size))

class Orb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.sprite = create_orb_sprite(self.radius)
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius*2, self.radius*2)
        self.collected = False
        
        # Animation variables
        self.frame = random.randint(0, 100)
    
    def update(self, scroll_speed):
        self.y += scroll_speed
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius
        self.frame += 1
    
    def draw(self, surface):
        # Pulsating effect
        scale = 1.0 + math.sin(self.frame * 0.1) * 0.2
        scaled_sprite = pygame.transform.scale(
            self.sprite, 
            (int(self.radius*2*scale), int(self.radius*2*scale))
        )
        surface.blit(
            scaled_sprite, 
            (self.x - int(self.radius*scale), self.y - int(self.radius*scale))
        )

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

# Draw main menu
def draw_main_menu(buttons, game_time):
    # Fill background
    screen.fill((0, 0, 0))
    
    # Draw starfield background
    for i in range(100):
        x = (i * 17) % SCREEN_WIDTH
        y = (i * 23) % SCREEN_HEIGHT
        size = random.randint(1, 3)
        brightness = 100 + int(math.sin(game_time + i) * 50)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(screen, color, (x, y), size)
    
    # Draw title
    title_font = get_font(72)
    title_text = "QAutoGame '90"
    title_surf = title_font.render(title_text, True, NEON_PINK)
    
    # Add glow effect to title
    for i in range(10, 0, -2):
        glow_surf = title_font.render(title_text, True, NEON_PINK)
        screen.blit(glow_surf, 
                   (SCREEN_WIDTH // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                    SCREEN_HEIGHT // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
    
    screen.blit(title_surf, 
               (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                SCREEN_HEIGHT // 6 - title_surf.get_height() // 2))
    
    # Draw all buttons
    button_font = get_font(24)
    for button in buttons.values():
        button.draw(screen, button_font)
        
    # Draw tip at the bottom
    tips = [
        "TIP: Use arrow keys or A/D to steer your car",
        "TIP: Collect orbs for extra points",
        "TIP: The game gets faster over time",
        "TIP: Press ESC to pause the game",
        "TIP: Try different color schemes in settings"
    ]
    tip_text = tips[int(game_time / 5) % len(tips)]
    tip_font = get_font(18)
    tip_surf = tip_font.render(tip_text, True, NEON_CYAN)
    screen.blit(tip_surf, 
               (SCREEN_WIDTH // 2 - tip_surf.get_width() // 2, 
                SCREEN_HEIGHT - 50))

# Draw pause menu
def draw_pause_menu(buttons):
    # Create semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    # Draw pause title
    title_font = get_font(48)
    title_text = "PAUSED"
    title_surf = title_font.render(title_text, True, NEON_YELLOW)
    
    screen.blit(title_surf, 
               (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                SCREEN_HEIGHT // 6 - title_surf.get_height() // 2))
    
    # Draw all buttons
    button_font = get_font(24)
    for button in buttons.values():
        button.draw(screen, button_font)

# Draw settings screen
def draw_settings_screen():
    # Fill background
    screen.fill((0, 0, 0))
    
    # Draw starfield background
    for i in range(100):
        x = (i * 17) % SCREEN_WIDTH
        y = (i * 23) % SCREEN_HEIGHT
        size = random.randint(1, 3)
        color = (100, 100, 100)
        pygame.draw.circle(screen, color, (x, y), size)
    
    # Draw title
    title_font = get_font(48)
    title_text = "SETTINGS"
    title_surf = title_font.render(title_text, True, NEON_BLUE)
    screen.blit(title_surf, 
               (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                SCREEN_HEIGHT // 6))
    
    # Draw settings options
    font = get_font(24)
    
    # Theme setting
    theme_text = f"THEME: {CONFIG['track_theme'].upper()}"
    theme_surf = font.render(theme_text, True, NEON_GREEN)
    screen.blit(theme_surf, 
               (SCREEN_WIDTH // 2 - theme_surf.get_width() // 2, 
                SCREEN_HEIGHT // 3))
    
    # Difficulty setting
    difficulty = "MEDIUM"  # Default
    difficulty_text = f"DIFFICULTY: {difficulty}"
    difficulty_surf = font.render(difficulty_text, True, NEON_PURPLE)
    screen.blit(difficulty_surf, 
               (SCREEN_WIDTH // 2 - difficulty_surf.get_width() // 2, 
                SCREEN_HEIGHT // 3 + 50))
    
    # Music setting
    music_text = "MUSIC: ON"
    music_surf = font.render(music_text, True, NEON_YELLOW)
    screen.blit(music_surf, 
               (SCREEN_WIDTH // 2 - music_surf.get_width() // 2, 
                SCREEN_HEIGHT // 3 + 100))
    
    # Back instructions
    back_text = "Press ESC to return to Main Menu"
    back_surf = font.render(back_text, True, NEON_ORANGE)
    screen.blit(back_surf, 
               (SCREEN_WIDTH // 2 - back_surf.get_width() // 2, 
                SCREEN_HEIGHT * 2 // 3))

# Draw high scores screen
def draw_high_scores_screen():
    # Fill background
    screen.fill((0, 0, 0))
    
    # Draw starfield background
    for i in range(100):
        x = (i * 17) % SCREEN_WIDTH
        y = (i * 23) % SCREEN_HEIGHT
        size = random.randint(1, 3)
        color = (100, 100, 100)
        pygame.draw.circle(screen, color, (x, y), size)
    
    # Draw title
    title_font = get_font(48)
    title_text = "HIGH SCORES"
    title_surf = title_font.render(title_text, True, NEON_PURPLE)
    screen.blit(title_surf, 
               (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                SCREEN_HEIGHT // 6))
    
    # Draw high scores
    font = get_font(24)
    
    # Sample high scores (replace with actual high scores)
    high_scores = [
        {"name": "AAA", "score": 5000},
        {"name": "BBB", "score": 4000},
        {"name": "CCC", "score": 3000},
        {"name": "DDD", "score": 2000},
        {"name": "EEE", "score": 1000}
    ]
    
    # Try to load high scores from file
    try:
        with open(os.path.join(os.path.dirname(__file__), "high_scores.json"), 'r') as f:
            loaded_scores = json.load(f)
            if loaded_scores:
                high_scores = loaded_scores
    except:
        pass
    
    y_pos = SCREEN_HEIGHT // 3
    for i, score in enumerate(high_scores[:10]):  # Show top 10 scores
        score_text = f"{i+1}. {score['name']} - {score['score']}"
        score_surf = font.render(score_text, True, NEON_CYAN)
        screen.blit(score_surf, 
                   (SCREEN_WIDTH // 2 - score_surf.get_width() // 2, 
                    y_pos))
        y_pos += 40
    
    # Back instructions
    back_text = "Press ESC to return to Main Menu"
    back_surf = font.render(back_text, True, NEON_ORANGE)
    screen.blit(back_surf, 
               (SCREEN_WIDTH // 2 - back_surf.get_width() // 2, 
                SCREEN_HEIGHT * 2 // 3))

# Draw instructions screen
def draw_instructions_screen():
    # Fill background
    screen.fill((0, 0, 0))
    
    # Draw starfield background
    for i in range(100):
        x = (i * 17) % SCREEN_WIDTH
        y = (i * 23) % SCREEN_HEIGHT
        size = random.randint(1, 3)
        color = (100, 100, 100)
        pygame.draw.circle(screen, color, (x, y), size)
    
    # Draw title
    title_font = get_font(48)
    title_text = "INSTRUCTIONS"
    title_surf = title_font.render(title_text, True, NEON_YELLOW)
    screen.blit(title_surf, 
               (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                SCREEN_HEIGHT // 6))
    
    # Draw instructions
    font = get_font(24)
    instructions = [
        "Use LEFT/RIGHT arrows or A/D keys to steer",
        "Avoid crashing into other cars",
        "Collect orbs for extra points",
        "Press ESC to pause the game"
    ]
    
    y_pos = SCREEN_HEIGHT // 3
    for instruction in instructions:
        instr_surf = font.render(instruction, True, WHITE)
        screen.blit(instr_surf, 
                   (SCREEN_WIDTH // 2 - instr_surf.get_width() // 2, 
                    y_pos))
        y_pos += 40
    
    # Back instructions
    back_text = "Press ESC to return to Main Menu"
    back_surf = font.render(back_text, True, NEON_ORANGE)
    screen.blit(back_surf, 
               (SCREEN_WIDTH // 2 - back_surf.get_width() // 2, 
                SCREEN_HEIGHT * 2 // 3))