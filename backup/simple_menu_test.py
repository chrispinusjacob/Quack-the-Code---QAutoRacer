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
pygame.display.set_caption("Menu Test")
clock = pygame.time.Clock()

# Simple Button class
class SimpleButton:
    def __init__(self, x, y, width, height, text, color=NEON_BLUE, hover_color=NEON_PINK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        # Get font
        font = pygame.font.SysFont("Arial", 24)
        
        # Draw button with hover effect
        color = self.hover_color if self.is_hovered else self.color
        
        # Main button
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=5)  # Border
        
        # Button text
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos):
        # Check if hover state changed
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        # Check if button was clicked
        return self.rect.collidepoint(mouse_pos) and mouse_click

# Create buttons
buttons = [
    SimpleButton(SCREEN_WIDTH//2 - 100, 200, 200, 50, "START GAME", NEON_GREEN),
    SimpleButton(SCREEN_WIDTH//2 - 100, 270, 200, 50, "SETTINGS", NEON_BLUE),
    SimpleButton(SCREEN_WIDTH//2 - 100, 340, 200, 50, "EXIT", NEON_ORANGE)
]

# Main loop
running = True
while running:
    # Handle events
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicked = True
    
    # Update buttons
    for button in buttons:
        button.update(mouse_pos)
        
        # Check for clicks
        if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
            print(f"Button clicked: {button.text}")
            if button.text == "EXIT":
                running = False
    
    # Draw everything
    screen.fill(BLACK)
    
    # Draw title
    font = pygame.font.SysFont("Arial", 48)
    title_text = "MENU TEST"
    title_surf = font.render(title_text, True, NEON_PINK)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 100))
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()