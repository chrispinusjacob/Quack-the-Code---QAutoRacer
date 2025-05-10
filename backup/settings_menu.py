import pygame
import sys
import math
import random
import os
from pygame.locals import *
from button import Button
from sound_manager import sound_manager
from difficulty_manager import difficulty_manager
from theme_manager import theme_manager

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

class SettingsMenu:
    def __init__(self, screen, font_function):
        self.screen = screen
        self.get_font = font_function
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Create buttons - ensure proper spacing to make all buttons visible
        button_width = 200
        button_height = 50
        button_spacing = 15  # Reduced spacing to fit all buttons
        start_y = self.screen_height // 3
        
        # Theme options
        self.themes = ["SYNTHWAVE", "CYBERPUNK", "RETROWAVE", "NIGHT"]
        self.current_theme = 0
        
        # Difficulty options
        self.difficulties = ["EASY", "MEDIUM", "HARD"]
        self.current_difficulty = 1
        
        # Music toggle
        self.music_on = True
        
        # Sound toggle
        self.sound_on = True
        
        # Create buttons
        self.buttons = {
            "theme": Button(
                self.screen_width // 2 + 100,
                start_y,
                button_height, button_height,
                ">", NEON_GREEN
            ),
            "theme_prev": Button(
                self.screen_width // 2 - 100 - button_height,
                start_y,
                button_height, button_height,
                "<", NEON_GREEN
            ),
            "difficulty": Button(
                self.screen_width // 2 + 100,
                start_y + 50,
                button_height, button_height,
                ">", NEON_PURPLE
            ),
            "difficulty_prev": Button(
                self.screen_width // 2 - 100 - button_height,
                start_y + 50,
                button_height, button_height,
                "<", NEON_PURPLE
            ),
            "music": Button(
                self.screen_width // 2 + 100,
                start_y + 100,
                button_width // 2, button_height,
                "TOGGLE", NEON_YELLOW
            ),
            "sound": Button(
                self.screen_width // 2 + 100,
                start_y + 150,
                button_width // 2, button_height,
                "TOGGLE", NEON_CYAN
            ),
            "back": Button(
                self.screen_width // 2 - button_width // 2,
                self.screen_height * 2 // 3 + 50,
                button_width, button_height,
                "BACK TO MENU", NEON_ORANGE
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
                    # Make sure to stop any game sounds when returning to menu
                    sound_manager.stop_all_sounds()
                    return STATE_MAIN_MENU
        
        # Update all buttons
        for button in self.buttons.values():
            button.update(mouse_pos)
        
        # Check for button clicks
        if mouse_clicked:
            if self.buttons["theme"].is_clicked(mouse_pos, mouse_clicked):
                self.current_theme = (self.current_theme + 1) % len(self.themes)
                theme_manager.set_theme(self.current_theme)
                sound_manager.play_sound("click")
            elif self.buttons["theme_prev"].is_clicked(mouse_pos, mouse_clicked):
                self.current_theme = (self.current_theme - 1) % len(self.themes)
                theme_manager.set_theme(self.current_theme)
                sound_manager.play_sound("click")
            elif self.buttons["difficulty"].is_clicked(mouse_pos, mouse_clicked):
                self.current_difficulty = (self.current_difficulty + 1) % len(self.difficulties)
                difficulty_manager.set_difficulty(self.current_difficulty)
                sound_manager.play_sound("click")
            elif self.buttons["difficulty_prev"].is_clicked(mouse_pos, mouse_clicked):
                self.current_difficulty = (self.current_difficulty - 1) % len(self.difficulties)
                difficulty_manager.set_difficulty(self.current_difficulty)
                sound_manager.play_sound("click")
            elif self.buttons["music"].is_clicked(mouse_pos, mouse_clicked):
                self.music_on = sound_manager.toggle_music()
                sound_manager.play_sound("click")
            elif self.buttons["sound"].is_clicked(mouse_pos, mouse_clicked):
                self.sound_on = sound_manager.toggle_sound()
                if self.sound_on:
                    sound_manager.play_sound("click")
            elif self.buttons["back"].is_clicked(mouse_pos, mouse_clicked):
                # Make sure to stop any game sounds when returning to menu
                sound_manager.stop_all_sounds()
                sound_manager.play_sound("click")
                return STATE_MAIN_MENU
        
        return STATE_SETTINGS
    
    def draw(self):
        # Fill background
        self.screen.fill((0, 0, 0))
        
        # Draw starfield background
        for i in range(100):
            x = (i * 17) % self.screen_width
            y = (i * 23) % self.screen_height
            size = random.randint(1, 3)
            color = (100, 100, 100)
            pygame.draw.circle(self.screen, color, (x, y), size)
        
        # Draw title
        title_font = self.get_font(48)
        title_text = "SETTINGS"
        title_surf = title_font.render(title_text, True, NEON_BLUE)
        
        # Add glow effect
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_BLUE[:3], 25 * i))
            self.screen.blit(glow_surf, 
                       (self.screen_width // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        self.screen_height // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
        
        self.screen.blit(title_surf, 
                   (self.screen_width // 2 - title_surf.get_width() // 2, 
                    self.screen_height // 6 - title_surf.get_height() // 2))
        
        # Draw settings options
        font = self.get_font(24)
        
        # Theme setting
        theme_text = f"THEME: {self.themes[self.current_theme]}"
        theme_surf = font.render(theme_text, True, NEON_GREEN)
        self.screen.blit(theme_surf, 
                   (self.screen_width // 2 - theme_surf.get_width() // 2, 
                    self.screen_height // 3))
        
        # Difficulty setting
        difficulty_text = f"DIFFICULTY: {self.difficulties[self.current_difficulty]}"
        difficulty_surf = font.render(difficulty_text, True, NEON_PURPLE)
        self.screen.blit(difficulty_surf, 
                   (self.screen_width // 2 - difficulty_surf.get_width() // 2, 
                    self.screen_height // 3 + 50))
        
        # Music setting
        music_text = f"MUSIC: {'ON' if self.music_on else 'OFF'}"
        music_surf = font.render(music_text, True, NEON_YELLOW)
        self.screen.blit(music_surf, 
                   (self.screen_width // 2 - 100, 
                    self.screen_height // 3 + 100))
        
        # Sound setting
        sound_text = f"SOUND FX: {'ON' if self.sound_on else 'OFF'}"
        sound_surf = font.render(sound_text, True, NEON_CYAN)
        self.screen.blit(sound_surf, 
                   (self.screen_width // 2 - 100, 
                    self.screen_height // 3 + 150))
        
        # Draw all buttons
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