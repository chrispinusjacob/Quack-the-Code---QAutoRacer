import pygame
import sys
import math
import random
import os
import json
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

class HighScores:
    """High scores screen to display top player scores"""
    
    def __init__(self, screen, clock, sound_manager, scores_data):
        # Current selected button for keyboard navigation
        self.selected_button = 0
        self.screen = screen
        self.clock = clock
        self.sound_manager = sound_manager
        self.scores_data = scores_data
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
        self.small_font = self.get_font(18)  # Added missing small_font
        
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
        
        # Create reset button
        self.reset_button = Button(
            SCREEN_WIDTH // 2 - 100, 
            SCREEN_HEIGHT - 190, 
            200, 50, 
            "RESET SCORES", 
            self.text_font,
            text_color=WHITE, 
            hover_color=NEON_RED if hasattr(self, 'NEON_RED') else NEON_ORANGE, 
            border_color=NEON_RED if hasattr(self, 'NEON_RED') else NEON_ORANGE,
            sound_manager=self.sound_manager
        )
    
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
                elif event.key == K_UP or event.key == K_DOWN:
                    # Toggle between back and reset buttons
                    self.selected_button = 1 - self.selected_button
                    self.sound_manager.play("hover")
                elif event.key == K_RETURN or event.key == K_SPACE:
                    # Select current button
                    self.sound_manager.play("click")
                    if self.selected_button == 0:  # Back button
                        self.running = False
                        return "menu"
                    elif self.selected_button == 1:  # Reset button
                        # Reset high scores
                        self.scores_data["scores"] = []
                        # Save the empty scores
                        with open("high_scores.json", "w") as f:
                            json.dump(self.scores_data, f)
            
            # Check button clicks
            if self.back_button.is_clicked(event):
                self.running = False
                return "menu"
            
            if self.reset_button.is_clicked(event):
                # Reset high scores
                self.scores_data["scores"] = []
                self.save_high_scores()
        
        return None
    
    def save_high_scores(self):
        """Save high scores to file"""
        with open("high_scores.json", "w") as f:
            json.dump(self.scores_data, f)
    
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
        
        # Update buttons
        # Set hover state based on selected button
        self.back_button.is_hovered = (self.selected_button == 0)
        self.back_button.update(dt)
        self.reset_button.is_hovered = (self.selected_button == 1)
        self.reset_button.update(dt)
    
    def draw(self):
        """Draw the high scores screen"""
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
        title_text = "HIGH SCORES"
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
        
        # Draw high scores
        if not self.scores_data["scores"]:
            # No scores yet
            no_scores_text = "NO HIGH SCORES YET!"
            no_scores_surface = self.subtitle_font.render(no_scores_text, True, NEON_PINK)
            no_scores_rect = no_scores_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(no_scores_surface, no_scores_rect)
            
            play_text = "PLAY THE GAME TO SET A SCORE"
            play_surface = self.text_font.render(play_text, True, NEON_CYAN)
            play_rect = play_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(play_surface, play_rect)
        else:
            # Draw scores table
            scores = sorted(self.scores_data["scores"], reverse=True)[:10]  # Top 10 scores
            
            # Draw table header
            header_text = "RANK       SCORE"
            header_surface = self.subtitle_font.render(header_text, True, NEON_CYAN)
            self.screen.blit(header_surface, (SCREEN_WIDTH // 2 - 150, 120))
            
            # Draw horizontal line
            pygame.draw.line(self.screen, NEON_CYAN, 
                           (SCREEN_WIDTH // 2 - 200, 160), 
                           (SCREEN_WIDTH // 2 + 200, 160), 2)
            
            # Draw scores
            y_pos = 180
            for i, score in enumerate(scores):
                # Determine color based on rank
                if i == 0:
                    color = NEON_YELLOW  # Gold for 1st place
                elif i == 1:
                    color = (200, 200, 200)  # Silver for 2nd place
                elif i == 2:
                    color = (205, 127, 50)  # Bronze for 3rd place
                else:
                    color = WHITE
                
                # Draw rank with right alignment
                rank_text = f"{i+1}."
                rank_surface = self.text_font.render(rank_text, True, color)
                self.screen.blit(rank_surface, (SCREEN_WIDTH // 2 - 150, y_pos))
                
                # Draw score with left alignment
                score_text = f"{score}"
                score_surface = self.text_font.render(score_text, True, color)
                self.screen.blit(score_surface, (SCREEN_WIDTH // 2 + 50, y_pos))
                
                y_pos += 30
        
        # Draw keyboard navigation instructions
        nav_text = "Use UP/DOWN to Switch Buttons, ENTER to Select"
        nav_surface = self.small_font.render(nav_text, True, (200, 200, 200))
        nav_rect = nav_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200))
        self.screen.blit(nav_surface, nav_rect)
        
        # Draw buttons
        self.back_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Run the high scores screen"""
        while self.running:
            result = self.handle_events()
            if result:
                return result
                
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        return "menu"  # Default return to menu