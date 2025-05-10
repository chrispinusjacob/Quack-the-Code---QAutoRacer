import pygame
import sys
import math
import random
import os
from pygame.locals import *
from button import Button

# Game states
STATE_MAIN_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_PAUSED = 3
STATE_SETTINGS = 4
STATE_HIGH_SCORES = 5
STATE_INSTRUCTIONS = 6

# Colors (for convenience)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (0, 191, 255)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (138, 43, 226)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)
NEON_CYAN = (0, 255, 255)
WHITE = (255, 255, 255)

class PauseMenu:
    def __init__(self, screen, font_function):
        self.screen = screen
        self.get_font = font_function
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Create buttons - ensure proper spacing to make all buttons visible
        button_width = 220  # Slightly wider buttons for better visibility
        button_height = 50
        button_spacing = 15  # Reduced spacing to fit all buttons
        
        # Calculate start_y to ensure all buttons fit on screen with proper spacing
        total_buttons_height = (button_height * 4) + (button_spacing * 3)
        start_y = (self.screen_height - total_buttons_height) // 2
        
        self.buttons = {
            "resume": Button(
                self.screen_width // 2 - button_width // 2,
                start_y,
                button_width, button_height,
                "RESUME", NEON_GREEN
            ),
            "restart": Button(
                self.screen_width // 2 - button_width // 2,
                start_y + button_height + button_spacing,
                button_width, button_height,
                "RESTART", NEON_BLUE
            ),
            "main_menu": Button(
                self.screen_width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 2,
                button_width, button_height,
                "MAIN MENU", NEON_PURPLE
            ),
            "quit": Button(
                self.screen_width // 2 - button_width // 2,
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
                    print("Resume game from pause menu via ESC key")
                    return STATE_PLAYING  # This returns to playing state
        
        # Update all buttons
        for button in self.buttons.values():
            button.update(mouse_pos)
        
        # Check for button clicks
        if mouse_clicked:
            if self.buttons["resume"].is_clicked(mouse_pos, mouse_clicked):
                print("Resume game from pause menu via Resume button")
                return STATE_PLAYING
            elif self.buttons["restart"].is_clicked(mouse_pos, mouse_clicked):
                # Return special code to indicate restart
                print("Restart game from pause menu")
                return -1
            elif self.buttons["main_menu"].is_clicked(mouse_pos, mouse_clicked):
                print("Return to main menu from pause menu")
                return STATE_MAIN_MENU
            elif self.buttons["quit"].is_clicked(mouse_pos, mouse_clicked):
                print("Quit game from pause menu")
                pygame.quit()
                sys.exit()
        
        return STATE_PAUSED
    
    def draw(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause title
        title_font = self.get_font(48)
        title_text = "PAUSED"
        title_surf = title_font.render(title_text, True, NEON_YELLOW)
        
        # Add glow effect to title
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_YELLOW[:3], 25 * i))
            self.screen.blit(glow_surf, 
                       (self.screen_width // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        self.screen_height // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
        
        self.screen.blit(title_surf, 
                   (self.screen_width // 2 - title_surf.get_width() // 2, 
                    self.screen_height // 6 - title_surf.get_height() // 2))
        
        # Draw all buttons - ensure they're all visible
        button_font = self.get_font(24)
        for button in self.buttons.values():
            button.draw(self.screen, button_font)
            
        # Add credits at the bottom
        credit_font = self.get_font(16)
        credit_text = "Created by Chrispinus Jacob, Powered by Amazon Q"
        credit_surf = credit_font.render(credit_text, True, WHITE)
        self.screen.blit(credit_surf,
                      (self.screen_width // 2 - credit_surf.get_width() // 2,
                       self.screen_height - 30))