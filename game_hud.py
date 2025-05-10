import pygame
import math

class GameHUD:
    """
    Heads-Up Display for the game.
    Shows score, high score, speed, and difficulty level.
    """
    def __init__(self, screen, font_function):
        self.screen = screen
        self.get_font = font_function
        self.score = 0
        self.high_score = 0
        self.speed_percent = 0
        self.difficulty_level = "MEDIUM"
        
        # Colors
        self.NEON_PINK = (255, 20, 147)
        self.NEON_CYAN = (0, 255, 255)
        self.NEON_GREEN = (57, 255, 20)
        self.NEON_YELLOW = (255, 255, 0)
        
        # Animation
        self.animation_time = 0
    
    def update(self, dt, score, high_score, speed_percent, difficulty_level=None):
        """Update HUD data"""
        self.score = score
        self.high_score = high_score
        self.speed_percent = speed_percent
        if difficulty_level:
            self.difficulty_level = difficulty_level
        
        # Update animation
        self.animation_time += dt
    
    def draw(self):
        """Draw the HUD on screen"""
        screen_width = self.screen.get_width()
        
        # Create a semi-transparent HUD background
        hud_surface = pygame.Surface((screen_width, 60), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 150))
        self.screen.blit(hud_surface, (0, 0))
        
        # Draw score
        font = self.get_font(24)
        score_text = f"SCORE: {self.score}"
        score_surface = font.render(score_text, True, self.NEON_PINK)
        self.screen.blit(score_surface, (20, 15))
        
        # Draw high score
        high_score_text = f"HIGH SCORE: {self.high_score}"
        high_score_surface = font.render(high_score_text, True, self.NEON_CYAN)
        self.screen.blit(high_score_surface, (screen_width - 20 - high_score_surface.get_width(), 15))
        
        # Draw speed indicator
        speed_text = f"SPEED: {int(self.speed_percent)}%"
        speed_surface = font.render(speed_text, True, self.NEON_GREEN)
        
        # Draw difficulty level with pulsating effect
        difficulty_color = self.NEON_YELLOW
        if self.difficulty_level.upper() == "EASY":
            difficulty_color = self.NEON_GREEN
        elif self.difficulty_level.upper() == "HARD":
            difficulty_color = self.NEON_PINK
        
        # Add pulsating effect to difficulty text
        pulse = math.sin(self.animation_time * 3) * 0.2 + 0.8
        difficulty_text = f"DIFFICULTY: {self.difficulty_level.upper()}"
        difficulty_surface = font.render(difficulty_text, True, difficulty_color)
        
        # Position speed and difficulty in the center
        center_width = screen_width // 2
        self.screen.blit(speed_surface, (center_width - speed_surface.get_width() - 10, 15))
        self.screen.blit(difficulty_surface, (center_width + 10, 15))