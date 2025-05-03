import pygame
import math
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, NEON_PINK, NEON_BLUE, NEON_GREEN, NEON_PURPLE, NEON_YELLOW, NEON_ORANGE, NEON_RED

# Sprite class for track decorations
class TrackSprite:
    def __init__(self, type, side, offset=0):
        self.type = type  # "tree", "billboard", "rock", "building"
        self.side = side  # -1 for left, 1 for right
        self.offset = offset  # Additional offset from road edge
        self.animation_frame = random.random() * 10  # Random start frame
        self.animation_speed = 0.05
        self.color_variation = random.randint(-20, 20)
    
    def draw(self, screen, x, y, w, h, scale):
        # Calculate position based on side and offset
        pos_x = x + (self.side * (w + 50)) + (self.offset * scale)
        
        if self.type == "tree":
            # Tree trunk
            trunk_width = max(5, int(10 * scale))
            trunk_height = max(10, int(40 * scale))
            trunk_color = (101 + self.color_variation, 67 + self.color_variation, 33 + self.color_variation)
            pygame.draw.rect(screen, trunk_color, 
                           (pos_x - trunk_width//2, y - trunk_height, trunk_width, trunk_height))
            
            # Tree foliage (animated slightly)
            foliage_size = max(15, int(50 * scale))
            sway = math.sin(self.animation_frame) * 2
            foliage_color = (0 + self.color_variation, 100 + self.color_variation, 0 + self.color_variation)
            
            pygame.draw.circle(screen, foliage_color, 
                             (int(pos_x + sway), int(y - trunk_height - foliage_size//2)), 
                             foliage_size)
            
        elif self.type == "billboard":
            # Billboard post
            post_width = max(5, int(8 * scale))
            post_height = max(20, int(60 * scale))
            pygame.draw.rect(screen, (150, 150, 150), 
                           (pos_x - post_width//2, y - post_height, post_width, post_height))
            
            # Billboard sign
            sign_width = max(30, int(100 * scale))
            sign_height = max(20, int(50 * scale))
            pygame.draw.rect(screen, (50, 50, 50), 
                           (pos_x - sign_width//2, y - post_height - sign_height, sign_width, sign_height))
            
            # Neon text effect
            text_color = random.choice([NEON_PINK, NEON_BLUE, NEON_GREEN])
            glow = math.sin(self.animation_frame) * 20 + 100
            text_color = (min(255, text_color[0] + glow), 
                         min(255, text_color[1] + glow), 
                         min(255, text_color[2] + glow))
            
            # Draw random neon "text" lines
            for i in range(3):
                line_y = y - post_height - sign_height + (i+1) * sign_height//4
                line_width = sign_width * 0.8
                pygame.draw.line(screen, text_color, 
                               (pos_x - line_width//2, line_y), 
                               (pos_x + line_width//2, line_y), 
                               max(1, int(3 * scale)))
            
        elif self.type == "rock":
            # Simple rock
            rock_size = max(10, int(30 * scale))
            rock_color = (100 + self.color_variation, 100 + self.color_variation, 100 + self.color_variation)
            
            # Draw irregular rock shape
            points = []
            for i in range(7):
                angle = i * 2 * math.pi / 7
                dist = rock_size * (0.8 + random.random() * 0.4)
                px = pos_x + math.cos(angle) * dist
                py = y - math.sin(angle) * dist
                points.append((px, py))
            
            pygame.draw.polygon(screen, rock_color, points)
            
        elif self.type == "building":
            # Simple building
            building_width = max(40, int(120 * scale))
            building_height = max(60, int(200 * scale))
            building_color = (80 + self.color_variation, 80 + self.color_variation, 100 + self.color_variation)
            
            pygame.draw.rect(screen, building_color, 
                           (pos_x - building_width//2, y - building_height, building_width, building_height))
            
            # Windows
            window_size = max(3, int(10 * scale))
            window_spacing = max(5, int(20 * scale))
            window_color = (200, 200, 100) if random.random() > 0.5 else (150, 150, 150)
            
            for row in range(int(building_height / window_spacing)):
                for col in range(int(building_width / window_spacing)):
                    if random.random() > 0.3:  # Some windows are dark
                        window_x = pos_x - building_width//2 + col * window_spacing + window_spacing//2
                        window_y = y - building_height + row * window_spacing + window_spacing//2
                        pygame.draw.rect(screen, window_color, 
                                       (window_x - window_size//2, window_y - window_size//2, 
                                        window_size, window_size))
        
        # Update animation
        self.animation_frame += self.animation_speed

# Power-up class
class PowerUp:
    def __init__(self, position, lane):
        self.position = position
        self.lane = lane
        self.width = 30
        self.height = 30
        self.collected = False
        self.type = random.choice(['boost', 'repair', 'shield', 'score'])
        
        # Set color based on type
        if self.type == 'boost':
            self.color = NEON_ORANGE
        elif self.type == 'repair':
            self.color = NEON_GREEN
        elif self.type == 'shield':
            self.color = NEON_BLUE
        else:  # score
            self.color = NEON_PURPLE
        
        self.animation_frame = 0
        self.animation_speed = 0.1
        
    def get_x_offset(self):
        from config import ROAD_WIDTH, LANES
        lane_width = ROAD_WIDTH / LANES
        return (self.lane * lane_width) - (lane_width)
        
    def draw(self, screen, x, y, w, h):
        # Animated floating effect
        hover_offset = math.sin(self.animation_frame) * 5
        
        # Draw power-up
        pygame.draw.circle(screen, self.color, (x, y + hover_offset), w//2)
        
        # Inner glow
        inner_color = (255, 255, 255)
        pygame.draw.circle(screen, inner_color, (x, y + hover_offset), w//4)
        
        # Outer glow
        glow_surface = pygame.Surface((w*2, h*2), pygame.SRCALPHA)
        glow_radius = w//2 + 5 + math.sin(self.animation_frame * 2) * 3
        pygame.draw.circle(glow_surface, (*self.color, 100), (w, h), glow_radius)
        screen.blit(glow_surface, (x - w, y - h + hover_offset))
        
        # Icon based on type
        if self.type == 'boost':
            # Lightning bolt
            points = [
                (x - w//6, y - h//4 + hover_offset),
                (x + w//8, y - h//8 + hover_offset),
                (x - w//8, y + h//8 + hover_offset),
                (x + w//6, y + h//4 + hover_offset)
            ]
            pygame.draw.lines(screen, (0, 0, 0), False, points, 2)
        elif self.type == 'repair':
            # Plus sign
            pygame.draw.line(screen, (0, 0, 0), 
                           (x, y - h//6 + hover_offset), 
                           (x, y + h//6 + hover_offset), 2)
            pygame.draw.line(screen, (0, 0, 0), 
                           (x - w//6, y + hover_offset), 
                           (x + w//6, y + hover_offset), 2)
        elif self.type == 'shield':
            # Shield icon
            pygame.draw.arc(screen, (0, 0, 0), 
                          (x - w//4, y - h//4 + hover_offset, w//2, h//2), 
                          math.pi, 0, 2)
        else:  # score
            # Star shape
            pygame.draw.circle(screen, (0, 0, 0), (x, y + hover_offset), w//8)
        
        # Update animation
        self.animation_frame += self.animation_speed