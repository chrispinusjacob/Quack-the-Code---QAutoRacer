import pygame
import os
import random
import math
from pygame.locals import *

class Button:
    def __init__(self, x, y, width, height, text, color=(0, 191, 255), hover_color=(255, 20, 147), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.click_sound = None
        self.hover_sound = None
        
        # Try to load sounds if available
        try:
            sound_dir = os.path.join(os.path.dirname(__file__), "assets", "sounds")
            self.click_sound = pygame.mixer.Sound(os.path.join(sound_dir, "click.mp3"))
            self.hover_sound = pygame.mixer.Sound(os.path.join(sound_dir, "hover.mp3"))
        except:
            pass
        
    def draw(self, surface, font):
        # Draw button with hover effect
        color = self.hover_color if self.is_hovered else self.color
        
        # Draw button background with glow effect
        for i in range(5, 0, -1):
            glow_rect = pygame.Rect(
                self.rect.x - i, self.rect.y - i, 
                self.rect.width + i*2, self.rect.height + i*2
            )
            # Use a regular color without alpha for compatibility
            glow_color = (color[0], color[1], color[2])
            pygame.draw.rect(surface, glow_color, glow_rect, border_radius=5)
        
        # Main button
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=5)  # Border
        
        # Button text
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos):
        # Check if hover state changed
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Play hover sound if just started hovering
        if not was_hovered and self.is_hovered and self.hover_sound:
            self.hover_sound.play()
        
    def is_clicked(self, mouse_pos, mouse_click):
        # Check if button was clicked
        clicked = self.rect.collidepoint(mouse_pos) and mouse_click
        if clicked and self.click_sound:
            self.click_sound.play()
        return clicked