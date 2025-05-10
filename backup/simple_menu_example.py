import pygame
import sys
import math
import random
import os
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Menu Example"

# Game states
STATE_MAIN_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (0, 191, 255)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (138, 43, 226)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color=NEON_BLUE, hover_color=NEON_PINK, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.SysFont("Arial", 24)
        
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

# Main Menu class
class MainMenu:
    def __init__(self):
        self.time = 0
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = SCREEN_HEIGHT // 3
        
        self.buttons = {
            "start": Button(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y,
                button_width, button_height,
                "START GAME", NEON_GREEN
            ),
            "settings": Button(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y + button_height + button_spacing,
                button_width, button_height,
                "SETTINGS", NEON_BLUE
            ),
            "exit": Button(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 2,
                button_width, button_height,
                "EXIT", NEON_ORANGE
            )
        }
    
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
            elif self.buttons["exit"].is_clicked(mouse_pos, mouse_clicked):
                pygame.quit()
                sys.exit()
        
        return STATE_MAIN_MENU
    
    def update(self, dt):
        self.time += dt
    
    def draw(self):
        # Fill background
        screen.fill(BLACK)
        
        # Draw starfield background
        for i in range(100):
            x = (i * 17) % SCREEN_WIDTH
            y = (i * 23) % SCREEN_HEIGHT
            size = random.randint(1, 3)
            brightness = 100 + int(math.sin(self.time + i) * 50)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (x, y), size)
        
        # Draw title
        title_font = pygame.font.SysFont("Arial", 72)
        title_text = "QAutoGame"
        title_surf = title_font.render(title_text, True, NEON_PINK)
        
        # Add glow effect to title
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_PINK[:3], 25 * i))
            screen.blit(glow_surf, 
                       (SCREEN_WIDTH // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        SCREEN_HEIGHT // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
        
        screen.blit(title_surf, 
                   (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                    SCREEN_HEIGHT // 6 - title_surf.get_height() // 2))
        
        # Draw all buttons
        for button in self.buttons.values():
            button.draw(screen)

# Pause Menu class
class PauseMenu:
    def __init__(self):
        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = SCREEN_HEIGHT // 3
        
        self.buttons = {
            "resume": Button(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y,
                button_width, button_height,
                "RESUME", NEON_GREEN
            ),
            "main_menu": Button(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y + button_height + button_spacing,
                button_width, button_height,
                "MAIN MENU", NEON_PURPLE
            ),
            "quit": Button(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 2,
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
            elif self.buttons["main_menu"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_MAIN_MENU
            elif self.buttons["quit"].is_clicked(mouse_pos, mouse_clicked):
                pygame.quit()
                sys.exit()
        
        return STATE_PAUSED
    
    def draw(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Draw pause title
        title_font = pygame.font.SysFont("Arial", 48)
        title_text = "PAUSED"
        title_surf = title_font.render(title_text, True, NEON_YELLOW)
        
        # Add glow effect to title
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_YELLOW[:3], 25 * i))
            screen.blit(glow_surf, 
                       (SCREEN_WIDTH // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        SCREEN_HEIGHT // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
        
        screen.blit(title_surf, 
                   (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                    SCREEN_HEIGHT // 6 - title_surf.get_height() // 2))
        
        # Draw all buttons
        for button in self.buttons.values():
            button.draw(screen)

# Simple game class
class SimpleGame:
    def __init__(self):
        self.running = True
        self.state = STATE_MAIN_MENU
        self.game_time = 0
        
        # Create menu objects
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()
    
    def handle_events(self):
        events = pygame.event.get()
        
        for event in events:
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.state == STATE_PLAYING:
                        self.state = STATE_PAUSED
                    elif self.state == STATE_PAUSED:
                        self.state = STATE_PLAYING
        
        # Handle menu states
        if self.state == STATE_MAIN_MENU:
            new_state = self.main_menu.handle_events(events)
            if new_state != self.state:
                self.state = new_state
        elif self.state == STATE_PAUSED:
            new_state = self.pause_menu.handle_events(events)
            if new_state != self.state:
                self.state = new_state
    
    def update(self):
        dt = clock.get_time() / 1000.0  # Delta time in seconds
        
        if self.state == STATE_MAIN_MENU:
            self.main_menu.update(dt)
        elif self.state == STATE_PLAYING:
            self.game_time += dt
    
    def draw(self):
        if self.state == STATE_MAIN_MENU:
            self.main_menu.draw()
        elif self.state == STATE_PLAYING:
            # Draw simple game screen
            screen.fill(BLACK)
            
            # Draw starfield background
            for i in range(100):
                x = (i * 17) % SCREEN_WIDTH
                y = (i * 23) % SCREEN_HEIGHT
                size = random.randint(1, 3)
                brightness = 100 + int(math.sin(self.game_time + i) * 50)
                color = (brightness, brightness, brightness)
                pygame.draw.circle(screen, color, (x, y), size)
            
            # Draw game text
            font = pygame.font.SysFont("Arial", 36)
            text = "Game Running - Press ESC to Pause"
            text_surf = font.render(text, True, NEON_GREEN)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text_surf, text_rect)
            
            # Draw time
            time_text = f"Time: {self.game_time:.1f}s"
            time_surf = font.render(time_text, True, NEON_BLUE)
            screen.blit(time_surf, (20, 20))
            
        # Draw pause menu if paused
        if self.state == STATE_PAUSED:
            self.pause_menu.draw()
        
        pygame.display.flip()
    
    def run(self):
        # Main game loop
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Start the game
if __name__ == "__main__":
    game = SimpleGame()
    game.run()