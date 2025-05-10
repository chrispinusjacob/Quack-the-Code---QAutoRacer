# Game speeds
PLAYER_SPEED = 5
INITIAL_ENEMY_SPEED = 3
INITIAL_SCROLL_SPEED = 5

import pygame
import math
import random

class Car:
    """
    Car class for both player and enemies.
    """
    def __init__(self, x, y, color, is_player=False):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.color = color
        self.is_player = is_player
        self.speed = PLAYER_SPEED if is_player else INITIAL_ENEMY_SPEED
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.animation_time = 0
    
    def update(self, dt):
        """Update car state"""
        self.animation_time += dt
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, surface):
        """Draw car on the surface"""
        # Draw car body
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0, 5)
        
        # Draw windows
        window_color = (50, 50, 80) if self.is_player else (30, 30, 50)
        pygame.draw.rect(surface, window_color, (self.x + 5, self.y + 10, self.width - 10, 15), 0, 3)
        
        # Draw wheels
        wheel_color = (30, 30, 30)
        wheel_offset = 2 if self.is_player else 0
        
        # Left wheels
        pygame.draw.rect(surface, wheel_color, (self.x - wheel_offset, self.y + 5, 5, 12), 0, 2)
        pygame.draw.rect(surface, wheel_color, (self.x - wheel_offset, self.y + self.height - 17, 5, 12), 0, 2)
        
        # Right wheels
        pygame.draw.rect(surface, wheel_color, (self.x + self.width - 5 + wheel_offset, self.y + 5, 5, 12), 0, 2)
        pygame.draw.rect(surface, wheel_color, (self.x + self.width - 5 + wheel_offset, self.y + self.height - 17, 5, 12), 0, 2)
        
        # Add headlights for player
        if self.is_player:
            # Headlights
            pygame.draw.rect(surface, (255, 255, 200), (self.x + 5, self.y, 8, 5), 0, 2)
            pygame.draw.rect(surface, (255, 255, 200), (self.x + self.width - 13, self.y, 8, 5), 0, 2)
            
            # Taillights
            pygame.draw.rect(surface, (255, 50, 50), (self.x + 5, self.y + self.height - 5, 8, 5), 0, 2)
            pygame.draw.rect(surface, (255, 50, 50), (self.x + self.width - 13, self.y + self.height - 5, 8, 5), 0, 2)

class Orb:
    """
    Collectible orb that gives points.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.color = (0, 255, 255)  # Cyan
        self.collected = False
        self.animation_time = 0
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
    
    def update(self, speed):
        """Update orb position and animation"""
        self.y += speed
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius
        self.animation_time += 0.1
    
    def draw(self, surface):
        """Draw orb on the surface"""
        if not self.collected:
            # Pulsating effect
            pulse = math.sin(self.animation_time) * 0.2 + 0.8
            color = [min(255, c * pulse) for c in self.color]
            
            # Draw outer glow
            for i in range(3, 0, -1):
                alpha = 100 if i == 1 else 50
                pygame.draw.circle(surface, (*color, alpha), (int(self.x), int(self.y)), self.radius + i)
            
            # Draw main orb
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            
            # Draw inner highlight
            pygame.draw.circle(surface, (255, 255, 255), (int(self.x - self.radius/3), int(self.y - self.radius/3)), self.radius/4)

# Helper functions for creating road elements
def create_road_segment(width, height):
    """Create a road segment surface"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw road background
    pygame.draw.rect(surface, (50, 50, 50), (0, 0, width, height))
    
    # Draw lane markings
    lane_count = 3
    lane_width = width // lane_count
    for i in range(1, lane_count):
        x = i * lane_width
        for y in range(0, height, 30):
            pygame.draw.rect(surface, (255, 255, 255), (x - 2, y, 4, 15))
    
    return surface

def create_stripe(width, height):
    """Create a road stripe surface"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surface, (255, 255, 0), (0, 0, width, height))
    return surface