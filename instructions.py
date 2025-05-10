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

class Instructions:
    """Instructions screen showing how to play the game"""
    
    def __init__(self, screen, clock, sound_manager):
        # Current selected button for keyboard navigation
        self.selected_button = 0
        self.screen = screen
        self.clock = clock
        self.sound_manager = sound_manager
        self.running = True
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
        self.title_font = self.get_font(48)
        self.subtitle_font = self.get_font(36)
        self.text_font = self.get_font(24)
        self.small_font = self.get_font(18)
        
        # Create back button
        self.back_button = Button(
            SCREEN_WIDTH // 2 - 100, 
            SCREEN_HEIGHT - 120, 
            200, 50, 
            "BACK TO MENU", 
            self.text_font,
            text_color=WHITE, 
            hover_color=NEON_PINK, 
            border_color=NEON_PINK,
            sound_manager=self.sound_manager
        )
        
        # Instructions content
        self.instructions = [
            {
                "title": "CONTROLS",
                "content": [
                    "LEFT/A: Move left | RIGHT/D: Move right",
                    "P or ESC: Pause | SPACE: Restart"
                ]
            },
            {
                "title": "GAMEPLAY",
                "content": [
                    "Avoid cars | Collect orbs for points",
                    "Speed increases over time"
                ]
            },
            {
                "title": "TIPS",
                "content": [
                    "Stay in open lanes | Plan ahead",
                    "Be careful with orbs in traffic"
                ]
            }
        ]
    
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
                return "exit"
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    return "menu"
                elif event.key == K_RETURN or event.key == K_SPACE:
                    # Return to menu
                    self.running = False
                    return "menu"
            
            # Check button clicks
            if self.back_button.is_clicked(event):
                self.running = False
                return "menu"
        
        return None
    
    def update(self):
        """Update screen elements"""
        dt = self.clock.get_time() / 1000.0  # Delta time in seconds
        self.animation_time += dt
        
        # Update stars
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
        
        # Update button
        # Always highlight the back button
        self.back_button.is_hovered = True
        self.back_button.update(dt)
    
    def draw(self):
        """Draw the instructions screen"""
        # Fill background
        self.screen.fill(BLACK)
        
        # Draw stars
        for star in self.stars:
            brightness = 100 + int(math.sin(self.animation_time * 2 + star['x']) * 50)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, 
                             (int(star['x']), int(star['y'])), 
                             int(star['size']))
        
        # Draw title
        title_text = "HOW TO PLAY"
        title_surface = self.title_font.render(title_text, True, NEON_YELLOW)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 40))
        
        # Add glow effect to title
        for i in range(6, 0, -2):
            glow_surface = self.title_font.render(title_text, True, (*NEON_YELLOW[:3], 25 * i))
            glow_rect = glow_surface.get_rect(center=(
                title_rect.centerx + random.randint(-i, i),
                title_rect.centery + random.randint(-i, i)
            ))
            self.screen.blit(glow_surface, glow_rect)
        
        # Draw main title
        self.screen.blit(title_surface, title_rect)
        
        # Draw instructions sections
        y_offset = 100
        for section in self.instructions:
            # Draw section title
            section_title = section["title"]
            section_surface = self.subtitle_font.render(section_title, True, NEON_CYAN)
            section_rect = section_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(section_surface, section_rect)
            
            # Draw section content
            y_offset += 40
            for line in section["content"]:
                line_surface = self.text_font.render(line, True, WHITE)
                line_rect = line_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(line_surface, line_rect)
                y_offset += 25
            
            y_offset += 10
        
        # Draw car controls diagram
        # Controls diagram removed to prevent overlap
        # self.draw_controls_diagram(SCREEN_WIDTH // 2 - 150, y_offset)
        
        # Draw keyboard navigation instructions
        nav_text = "Press ESC or ENTER to Return to Menu"
        nav_surface = self.small_font.render(nav_text, True, (200, 200, 200))
        nav_rect = nav_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
        self.screen.blit(nav_surface, nav_rect)
        
                # Draw back button
        self.back_button.draw(self.screen)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Run the instructions screen"""
        while self.running:
            result = self.handle_events()
            if result:
                return result
                
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        return "menu"  # Default return to menu