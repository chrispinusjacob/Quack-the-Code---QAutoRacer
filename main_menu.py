import pygame
import sys
import math
import random
import os
from pygame.locals import *
from button import Button

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "QAutoGame"

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

class MainMenu:
    def __init__(self, screen, clock, sound_manager):
        # Current selected button for keyboard navigation
        self.selected_button = 0
        self.screen = screen
        self.clock = clock
        self.sound_manager = sound_manager
        self.running = True
        self.selected_option = None
        self.animation_time = 0
        self.stars = []
        
        # Create stars for background
        for i in range(100):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.uniform(1, 3),
                'speed': random.uniform(0.5, 2)
            })
        
        # Load or create fonts
        self.title_font = self.get_font(60)
        self.menu_font = self.get_font(36)
        self.small_font = self.get_font(24)
        
        # Create buttons
        button_width = 300
        button_height = 60
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.buttons = [
            Button(button_x, 150, button_width, button_height, 
                  "START GAME", self.menu_font, 
                  text_color=WHITE, hover_color=NEON_GREEN, 
                  border_color=NEON_GREEN, sound_manager=self.sound_manager),
            
            Button(button_x, 220, button_width, button_height, 
                  "HIGH SCORES", self.menu_font, 
                  text_color=WHITE, hover_color=NEON_BLUE, 
                  border_color=NEON_BLUE, sound_manager=self.sound_manager),
            
            Button(button_x, 290, button_width, button_height, 
                  "INSTRUCTIONS", self.menu_font, 
                  text_color=WHITE, hover_color=NEON_YELLOW, 
                  border_color=NEON_YELLOW, sound_manager=self.sound_manager),
            
            Button(button_x, 360, button_width, button_height, 
                  "SETTINGS", self.menu_font, 
                  text_color=WHITE, hover_color=NEON_PURPLE, 
                  border_color=NEON_PURPLE, sound_manager=self.sound_manager),
            
            Button(button_x, 430, button_width, button_height, 
                  "EXIT", self.menu_font, 
                  text_color=WHITE, hover_color=NEON_PINK, 
                  border_color=NEON_PINK, sound_manager=self.sound_manager)
        ]
        
        # Make sure engine sound is stopped
        self.sound_manager.stop("engine")
        
        # Start menu music
        self.sound_manager.play_music("menu_music.mp3")
    
    def get_font(self, size):
        """Get a font of specified size"""
        font_dir = os.path.join(os.path.dirname(__file__), "assets", "fonts")
        try:
            return pygame.font.Font(os.path.join(font_dir, "pixel.ttf"), size)
        except:
            return pygame.font.SysFont("Arial", size)
    
    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                self.selected_option = "exit"
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    self.selected_option = "exit"
                elif event.key == K_UP:
                    # Navigate up
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                    self.sound_manager.play("hover")
                elif event.key == K_DOWN:
                    # Navigate down
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                    self.sound_manager.play("hover")
                elif event.key == K_RETURN or event.key == K_SPACE:
                    # Select current button
                    self.sound_manager.play("click")
                    if self.selected_button == 0:  # Start Game
                        self.running = False
                        self.selected_option = "start"
                    elif self.selected_button == 1:  # High Scores
                        self.running = False
                        self.selected_option = "scores"
                    elif self.selected_button == 2:  # Instructions
                        self.running = False
                        self.selected_option = "instructions"
                    elif self.selected_button == 3:  # Settings
                        self.running = False
                        self.selected_option = "settings"
                    elif self.selected_button == 4:  # Exit
                        self.running = False
                        self.selected_option = "exit"
            
            # Check button clicks
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event):
                    if i == 0:  # Start Game
                        self.running = False
                        self.selected_option = "start"
                    elif i == 1:  # High Scores
                        self.running = False
                        self.selected_option = "scores"
                    elif i == 2:  # Instructions
                        self.running = False
                        self.selected_option = "instructions"
                    elif i == 3:  # Settings
                        self.running = False
                        self.selected_option = "settings"
                    elif i == 4:  # Exit
                        self.running = False
                        self.selected_option = "exit"
    
    def update(self):
        """Update menu state"""
        dt = self.clock.get_time() / 1000.0  # Delta time in seconds
        self.animation_time += dt
        
        # Update stars
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
        
        # Update buttons
        for i, button in enumerate(self.buttons):
            # Set hover state based on selected button
            button.is_hovered = (i == self.selected_button)
            button.update(dt)
    
    def draw(self):
        """Draw the menu"""
        # Fill background
        self.screen.fill(BLACK)
        
        # Draw stars
        for star in self.stars:
            brightness = 100 + int(math.sin(self.animation_time * 2 + star['x']) * 50)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, 
                             (int(star['x']), int(star['y'])), 
                             int(star['size']))
        
        # Draw title with glow effect
        title_text = "QAutoGame"
        title_surface = self.title_font.render(title_text, True, NEON_PINK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        
        # Add glow effect to title
        for i in range(10, 0, -2):
            glow_surface = self.title_font.render(title_text, True, (*NEON_PINK[:3], 25 * i))
            glow_rect = glow_surface.get_rect(center=(
                title_rect.centerx + random.randint(-i, i),
                title_rect.centery + random.randint(-i, i)
            ))
            self.screen.blit(glow_surface, glow_rect)
        
        # Draw main title
        self.screen.blit(title_surface, title_rect)
        # Draw copyright text
        copyright_font = self.get_font(16)
        copyright_text = "Copyright 2025 by Chrispinus Jacob"
        copyright_surface = copyright_font.render(copyright_text, True, (150, 150, 150))
        copyright_rect = copyright_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(copyright_surface, copyright_rect)
        # Draw powered by text
        powered_text = "Powered by Amazon Q"
        powered_surface = copyright_font.render(powered_text, True, (150, 150, 150))
        powered_rect = powered_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        self.screen.blit(powered_surface, powered_rect)
        
        # Draw subtitle
        subtitle_text = ""
        subtitle_surface = self.small_font.render(subtitle_text, True, NEON_CYAN)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        # Draw keyboard navigation instructions
        nav_text = "Use Arrow Keys to Navigate, Enter to Select"
        nav_surface = self.small_font.render(nav_text, True, (200, 200, 200))
        nav_rect = nav_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 140))
        self.screen.blit(nav_surface, nav_rect)
                # Draw footer text
        footer_text = "QAutoGame © 2025"
        footer_surface = self.small_font.render(footer_text, True, (150, 150, 150))
        footer_rect = footer_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(footer_surface, footer_rect)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Run the main menu loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Return the selected option
        return self.selected_option