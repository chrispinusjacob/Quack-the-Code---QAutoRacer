import pygame
import sys
import json
import os
from pygame.locals import *

# Game states
STATE_MAIN_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_PAUSED = 3
STATE_SETTINGS = 4
STATE_HIGH_SCORES = 5
STATE_INSTRUCTIONS = 6

# Colors (matching the main game)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (0, 191, 255)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (138, 43, 226)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)
NEON_CYAN = (0, 255, 255)

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")
FONT_DIR = os.path.join(ASSET_DIR, "fonts")

# Create directories if they don't exist
os.makedirs(SOUND_DIR, exist_ok=True)
os.makedirs(FONT_DIR, exist_ok=True)

# Create pixel fonts
def get_font(size):
    try:
        return pygame.font.Font(os.path.join(FONT_DIR, "pixel.ttf"), size)
    except:
        return pygame.font.SysFont("Arial", size)

# Button class for menus
class Button:
    def __init__(self, x, y, width, height, text, color=NEON_BLUE, hover_color=NEON_PINK, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.font = get_font(24)
        
    def draw(self, surface):
        # Draw button with hover effect
        color = self.hover_color if self.is_hovered else self.color
        
        # Draw button background with glow effect
        for i in range(5, 0, -1):
            glow_rect = pygame.Rect(
                self.rect.x - i, self.rect.y - i, 
                self.rect.width + i*2, self.rect.height + i*2
            )
            pygame.draw.rect(surface, (*color[:3], 50), glow_rect, border_radius=5)
        
        # Main button
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=5)  # Border
        
        # Button text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos):
        # Update hover state
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        # Check if button was clicked
        return self.rect.collidepoint(mouse_pos) and mouse_click

class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.state = STATE_MAIN_MENU
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = screen_height // 3
        
        self.buttons = {
            "start": Button(
                screen_width // 2 - button_width // 2,
                start_y,
                button_width, button_height,
                "START GAME", NEON_GREEN
            ),
            "settings": Button(
                screen_width // 2 - button_width // 2,
                start_y + button_height + button_spacing,
                button_width, button_height,
                "SETTINGS", NEON_BLUE
            ),
            "high_scores": Button(
                screen_width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 2,
                button_width, button_height,
                "HIGH SCORES", NEON_PURPLE
            ),
            "instructions": Button(
                screen_width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 3,
                button_width, button_height,
                "INSTRUCTIONS", NEON_YELLOW
            ),
            "exit": Button(
                screen_width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 4,
                button_width, button_height,
                "EXIT", NEON_ORANGE
            )
        }
        
        # Animation variables
        self.time = 0
        
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
        
        # Update all buttons
        for button in self.buttons.values():
            button.update(mouse_pos)
        
        # Check for button clicks
        if mouse_clicked:
            if self.buttons["start"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_PLAYING
            elif self.buttons["settings"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_SETTINGS
            elif self.buttons["high_scores"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_HIGH_SCORES
            elif self.buttons["instructions"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_INSTRUCTIONS
            elif self.buttons["exit"].is_clicked(mouse_pos, mouse_clicked):
                pygame.quit()
                sys.exit()
        
        return self.state
    
    def update(self, dt):
        self.time += dt
    
    def draw(self, surface):
        # Fill background
        surface.fill(BLACK)
        
        # Draw starfield background
        for i in range(100):
            x = (i * 17) % self.screen_width
            y = (i * 23) % self.screen_height
            size = random.randint(1, 3)
            brightness = 100 + int(math.sin(self.time + i) * 50)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(surface, color, (x, y), size)
        
        # Draw title
        title_font = get_font(72)
        title_text = "QAutoGame '90"
        title_surf = title_font.render(title_text, True, NEON_PINK)
        
        # Add glow effect to title
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_PINK[:3], 25 * i))
            surface.blit(glow_surf, 
                       (self.screen_width // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        self.screen_height // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
        
        surface.blit(title_surf, 
                   (self.screen_width // 2 - title_surf.get_width() // 2, 
                    self.screen_height // 6 - title_surf.get_height() // 2))
        
        # Draw all buttons
        for button in self.buttons.values():
            button.draw(surface)

class PauseMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = screen_height // 3
        
        self.buttons = {
            "resume": Button(
                screen_width // 2 - button_width // 2,
                start_y,
                button_width, button_height,
                "RESUME", NEON_GREEN
            ),
            "restart": Button(
                screen_width // 2 - button_width // 2,
                start_y + button_height + button_spacing,
                button_width, button_height,
                "RESTART", NEON_BLUE
            ),
            "main_menu": Button(
                screen_width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 2,
                button_width, button_height,
                "MAIN MENU", NEON_PURPLE
            ),
            "quit": Button(
                screen_width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 3,
                button_width, button_height,
                "QUIT GAME", NEON_ORANGE
            )
        }
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return STATE_PLAYING
        
        # Update all buttons
        for button in self.buttons.values():
            button.update(mouse_pos)
        
        # Check for button clicks
        if mouse_clicked:
            if self.buttons["resume"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_PLAYING
            elif self.buttons["restart"].is_clicked(mouse_pos, mouse_clicked):
                # Return special code to indicate restart
                return -1
            elif self.buttons["main_menu"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_MAIN_MENU
            elif self.buttons["quit"].is_clicked(mouse_pos, mouse_clicked):
                pygame.quit()
                sys.exit()
        
        return STATE_PAUSED
    
    def draw(self, surface):
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        
        # Draw pause title
        title_font = get_font(48)
        title_text = "PAUSED"
        title_surf = title_font.render(title_text, True, NEON_YELLOW)
        
        # Add glow effect to title
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_YELLOW[:3], 25 * i))
            surface.blit(glow_surf, 
                       (self.screen_width // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        self.screen_height // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
        
        surface.blit(title_surf, 
                   (self.screen_width // 2 - title_surf.get_width() // 2, 
                    self.screen_height // 6 - title_surf.get_height() // 2))
        
        # Draw all buttons
        for button in self.buttons.values():
            button.draw(surface)

# Save and load functions
def save_high_scores(scores, filename="high_scores.json"):
    """Save high scores to a JSON file"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'w') as f:
        json.dump(scores, f)

def load_high_scores(filename="high_scores.json"):
    """Load high scores from a JSON file"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty scores if file doesn't exist or is invalid
        return []

def save_game_state(state, filename="game_save.json"):
    """Save game state to a JSON file"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'w') as f:
        json.dump(state, f)

def load_game_state(filename="game_save.json"):
    """Load game state from a JSON file"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return None if file doesn't exist or is invalid
        return None