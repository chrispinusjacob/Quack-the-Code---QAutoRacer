import pygame
import sys
import math
import random
import numpy as np
import os
import time
from pygame.locals import *

# Initialize pygame with better defaults
pygame.mixer.pre_init(44100, -16, 2, 2048)  # Setup for less sound lag
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
ROAD_WIDTH = 2000
SEGMENT_LENGTH = 200
RUMBLE_LENGTH = 3
LANES = 3

# Advanced configuration
CONFIG = {
    "difficulty_scaling": 0.0001,  # How quickly the game gets harder
    "max_obstacles": 30,           # Maximum obstacles on screen
    "draw_distance": 300,          # How far ahead to render (segments)
    "fog_density": 5,              # Fog effect intensity
    "camera_height": 1000,         # Camera height above road
    "camera_depth": 0.84,          # Camera depth (field of view)
    "centrifugal_factor": 0.3,     # How much curves pull the car
    "offroad_deceleration": 0.95,  # Speed multiplier when off road
    "night_mode": False,           # Night mode toggle
    "debug_mode": False            # Debug information toggle
}

# Colors
SKY = (10, 10, 40)
NIGHT_SKY = (5, 5, 20)
GROUND = (16, 16, 16)
RUMBLE_LIGHT = (255, 255, 255)
RUMBLE_DARK = (0, 0, 0)
ROAD = (100, 100, 100)
ROAD_NIGHT = (70, 70, 70)
GRASS_LIGHT = (16, 200, 16)
GRASS_DARK = (0, 154, 0)
GRASS_NIGHT_LIGHT = (8, 100, 8)
GRASS_NIGHT_DARK = (0, 77, 0)
LANE_MARKER = (255, 255, 255)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (0, 191, 255)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (138, 43, 226)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)

# Color schemes
COLOR_SCHEMES = {
    "synthwave": {
        "sky": SKY,
        "ground": GROUND,
        "road": ROAD,
        "rumble_light": RUMBLE_LIGHT,
        "rumble_dark": RUMBLE_DARK,
        "grass_light": GRASS_LIGHT,
        "grass_dark": GRASS_DARK,
        "lane": LANE_MARKER,
        "car": NEON_PINK,
        "obstacles": [NEON_BLUE, NEON_GREEN, NEON_PURPLE, NEON_YELLOW]
    },
    "night": {
        "sky": NIGHT_SKY,
        "ground": GROUND,
        "road": ROAD_NIGHT,
        "rumble_light": RUMBLE_LIGHT,
        "rumble_dark": RUMBLE_DARK,
        "grass_light": GRASS_NIGHT_LIGHT,
        "grass_dark": GRASS_NIGHT_DARK,
        "lane": LANE_MARKER,
        "car": NEON_BLUE,
        "obstacles": [NEON_PINK, NEON_ORANGE, NEON_PURPLE, NEON_GREEN]
    }
}

# Set up the display with more options
flags = pygame.HWSURFACE | pygame.DOUBLEBUF
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
pygame.display.set_caption("QAutoRacer - Synthwave Edition")
icon = pygame.Surface((32, 32))
icon.fill(NEON_PINK)
pygame.draw.rect(icon, NEON_BLUE, (8, 8, 16, 16))
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")

# Create directories if they don't exist
os.makedirs(SOUND_DIR, exist_ok=True)

# Global variables
high_score = 0
current_color_scheme = "synthwave"

# Utility functions
def ease_in_out(t):
    """Smooth easing function for transitions"""
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    """Linear interpolation between a and b"""
    return a + (b - a) * t

def get_color_scheme():
    """Get current color scheme based on settings"""
    if CONFIG["night_mode"]:
        return COLOR_SCHEMES["night"]
    return COLOR_SCHEMES["synthwave"]

# Game state
class GameState:
    def __init__(self):
        self.position = 0
        self.player_x = 0
        self.player_y = 0
        self.speed = 0
        self.max_speed = 300
        self.acceleration = 0.85
        self.deceleration = -0.3
        self.handling = 0.35
        self.centrifugal = CONFIG["centrifugal_factor"]
        self.score = 0
        self.distance = 0
        self.curvature = 0
        self.track_curvature = []
        self.hills = []
        self.track_width = []  # Variable track width
        self.track_sprites = []  # Decorative sprites along the track
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        self.last_score_milestone = 0
        self.boost = 0  # Boost meter (0-100)
        self.boost_cooldown = 0
        self.offroad = False  # Whether player is off the road
        self.drift = 0  # Drift effect
        self.generate_track(10000)  # Longer track for extended gameplay
        
    def generate_track(self, length):
        # Generate a series of track segments with varying curvature
        self.track_curvature = [0] * length
        self.hills = [0] * length
        self.track_width = [1.0] * length  # Default width multiplier
        self.track_sprites = [None] * length
        
        # Create track sections with different characteristics
        section_types = ["straight", "curves", "hills", "narrow", "wide", "mixed"]
        section_length = 200  # Base section length
        
        pos = 0
        while pos < length:
            # Choose a section type
            section_type = random.choice(section_types)
            # Vary section length
            current_section_length = section_length + random.randint(-50, 100)
            current_section_length = min(current_section_length, length - pos)
            
            if section_type == "straight":
                # Straight section with minimal curves
                for i in range(current_section_length):
                    if pos + i < length:
                        self.track_curvature[pos + i] = 0
                        self.hills[pos + i] = 0
                        
            elif section_type == "curves":
                # Section with pronounced curves
                curve_count = random.randint(1, 3)
                sub_length = current_section_length // curve_count
                
                for c in range(curve_count):
                    curve = random.uniform(-0.8, 0.8)  # Stronger curves
                    for i in range(sub_length):
                        idx = pos + c * sub_length + i
                        if idx < length:
                            # Smooth curve using ease in/out
                            t = i / sub_length
                            ease = ease_in_out(t)
                            self.track_curvature[idx] = curve * math.sin(math.pi * ease)
                            
            elif section_type == "hills":
                # Section with pronounced hills
                hill_count = random.randint(1, 4)
                sub_length = current_section_length // hill_count
                
                for h in range(hill_count):
                    hill = random.uniform(-0.1, 0.1)  # Stronger hills
                    for i in range(sub_length):
                        idx = pos + h * sub_length + i
                        if idx < length:
                            # Smooth hill using ease in/out
                            t = i / sub_length
                            ease = ease_in_out(t)
                            self.hills[idx] = hill * math.sin(math.pi * ease)
                            
            elif section_type == "narrow":
                # Section with narrower track
                for i in range(current_section_length):
                    idx = pos + i
                    if idx < length:
                        # Gradually narrow the track
                        t = i / current_section_length
                        ease = ease_in_out(t)
                        if i < current_section_length / 2:
                            self.track_width[idx] = lerp(1.0, 0.7, ease * 2)
                        else:
                            self.track_width[idx] = lerp(0.7, 1.0, (ease - 0.5) * 2)
                            
            elif section_type == "wide":
                # Section with wider track
                for i in range(current_section_length):
                    idx = pos + i
                    if idx < length:
                        # Gradually widen the track
                        t = i / current_section_length
                        ease = ease_in_out(t)
                        if i < current_section_length / 2:
                            self.track_width[idx] = lerp(1.0, 1.3, ease * 2)
                        else:
                            self.track_width[idx] = lerp(1.3, 1.0, (ease - 0.5) * 2)
                            
            elif section_type == "mixed":
                # Mixed section with both curves and hills
                curve = random.uniform(-0.6, 0.6)
                hill = random.uniform(-0.08, 0.08)
                
                for i in range(current_section_length):
                    idx = pos + i
                    if idx < length:
                        t = i / current_section_length
                        ease = ease_in_out(t)
                        self.track_curvature[idx] = curve * math.sin(math.pi * ease)
                        self.hills[idx] = hill * math.cos(math.pi * ease)
            
            # Add decorative sprites occasionally
            if random.random() < 0.3:  # 30% chance for decorations
                sprite_pos = pos + random.randint(0, current_section_length - 1)
                if sprite_pos < length:
                    side = random.choice([-1, 1])  # Left or right side
                    sprite_type = random.choice(["tree", "billboard", "rock", "building"])
                    self.track_sprites[sprite_pos] = (sprite_type, side)
            
            pos += current_section_length
    
    def update(self, dt):
        """Update game state with delta time for consistent physics"""
        # Apply difficulty scaling
        difficulty = 1.0 + (self.distance / 10000) * CONFIG["difficulty_scaling"]
        
        # Check if player is off-road
        road_width = ROAD_WIDTH * self.track_width[int(self.position / SEGMENT_LENGTH) % len(self.track_width)]
        self.offroad = abs(self.player_x) > road_width / 2000
        
        # Apply off-road penalty
        if self.offroad and self.speed > 0:
            self.speed *= CONFIG["offroad_deceleration"]
        
        # Update boost cooldown
        if self.boost_cooldown > 0:
            self.boost_cooldown -= dt
        
        # Gradually reduce boost
        if self.boost > 0:
            self.boost = max(0, self.boost - dt * 10)  # Drain boost over time
        
        # Update drift effect
        self.drift *= 0.95  # Decay drift effect

# Particle system for visual effects
class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_particle(self, x, y, color, size, life, velocity_x, velocity_y, decay=0.95):
        self.particles.append({
            'x': x, 'y': y,
            'color': color,
            'size': size,
            'life': life,
            'velocity_x': velocity_x,
            'velocity_y': velocity_y,
            'decay': decay
        })
    
    def update(self):
        # Update and remove dead particles
        new_particles = []
        for p in self.particles:
            p['x'] += p['velocity_x']
            p['y'] += p['velocity_y']
            p['life'] -= 1
            p['size'] *= p['decay']
            
            if p['life'] > 0 and p['size'] > 0.5:
                new_particles.append(p)
        
        self.particles = new_particles
    
    def draw(self):
        for p in self.particles:
            alpha = min(255, int(p['life'] * 5))
            color_with_alpha = (*p['color'], alpha)
            
            # Create a surface for the particle with alpha
            particle_surface = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color_with_alpha, (p['size'], p['size']), p['size'])
            
            # Blit the particle
            screen.blit(particle_surface, (int(p['x'] - p['size']), int(p['y'] - p['size'])))

# Player car with advanced features
class Car:
    def __init__(self):
        self.width = 80
        self.height = 40
        self.base_color = NEON_PINK
        self.color = self.base_color
        self.exhaust_particles = ParticleSystem()
        self.boost_particles = ParticleSystem()
        self.skid_particles = ParticleSystem()
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.wheel_rotation = 0
        self.suspension_compression = 0
        self.damage = 0  # 0-100 damage level
        self.flash_timer = 0
        
    def update(self, speed_ratio, drift, offroad, boosting):
        # Update animation frame
        self.animation_frame += self.animation_speed * speed_ratio
        
        # Update wheel rotation based on speed
        self.wheel_rotation += speed_ratio * 15
        self.wheel_rotation %= 360
        
        # Update suspension based on hills and offroad
        target_compression = 0
        if offroad:
            target_compression = random.uniform(-3, 3)
        self.suspension_compression = lerp(self.suspension_compression, target_compression, 0.2)
        
        # Update color based on damage
        if self.flash_timer > 0:
            self.flash_timer -= 1
            self.color = NEON_RED if self.flash_timer % 4 < 2 else self.base_color
        else:
            damage_factor = self.damage / 100
            self.color = (
                lerp(self.base_color[0], 150, damage_factor),
                lerp(self.base_color[1], 150, damage_factor),
                lerp(self.base_color[2], 150, damage_factor)
            )
        
        # Generate exhaust particles
        if speed_ratio > 0.1:
            particle_count = int(speed_ratio * 2)
            for _ in range(particle_count):
                self.exhaust_particles.add_particle(
                    SCREEN_WIDTH // 2 - self.width // 3,
                    SCREEN_HEIGHT - 140 + self.suspension_compression,
                    (100, 100, 100),
                    random.uniform(2, 4),
                    random.randint(10, 20),
                    random.uniform(-1, -0.5),
                    random.uniform(-0.5, 0.5)
                )
        
        # Generate boost particles
        if boosting:
            for _ in range(5):
                self.boost_particles.add_particle(
                    SCREEN_WIDTH // 2 - self.width // 2,
                    SCREEN_HEIGHT - 150 + self.suspension_compression,
                    (255, random.randint(100, 200), 0),
                    random.uniform(3, 6),
                    random.randint(15, 30),
                    random.uniform(-3, -1),
                    random.uniform(-1, 1)
                )
        
        # Generate skid particles when drifting
        if abs(drift) > 0.5:
            side = 1 if drift > 0 else -1
            for _ in range(2):
                self.skid_particles.add_particle(
                    SCREEN_WIDTH // 2 + side * self.width // 3,
                    SCREEN_HEIGHT - 130 + self.suspension_compression,
                    (50, 50, 50),
                    random.uniform(2, 5),
                    random.randint(20, 40),
                    random.uniform(-0.5, 0.5),
                    random.uniform(-0.2, 0.2)
                )
        
        # Update all particle systems
        self.exhaust_particles.update()
        self.boost_particles.update()
        self.skid_particles.update()
    
    def take_damage(self, amount):
        self.damage = min(100, self.damage + amount)
        self.flash_timer = 20  # Flash for 20 frames
        
    def repair(self, amount):
        self.damage = max(0, self.damage - amount)
        
    def draw(self, x, y, speed_ratio, drift=0, boosting=False):
        # Apply drift to visual position
        visual_x = x + drift * 10
        
        # Draw particles first (behind car)
        self.exhaust_particles.draw()
        self.boost_particles.draw()
        self.skid_particles.draw()
        
        # Calculate car position with suspension
        car_y = SCREEN_HEIGHT - 150 + self.suspension_compression
        
        # Draw car shadow
        shadow_offset = 5 + int(speed_ratio * 3)
        shadow_rect = pygame.Rect(
            SCREEN_WIDTH // 2 + visual_x - self.width // 2 + shadow_offset,
            car_y - self.height // 2 + shadow_offset,
            self.width,
            self.height
        )
        pygame.draw.rect(screen, (0, 0, 0, 128), shadow_rect, border_radius=10)
        
        # Draw car body with slight tilt based on turning
        car_rect = pygame.Rect(
            SCREEN_WIDTH // 2 + visual_x - self.width // 2,
            car_y - self.height // 2,
            self.width,
            self.height
        )
        
        # Create a surface for the car to allow rotation
        car_surface = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
        car_body_rect = pygame.Rect(10, 10, self.width, self.height)
        pygame.draw.rect(car_surface, self.color, car_body_rect, border_radius=10)
        
        # Add racing stripes if not damaged
        if self.damage < 50:
            stripe_color = (255, 255, 255)
            pygame.draw.rect(car_surface, stripe_color, 
                            (10 + self.width // 4, 10, self.width // 8, self.height), 
                            border_radius=5)
            pygame.draw.rect(car_surface, stripe_color, 
                            (10 + self.width // 2 + self.width // 8, 10, self.width // 8, self.height), 
                            border_radius=5)
        
        # Draw windshield
        windshield = pygame.Rect(
            10 + self.width // 4,
            10 + 5,
            self.width // 2,
            self.height // 2 - 10
        )
        pygame.draw.rect(car_surface, (0, 0, 0), windshield, border_radius=5)
        
        # Add headlights
        headlight_size = 8
        pygame.draw.circle(car_surface, (255, 255, 200), 
                          (10 + self.width // 6, 10 + self.height // 2), headlight_size)
        pygame.draw.circle(car_surface, (255, 255, 200), 
                          (10 + self.width - self.width // 6, 10 + self.height // 2), headlight_size)
        
        # Add taillights
        taillight_size = 6
        brake_color = (255, 50, 50) if speed_ratio < 0.2 else (200, 0, 0)
        pygame.draw.circle(car_surface, brake_color, 
                          (10 + self.width // 6, 10 + self.height - 5), taillight_size)
        pygame.draw.circle(car_surface, brake_color, 
                          (10 + self.width - self.width // 6, 10 + self.height - 5), taillight_size)
        
        # Rotate car slightly based on drift
        rotation_angle = -drift * 5  # Negative because pygame rotation is clockwise
        rotated_car = pygame.transform.rotate(car_surface, rotation_angle)
        
        # Get the rect of the rotated surface
        rotated_rect = rotated_car.get_rect(center=car_rect.center)
        
        # Draw the rotated car
        screen.blit(rotated_car, rotated_rect.topleft)
        
        # Draw wheels with rotation
        wheel_size = 12
        wheel_offset_x = self.width // 3
        wheel_offset_y = self.height // 2 + 5
        
        # Function to draw a wheel with rotation
        def draw_wheel(x, y, size, rotation):
            wheel_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            pygame.draw.circle(wheel_surface, (30, 30, 30), (size, size), size)
            
            # Draw wheel details (spokes)
            for i in range(4):
                angle = math.radians(rotation + i * 90)
                spoke_x = size + math.cos(angle) * (size - 2)
                spoke_y = size + math.sin(angle) * (size - 2)
                pygame.draw.line(wheel_surface, (80, 80, 80), (size, size), (spoke_x, spoke_y), 2)
            
            screen.blit(wheel_surface, (x - size, y - size))
        
        # Draw all wheels with rotation
        wheel_y_offset = self.suspension_compression
        
        # Front left wheel
        draw_wheel(
            int(SCREEN_WIDTH // 2 + visual_x - wheel_offset_x), 
            int(car_y + wheel_offset_y + wheel_y_offset),
            wheel_size,
            self.wheel_rotation
        )
        
        # Front right wheel
        draw_wheel(
            int(SCREEN_WIDTH // 2 + visual_x + wheel_offset_x), 
            int(car_y + wheel_offset_y + wheel_y_offset),
            wheel_size,
            self.wheel_rotation
        )
        
        # Rear left wheel
        draw_wheel(
            int(SCREEN_WIDTH // 2 + visual_x - wheel_offset_x), 
            int(car_y - wheel_offset_y + 15 + wheel_y_offset),
            wheel_size,
            self.wheel_rotation
        )
        
        # Rear right wheel
        draw_wheel(
            int(SCREEN_WIDTH // 2 + visual_x + wheel_offset_x), 
            int(car_y - wheel_offset_y + 15 + wheel_y_offset),
            wheel_size,
            self.wheel_rotation
        )
        
        # Neon underglow effect based on speed
        glow_intensity = speed_ratio + (0.5 if boosting else 0)
        glow_color = (
            min(255, self.color[0] + int(glow_intensity * 100)),
            min(255, self.color[1] + int(glow_intensity * 100)),
            min(255, self.color[2] + int(glow_intensity * 100))
        )
        
        # Create multiple glows for more intense effect
        for i in range(3):
            glow_size = self.width + 20 + (i * 10)
            glow_alpha = max(30, int(128 - i * 30))
            
            glow_surface = pygame.Surface((glow_size, 20), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surface, (*glow_color, glow_alpha), (0, 0, glow_size, 20))
            screen.blit(glow_surface, 
                       (SCREEN_WIDTH // 2 + visual_x - glow_size // 2, 
                        car_y + self.height // 2 + 5))
        
        # Draw boost flames if boosting
        if boosting:
            flame_width = self.width // 2
            flame_height = self.height // 2
            flame_points = [
                (SCREEN_WIDTH // 2 + visual_x - self.width // 2, car_y),
                (SCREEN_WIDTH // 2 + visual_x - self.width // 2 - flame_width, car_y),
                (SCREEN_WIDTH // 2 + visual_x - self.width // 2, car_y + flame_height // 2),
            ]
            pygame.draw.polygon(screen, (255, 200, 0), flame_points)
            
            # Inner flame
            inner_flame_points = [
                (SCREEN_WIDTH // 2 + visual_x - self.width // 2, car_y + 5),
                (SCREEN_WIDTH // 2 + visual_x - self.width // 2 - flame_width // 2, car_y + 5),
                (SCREEN_WIDTH // 2 + visual_x - self.width // 2, car_y + flame_height // 4),
            ]
            pygame.draw.polygon(screen, (255, 255, 200), inner_flame_points)
        
        # Draw damage effects if damaged
        if self.damage > 30:
            # Add dents and scratches
            for _ in range(int(self.damage / 10)):
                dent_x = SCREEN_WIDTH // 2 + visual_x - self.width // 2 + random.randint(0, self.width)
                dent_y = car_y - self.height // 2 + random.randint(0, self.height)
                dent_size = random.randint(2, 5)
                pygame.draw.circle(screen, (40, 40, 40), (dent_x, dent_y), dent_size)

# Obstacle class
# Sprite class for track decorations
class TrackSprite:
    def __init__(self, type, side, offset=0):
        self.type = type  # "tree", "billboard", "rock", "building"
        self.side = side  # -1 for left, 1 for right
        self.offset = offset  # Additional offset from road edge
        self.animation_frame = random.random() * 10  # Random start frame
        self.animation_speed = 0.05
        self.color_variation = random.randint(-20, 20)
    
    def draw(self, x, y, w, h, scale):
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
        lane_width = ROAD_WIDTH / LANES
        return (self.lane * lane_width) - (lane_width)
        
    def draw(self, x, y, w, h):
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

# Enhanced obstacle class
class Obstacle:
    def __init__(self, position, lane):
        self.position = position
        self.lane = lane  # -1 (left), 0 (center), 1 (right)
        self.width = 60
        self.height = 40
        self.passed = False
        self.hit = False
        self.type = random.choice(['car', 'barrier', 'truck', 'oil', 'cone'])
        
        # Color schemes based on current game settings
        scheme = get_color_scheme()
        self.color = random.choice(scheme["obstacles"])
        
        # Type-specific properties
        if self.type == 'truck':
            self.width = 80
            self.height = 60
        elif self.type == 'oil':
            self.width = 40
            self.height = 10
        elif self.type == 'cone':
            self.width = 20
            self.height = 30
            
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.particles = ParticleSystem()
        
    def update(self):
        self.animation_frame += self.animation_speed
        self.particles.update()
        
        # Generate smoke particles for damaged cars
        if self.hit and (self.type == 'car' or self.type == 'truck'):
            if random.random() > 0.7:
                self.particles.add_particle(
                    random.randint(-self.width//2, self.width//2),
                    random.randint(-self.height//2, 0),
                    (100, 100, 100),
                    random.uniform(3, 6),
                    random.randint(20, 40),
                    random.uniform(-0.5, 0.5),
                    random.uniform(-2, -1)
                )
        
    def get_x_offset(self):
        lane_width = ROAD_WIDTH / LANES
        return (self.lane * lane_width) - (lane_width)
        
    def draw(self, x, y, w, h):
        # Draw particles relative to obstacle position
        for p in self.particles.particles:
            p_x = x + p['x']
            p_y = y + p['y']
            alpha = min(255, int(p['life'] * 5))
            color_with_alpha = (*p['color'], alpha)
            
            particle_surface = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color_with_alpha, (p['size'], p['size']), p['size'])
            screen.blit(particle_surface, (int(p_x - p['size']), int(p_y - p['size'])))
        
        if self.type == 'car':
            # Draw enemy car with more detail
            car_surface = pygame.Surface((w, h), pygame.SRCALPHA)
            car_rect = pygame.Rect(0, 0, w, h)
            pygame.draw.rect(car_surface, self.color, car_rect, border_radius=5)
            
            # Windshield
            windshield = pygame.Rect(w//4, h//4, w//2, h//3)
            pygame.draw.rect(car_surface, (0, 0, 0), windshield, border_radius=3)
            
            # Headlights
            light_size = max(2, int(w * 0.1))
            pygame.draw.circle(car_surface, (255, 255, 200), (w//6, h//2), light_size)
            pygame.draw.circle(car_surface, (255, 255, 200), (w - w//6, h//2), light_size)
            
            # If hit, add damage effects
            if self.hit:
                # Dents and scratches
                for _ in range(5):
                    dent_x = random.randint(0, w)
                    dent_y = random.randint(0, h)
                    dent_size = random.randint(2, 4)
                    pygame.draw.circle(car_surface, (40, 40, 40), (dent_x, dent_y), dent_size)
            
            # Draw the car
            screen.blit(car_surface, (x - w//2, y - h//2))
            
        elif self.type == 'barrier':
            # Draw barrier with reflective stripes
            barrier_rect = pygame.Rect(x - w//2, y - h//2, w, h//2)
            pygame.draw.rect(screen, self.color, barrier_rect)
            
            # Reflective stripes that pulse
            stripe_brightness = int(128 + 127 * math.sin(self.animation_frame))
            stripe_color = (stripe_brightness, stripe_brightness, stripe_brightness)
            
            for i in range(3):
                stripe = pygame.Rect(x - w//2 + i*(w//3), y - h//2, w//6, h//2)
                pygame.draw.rect(screen, stripe_color, stripe)
                
        elif self.type == 'truck':
            # Draw truck
            truck_body = pygame.Rect(x - w//2, y - h//2, w, h//1.5)
            pygame.draw.rect(screen, self.color, truck_body, border_radius=5)
            
            # Cab
            cab_height = h//3
            cab = pygame.Rect(x - w//2, y - h//2 - cab_height, w//3, cab_height)
            pygame.draw.rect(screen, self.color, cab, border_radius=3)
            
            # Windows
            window = pygame.Rect(x - w//2 + w//20, y - h//2 - cab_height + cab_height//5, 
                               w//4, cab_height//2)
            pygame.draw.rect(screen, (0, 0, 0), window, border_radius=2)
            
            # Wheels
            wheel_size = h//6
            wheel_positions = [
                (x - w//3, y),
                (x + w//3, y),
                (x - w//3, y - h//3),
                (x + w//3, y - h//3)
            ]
            
            for wx, wy in wheel_positions:
                pygame.draw.circle(screen, (30, 30, 30), (wx, wy), wheel_size)
                pygame.draw.circle(screen, (80, 80, 80), (wx, wy), wheel_size//2)
            
            # If hit, add damage effects
            if self.hit:
                for _ in range(8):
                    dent_x = random.randint(int(x - w//2), int(x + w//2))
                    dent_y = random.randint(int(y - h//2 - cab_height), int(y))
                    dent_size = random.randint(3, 6)
                    pygame.draw.circle(screen, (40, 40, 40), (dent_x, dent_y), dent_size)
                
        elif self.type == 'oil':
            # Draw oil slick
            for i in range(3):
                size_factor = 1 - i * 0.2
                alpha = 200 - i * 50
                oil_surface = pygame.Surface((w * size_factor, h * size_factor), pygame.SRCALPHA)
                oil_color = (0, 0, 0, alpha)
                pygame.draw.ellipse(oil_surface, oil_color, (0, 0, w * size_factor, h * size_factor))
                screen.blit(oil_surface, (x - (w * size_factor)//2, y - (h * size_factor)//2))
            
            # Add shine effect
            shine_pos = (x + math.sin(self.animation_frame) * w//4, y + math.cos(self.animation_frame) * h//4)
            shine_size = max(2, int(w * 0.1))
            pygame.draw.circle(screen, (150, 150, 150, 150), shine_pos, shine_size)
            
        elif self.type == 'cone':
            # Draw traffic cone
            cone_color = (255, 100, 0)  # Orange
            
            # Base
            base_rect = pygame.Rect(x - w//2, y - h//6, w, h//3)
            pygame.draw.rect(screen, cone_color, base_rect)
            
            # Cone shape
            cone_points = [
                (x - w//2, y - h//6),
                (x + w//2, y - h//6),
                (x, y - h)
            ]
            pygame.draw.polygon(screen, cone_color, cone_points)
            
            # Reflective stripes
            stripe_brightness = int(128 + 127 * math.sin(self.animation_frame))
            stripe_color = (stripe_brightness, stripe_brightness, stripe_brightness)
            
            stripe_points1 = [
                (x - w//3, y - h//3),
                (x + w//3, y - h//3),
                (x, y - h//2)
            ]
            pygame.draw.polygon(screen, stripe_color, stripe_points1)
            
            stripe_points2 = [
                (x - w//6, y - h//1.5),
                (x + w//6, y - h//1.5),
                (x, y - h//1.2)
            ]
            pygame.draw.polygon(screen, stripe_color, stripe_points2)

# Game objects
game_state = GameState()
player_car = Car()
obstacles = []
power_ups = []
last_obstacle_pos = 0
last_powerup_pos = 0

# Game effects
screen_shake = 0
flash_effect = 0
vignette_effect = 0

# Game statistics
stats = {
    "obstacles_avoided": 0,
    "powerups_collected": 0,
    "distance_traveled": 0,
    "max_speed": 0,
    "crashes": 0,
    "game_time": 0,
    "drift_time": 0
}

# Generate initial obstacles
for i in range(10):
    pos = last_obstacle_pos + random.randint(500, 1000)
    lane = random.randint(-1, 1)
    obstacles.append(Obstacle(pos, lane))
    last_obstacle_pos = pos
    
# Generate initial power-ups
for i in range(3):
    pos = last_powerup_pos + random.randint(1000, 2000)
    lane = random.randint(-1, 1)
    power_ups.append(PowerUp(pos, lane))
    last_powerup_pos = pos
# Function to project 3D points to 2D screen with advanced camera options
def project(point_x, point_y, point_z, camera_shake=0):
    camera_height = CONFIG["camera_height"]
    camera_depth = CONFIG["camera_depth"]
    
    # Apply camera shake if any
    if camera_shake > 0:
        shake_x = random.uniform(-camera_shake, camera_shake)
        shake_y = random.uniform(-camera_shake, camera_shake)
    else:
        shake_x = shake_y = 0
    
    # Don't divide by zero
    if point_z <= 0:
        point_z = 0.1
        
    # Apply fog effect to distant objects
    fog_factor = min(1.0, point_z / (CONFIG["draw_distance"] * SEGMENT_LENGTH))
    
    # Calculate scale with perspective
    scale = camera_depth / point_z
    
    # Project to screen coordinates with shake
    x = SCREEN_WIDTH / 2 + scale * point_x * SCREEN_WIDTH / 2 + shake_x
    y = SCREEN_HEIGHT / 2 - scale * (point_y - camera_height) * SCREEN_HEIGHT / 2 + shake_y
    
    return x, y, scale, fog_factor

# Draw a segment of the road with fog and lighting effects
def draw_segment(x1, y1, w1, x2, y2, w2, color, fog_factor1=0, fog_factor2=0):
    # Apply fog effect to color
    def apply_fog(color, fog_factor):
        fog_color = SKY if not CONFIG["night_mode"] else NIGHT_SKY
        r = int(lerp(color[0], fog_color[0], fog_factor * CONFIG["fog_density"]))
        g = int(lerp(color[1], fog_color[1], fog_factor * CONFIG["fog_density"]))
        b = int(lerp(color[2], fog_color[2], fog_factor * CONFIG["fog_density"]))
        return (r, g, b)
    
    # Apply fog to start and end colors
    color1 = apply_fog(color, fog_factor1)
    color2 = apply_fog(color, fog_factor2)
    
    # If colors are different, use a gradient
    if color1 != color2:
        # Create a surface for the segment
        width = max(int(x1 + w1), int(x2 + w2)) - min(int(x1 - w1), int(x2 - w2))
        height = int(y2) - int(y1)
        
        if width <= 0 or height <= 0:
            return
            
        segment_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw the segment with a vertical gradient
        for i in range(height):
            progress = i / height
            r = int(lerp(color1[0], color2[0], progress))
            g = int(lerp(color1[1], color2[1], progress))
            b = int(lerp(color1[2], color2[2], progress))
            gradient_color = (r, g, b)
            
            # Calculate width at this y position
            segment_width = lerp(w1 * 2, w2 * 2, progress)
            segment_x = lerp(0, width - segment_width, progress)
            
            pygame.draw.line(segment_surface, gradient_color, 
                           (segment_x, i), (segment_x + segment_width, i))
        
        # Draw the surface
        screen.blit(segment_surface, (min(int(x1 - w1), int(x2 - w2)), int(y1)))
    else:
        # Draw a simple trapezoid if colors are the same
        points = [
            (x1 - w1, y1),
            (x1 + w1, y1),
            (x2 + w2, y2),
            (x2 - w2, y2)
        ]
        pygame.draw.polygon(screen, color1, points)

# Draw stars for night sky
def draw_stars(position):
    # Use position to make stars move slightly
    star_offset = position / 1000
    
    # Create a set of fixed stars
    for i in range(100):
        # Use deterministic positions based on index
        x = ((i * 263) % SCREEN_WIDTH + star_offset) % SCREEN_WIDTH
        y = ((i * 173) % (SCREEN_HEIGHT // 2))
        
        # Twinkle effect
        brightness = 128 + int(127 * math.sin(i + time.time() * (i % 5 + 1)))
        size = 1 + (i % 3)
        
        pygame.draw.circle(screen, (brightness, brightness, brightness), (int(x), int(y)), size)

# Draw the road with advanced visual effects
def draw_road(position, player_x, curvature, hill, dt):
    # Get color scheme
    colors = get_color_scheme()
    
    # Draw sky
    screen.fill(colors["sky"])
    
    # Draw stars at night
    if CONFIG["night_mode"]:
        draw_stars(position)
    
    # Draw sun or moon
    celestial_y = SCREEN_HEIGHT // 4
    celestial_radius = 50
    
    if CONFIG["night_mode"]:
        # Moon with craters
        moon_color = (200, 200, 220)
        pygame.draw.circle(screen, moon_color, (SCREEN_WIDTH - celestial_radius - 50, celestial_y), celestial_radius)
        
        # Moon craters
        for i in range(5):
            crater_size = random.randint(5, 15)
            crater_x = SCREEN_WIDTH - celestial_radius - 50 + random.randint(-30, 30)
            crater_y = celestial_y + random.randint(-30, 30)
            # Only draw if within moon circle
            if math.sqrt((crater_x - (SCREEN_WIDTH - celestial_radius - 50))**2 + 
                         (crater_y - celestial_y)**2) < celestial_radius - crater_size:
                pygame.draw.circle(screen, (170, 170, 190), (crater_x, crater_y), crater_size)
    else:
        # Sun with corona
        sun_color = (255, 60, 60)
        
        # Draw sun rays
        for i in range(12):
            angle = i * math.pi / 6
            ray_length = celestial_radius + random.randint(10, 30)
            end_x = SCREEN_WIDTH - celestial_radius - 50 + math.cos(angle) * ray_length
            end_y = celestial_y + math.sin(angle) * ray_length
            pygame.draw.line(screen, sun_color, 
                           (SCREEN_WIDTH - celestial_radius - 50, celestial_y), 
                           (end_x, end_y), 3)
        
        pygame.draw.circle(screen, sun_color, (SCREEN_WIDTH - celestial_radius - 50, celestial_y), celestial_radius)
    
    # Draw grid horizon (synthwave style)
    horizon_y = SCREEN_HEIGHT // 2
    grid_spacing = 20
    grid_depth = 20
    
    # Horizontal grid lines with animation
    grid_offset = (position / 100) % grid_spacing
    for i in range(grid_depth):
        y = horizon_y + i * (SCREEN_HEIGHT - horizon_y) / grid_depth + grid_offset
        if y >= horizon_y:
            intensity = 1 - (i / grid_depth)
            color = (int(NEON_PINK[0] * intensity), int(NEON_PINK[1] * intensity), int(NEON_PINK[2] * intensity))
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y), 2)
    
    # Vertical grid lines with perspective and animation
    for i in range(-10, 11):
        offset = (position / 50) % (grid_spacing * 2) - grid_spacing
        start_x = SCREEN_WIDTH // 2 + i * grid_spacing + offset
        end_x = SCREEN_WIDTH // 2 + i * grid_spacing * 10 + offset * 10
        pygame.draw.line(screen, NEON_PINK, (start_x, horizon_y), (end_x, SCREEN_HEIGHT), 2)
    
    # Draw mountains in background with parallax effect
    mountain_parallax = position / 500
    mountain_colors = [(40, 10, 40), (60, 20, 60), (30, 5, 30)]
    
    for layer in range(3):
        layer_parallax = mountain_parallax * (3 - layer) * 0.5
        mountain_color = mountain_colors[layer]
        
        for i in range(8):
            # Use deterministic heights and widths based on index for consistency
            height = 50 + ((i * 17 + layer * 37) % 100)
            width = 200 + ((i * 23 + layer * 13) % 200)
            x = (i * width // 2) - (layer_parallax % width)
            
            while x < SCREEN_WIDTH:
                points = [
                    (x, horizon_y),
                    (x + width // 2, horizon_y - height),
                    (x + width, horizon_y)
                ]
                pygame.draw.polygon(screen, mountain_color, points)
                x += width
    
    # Draw city skyline if in night mode
    if CONFIG["night_mode"]:
        building_colors = [(20, 20, 40), (30, 30, 50), (10, 10, 30)]
        building_parallax = position / 400
        
        for i in range(15):
            # Deterministic building properties
            height = 30 + ((i * 13) % 70)
            width = 40 + ((i * 17) % 60)
            x = (i * width // 2) - (building_parallax % (width * 8))
            color = building_colors[i % len(building_colors)]
            
            while x < SCREEN_WIDTH:
                # Building
                pygame.draw.rect(screen, color, (x, horizon_y - height, width, height))
                
                # Windows
                window_size = 4
                window_spacing = 10
                window_color = (200, 200, 100) if random.random() > 0.5 else (150, 150, 150)
                
                for row in range(int(height / window_spacing)):
                    for col in range(int(width / window_spacing)):
                        if random.random() > 0.3:  # Some windows are dark
                            window_x = x + col * window_spacing + window_spacing//2
                            window_y = horizon_y - height + row * window_spacing + window_spacing//2
                            pygame.draw.rect(screen, window_color, 
                                           (window_x - window_size//2, window_y - window_size//2, 
                                            window_size, window_size))
                
                x += width + 10
    
    # Draw road segments with advanced rendering
    base_segment = int(position / SEGMENT_LENGTH)
    
    # Draw from back to front (painter's algorithm)
    for i in range(CONFIG["draw_distance"]):
        segment = (base_segment + i) % len(game_state.track_curvature)
        
        # Calculate segment curve and hill
        curve = game_state.track_curvature[segment] * player_x
        hill = game_state.hills[segment]
        
        # Get track width for this segment
        track_width_multiplier = game_state.track_width[segment]
        
        # Project 3D points to 2D with camera shake
        p1_x = curve
        p1_y = hill
        p1_z = i * SEGMENT_LENGTH
        
        p2_x = game_state.track_curvature[(segment + 1) % len(game_state.track_curvature)] * player_x
        p2_y = game_state.hills[(segment + 1) % len(game_state.hills)]
        p2_z = (i + 1) * SEGMENT_LENGTH
        
        # Project to screen coordinates
        x1, y1, s1, fog1 = project(p1_x, p1_y, p1_z, screen_shake)
        x2, y2, s2, fog2 = project(p2_x, p2_y, p2_z, screen_shake)
        
        # Skip if behind camera or off screen
        if y1 >= SCREEN_HEIGHT or y2 < 0:
            continue
            
        # Calculate road width with track width multiplier
        w1 = s1 * ROAD_WIDTH * track_width_multiplier / 2
        w2 = s2 * ROAD_WIDTH * track_width_multiplier / 2
        
        # Determine segment color (alternate for rumble strips)
        rumble_color = colors["rumble_light"] if (segment // RUMBLE_LENGTH) % 2 == 0 else colors["rumble_dark"]
        road_color = colors["road"]
        grass_color = colors["grass_light"] if (segment // RUMBLE_LENGTH) % 2 == 0 else colors["grass_dark"]
        
        # Draw segment layers (grass, rumble, road) with fog
        # Grass
        draw_segment(x1, y1, w1 * 2, x2, y2, w2 * 2, grass_color, fog1, fog2)
        # Rumble strips
        draw_segment(x1, y1, w1 * 1.2, x2, y2, w2 * 1.2, rumble_color, fog1, fog2)
        # Road
        draw_segment(x1, y1, w1, x2, y2, w2, road_color, fog1, fog2)
        
        # Draw lane markers
        if (segment // RUMBLE_LENGTH) % 2 == 0:
            lane_w1 = w1 * 0.05
            lane_w2 = w2 * 0.05
            lane_x1 = x1 - w1 * 0.5 + lane_w1
            lane_x2 = x2 - w2 * 0.5 + lane_w2
            
            # Draw lane markers for each lane
            for lane in range(LANES - 1):
                lane_offset = (lane + 1) * (1.0 / LANES)
                draw_segment(
                    x1 + w1 * lane_offset, y1, lane_w1,
                    x2 + w2 * lane_offset, y2, lane_w2,
                    colors["lane"],
                    fog1, fog2
                )
        
        # Draw track sprites (decorations)
        sprite = game_state.track_sprites[segment]
        if sprite:
            sprite_type, sprite_side = sprite
            track_sprite = TrackSprite(sprite_type, sprite_side)
            track_sprite.draw(x1 + sprite_side * w1 * 1.5, y1, w1, w1, s1)
        
        # Draw obstacles in this segment
        for obstacle in obstacles:
            obstacle_segment = int((obstacle.position - position) / SEGMENT_LENGTH)
            if obstacle_segment == i:
                # Calculate obstacle position
                obstacle_x = obstacle.get_x_offset() * s1
                obstacle_width = obstacle.width * s1
                obstacle_height = obstacle.height * s1
                
                # Update and draw the obstacle
                obstacle.update()
                obstacle.draw(x1 + obstacle_x, y1, obstacle_width, obstacle_height)
        
        # Draw power-ups in this segment
        for power_up in power_ups:
            if not power_up.collected:
                powerup_segment = int((power_up.position - position) / SEGMENT_LENGTH)
                if powerup_segment == i:
                    # Calculate power-up position
                    powerup_x = power_up.get_x_offset() * s1
                    powerup_width = power_up.width * s1
                    powerup_height = power_up.height * s1
                    
                    # Draw the power-up
                    power_up.draw(x1 + powerup_x, y1, powerup_width, powerup_height)
    
    # Draw special effects
    
    # Flash effect (for collisions, power-ups)
    if flash_effect > 0:
        flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        flash_alpha = min(255, flash_effect * 255)
        flash_surface.fill((255, 255, 255, flash_alpha))
        screen.blit(flash_surface, (0, 0))
    
    # Vignette effect (for focus, damage)
    if vignette_effect > 0:
        vignette_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        vignette_color = (0, 0, 0, int(vignette_effect * 150))
        
        # Draw a radial gradient
        for i in range(10):
            size = SCREEN_WIDTH + SCREEN_HEIGHT - i * 50
            alpha = int(vignette_effect * (15 - i) * 10)
            if alpha <= 0:
                continue
                
            pygame.draw.circle(vignette_surface, (0, 0, 0, alpha), 
                             (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), size // 2)
        
        screen.blit(vignette_surface, (0, 0))
    
    # Debug information
    if CONFIG["debug_mode"]:
        debug_font = pygame.font.SysFont("Courier New", 14)
        debug_info = [
            f"FPS: {int(clock.get_fps())}",
            f"Position: {int(position)}",
            f"Segment: {base_segment}",
            f"Curvature: {curvature:.2f}",
            f"Hill: {hill:.2f}",
            f"Player X: {player_x:.2f}",
            f"Obstacles: {len(obstacles)}",
            f"Power-ups: {len(power_ups)}",
            f"Track Width: {track_width_multiplier:.2f}"
        ]
        
        for i, info in enumerate(debug_info):
            debug_text = debug_font.render(info, True, (255, 255, 255))
            screen.blit(debug_text, (10, SCREEN_HEIGHT - 20 * (len(debug_info) - i)))

# Draw advanced HUD (Heads-Up Display)
def draw_hud(speed, score, boost=0, damage=0, game_over=False):
    # Get a high-quality font
    font = pygame.font.SysFont("Arial", 24, bold=True)
    small_font = pygame.font.SysFont("Arial", 18)
    
    # Create a semi-transparent HUD background
    hud_surface = pygame.Surface((SCREEN_WIDTH, 80), pygame.SRCALPHA)
    hud_surface.fill((0, 0, 0, 128))
    screen.blit(hud_surface, (0, 0))
    
    # Speed display with animation
    speed_kmh = int(speed * 3.6)  # Convert to km/h
    speed_text = f"SPEED: {speed_kmh} KM/H"
    
    # Animate speed text color based on speed
    speed_ratio = min(1.0, speed / game_state.max_speed)
    if speed_ratio > 0.8:
        # Pulse red at high speeds
        pulse = (math.sin(time.time() * 10) + 1) / 2
        speed_color = (255, int(255 * (1 - pulse)), int(255 * (1 - pulse)))
    else:
        # Gradient from green to yellow to red
        if speed_ratio < 0.5:
            # Green to yellow
            green_to_yellow = speed_ratio * 2
            speed_color = (int(255 * green_to_yellow), 255, 0)
        else:
            # Yellow to red
            yellow_to_red = (speed_ratio - 0.5) * 2
            speed_color = (255, int(255 * (1 - yellow_to_red)), 0)
    
    speed_surface = font.render(speed_text, True, speed_color)
    screen.blit(speed_surface, (20, 20))
    
    # Score display with animation for milestones
    score_int = int(score)
    score_text = f"SCORE: {score_int}"
    
    # Check for score milestone
    milestone_animation = 0
    if score_int > 0 and score_int % 1000 == 0 and score_int != game_state.last_score_milestone:
        milestone_animation = math.sin(time.time() * 10) * 10
        game_state.last_score_milestone = score_int
    
    score_size = 24 + int(milestone_animation)
    score_font = pygame.font.SysFont("Arial", score_size, bold=True)
    score_surface = score_font.render(score_text, True, NEON_PINK)
    screen.blit(score_surface, (20, 50))
    
    # High score display
    global high_score
    if score_int > high_score:
        high_score = score_int
        
    high_score_text = f"HIGH: {high_score}"
    high_score_surface = small_font.render(high_score_text, True, NEON_BLUE)
    screen.blit(high_score_surface, (200, 55))
    
    # Boost meter
    boost_width = 150
    boost_height = 15
    boost_x = SCREEN_WIDTH - boost_width - 20
    boost_y = 20
    
    # Boost background
    pygame.draw.rect(screen, (50, 50, 50), (boost_x, boost_y, boost_width, boost_height), border_radius=3)
    
    # Boost fill
    if boost > 0:
        boost_fill_width = int(boost_width * (boost / 100))
        
        # Gradient color based on boost amount
        if boost < 30:
            boost_color = NEON_RED
        elif boost < 70:
            boost_color = NEON_YELLOW
        else:
            boost_color = NEON_GREEN
            
        pygame.draw.rect(screen, boost_color, 
                       (boost_x, boost_y, boost_fill_width, boost_height), 
                       border_radius=3)
    
    # Boost text
    boost_text = "BOOST"
    boost_text_surface = small_font.render(boost_text, True, (255, 255, 255))
    screen.blit(boost_text_surface, 
               (boost_x + boost_width//2 - boost_text_surface.get_width()//2, 
                boost_y + boost_height//2 - boost_text_surface.get_height()//2))
    
    # Damage meter
    damage_width = 150
    damage_height = 15
    damage_x = SCREEN_WIDTH - damage_width - 20
    damage_y = 45
    
    # Damage background
    pygame.draw.rect(screen, (50, 50, 50), (damage_x, damage_y, damage_width, damage_height), border_radius=3)
    
    # Damage fill
    if damage > 0:
        damage_fill_width = int(damage_width * (damage / 100))
        
        # Color based on damage amount
        if damage < 30:
            damage_color = NEON_GREEN
        elif damage < 70:
            damage_color = NEON_YELLOW
        else:
            # Flashing red for critical damage
            if time.time() % 0.5 < 0.25:
                damage_color = NEON_RED
            else:
                damage_color = (150, 0, 0)
                
        pygame.draw.rect(screen, damage_color, 
                       (damage_x, damage_y, damage_fill_width, damage_height), 
                       border_radius=3)
    
    # Damage text
    damage_text = "DAMAGE"
    damage_text_surface = small_font.render(damage_text, True, (255, 255, 255))
    screen.blit(damage_text_surface, 
               (damage_x + damage_width//2 - damage_text_surface.get_width()//2, 
                damage_y + damage_height//2 - damage_text_surface.get_height()//2))
    
    # Speedometer with advanced styling
    center_x = SCREEN_WIDTH - 100
    center_y = 120
    radius = 60
    
    # Draw speedometer background with gradient
    for r in range(radius, radius-15, -1):
        alpha = int(255 * (1 - (radius - r) / 15))
        color = (30, 30, 30, alpha)
        pygame.draw.circle(screen, color, (center_x, center_y), r)
    
    # Draw speed markers with gradient colors
    for i in range(8):
        angle = math.pi * 0.75 + i * (math.pi * 1.5 / 7)
        marker_length = 10 if i % 2 == 0 else 5
        
        # Gradient color based on position
        marker_ratio = i / 7
        if marker_ratio < 0.5:
            marker_color = (int(255 * marker_ratio * 2), 255, 0)
        else:
            marker_color = (255, int(255 * (1 - (marker_ratio - 0.5) * 2)), 0)
        
        x1 = center_x + math.cos(angle) * (radius - 10)
        y1 = center_y + math.sin(angle) * (radius - 10)
        x2 = center_x + math.cos(angle) * (radius - 10 - marker_length)
        y2 = center_y + math.sin(angle) * (radius - 10 - marker_length)
        pygame.draw.line(screen, marker_color, (x1, y1), (x2, y2), 2)
        
        # Add speed numbers
        if i % 2 == 0:
            speed_value = int(i * game_state.max_speed * 3.6 / 7)  # km/h
            speed_label = small_font.render(str(speed_value), True, (200, 200, 200))
            text_x = center_x + math.cos(angle) * (radius - 25)
            text_y = center_y + math.sin(angle) * (radius - 25)
            screen.blit(speed_label, 
                       (text_x - speed_label.get_width()//2, 
                        text_y - speed_label.get_height()//2))
    
    # Draw speed needle with glow effect
    speed_ratio = min(1.0, speed / game_state.max_speed)
    angle = math.pi * 0.75 + speed_ratio * math.pi * 1.5
    
    # Needle glow
    for i in range(3):
        glow_width = 3 - i
        glow_alpha = 100 - i * 30
        glow_color = (*speed_color[:3], glow_alpha)
        
        needle_length = radius - 15 - i * 2
        x = center_x + math.cos(angle) * needle_length
        y = center_y + math.sin(angle) * needle_length
        
        # Create a surface for the glowing line
        line_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(line_surface, glow_color, (center_x, center_y), (x, y), glow_width)
        screen.blit(line_surface, (0, 0))
    
    # Needle itself
    needle_length = radius - 15
    x = center_x + math.cos(angle) * needle_length
    y = center_y + math.sin(angle) * needle_length
    pygame.draw.line(screen, speed_color, (center_x, center_y), (x, y), 2)
    
    # Center cap
    pygame.draw.circle(screen, speed_color, (center_x, center_y), 5)
    pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 2)
    
    # Current speed in center of speedometer
    current_speed_text = f"{speed_kmh}"
    current_speed_font = pygame.font.SysFont("Arial", 20, bold=True)
    current_speed_surface = current_speed_font.render(current_speed_text, True, (255, 255, 255))
    screen.blit(current_speed_surface, 
               (center_x - current_speed_surface.get_width()//2, 
                center_y + 15))
    
    # "KM/H" label
    kmh_font = pygame.font.SysFont("Arial", 12)
    kmh_surface = kmh_font.render("KM/H", True, (200, 200, 200))
    screen.blit(kmh_surface, 
               (center_x - kmh_surface.get_width()//2, 
                center_y + 35))
    
    # Mini-map (top-down view of upcoming track)
    map_width = 100
    map_height = 50
    map_x = center_x - map_width // 2
    map_y = center_y + 50
    
    # Map background
    pygame.draw.rect(screen, (30, 30, 30), (map_x, map_y, map_width, map_height), border_radius=5)
    
    # Draw upcoming track segments on mini-map
    map_segments = 100
    base_segment = int(game_state.position / SEGMENT_LENGTH)
    
    for i in range(map_segments):
        segment = (base_segment + i) % len(game_state.track_curvature)
        curve = game_state.track_curvature[segment]
        
        # Calculate position on mini-map
        map_pos_y = map_y + (i * map_height / map_segments)
        map_pos_x = map_x + map_width / 2 + curve * 20  # Scale curve for visibility
        
        # Draw track point
        pygame.draw.circle(screen, (100, 100, 100), (int(map_pos_x), int(map_pos_y)), 1)
    
    # Player position on mini-map
    player_map_x = map_x + map_width / 2 + game_state.player_x * 5
    player_map_y = map_y + 10
    pygame.draw.circle(screen, NEON_PINK, (int(player_map_x), int(player_map_y)), 3)
    
    # Game over message with advanced styling
    if game_over:
        # Create overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Game over text with glow effect
        font_large = pygame.font.SysFont("Arial", 72, bold=True)
        game_over_text = "GAME OVER"
        
        # Pulse effect
        pulse = (math.sin(time.time() * 3) + 1) / 2
        glow_size = int(5 + pulse * 10)
        
        # Draw glow
        for i in range(glow_size, 0, -1):
            alpha = int(200 * (1 - i / glow_size))
            glow_color = (NEON_PINK[0], NEON_PINK[1], NEON_PINK[2], alpha)
            glow_text = font_large.render(game_over_text, True, glow_color)
            screen.blit(glow_text, 
                       (SCREEN_WIDTH // 2 - glow_text.get_width() // 2 + random.randint(-i//2, i//2), 
                        SCREEN_HEIGHT // 3 - glow_text.get_height() // 2 + random.randint(-i//2, i//2)))
        
        # Main text
        main_text = font_large.render(game_over_text, True, NEON_PINK)
        screen.blit(main_text, 
                   (SCREEN_WIDTH // 2 - main_text.get_width() // 2, 
                    SCREEN_HEIGHT // 3 - main_text.get_height() // 2))
        
        # Final score
        score_font = pygame.font.SysFont("Arial", 48)
        final_score_text = f"FINAL SCORE: {score_int}"
        final_score_surface = score_font.render(final_score_text, True, NEON_GREEN)
        screen.blit(final_score_surface, 
                   (SCREEN_WIDTH // 2 - final_score_surface.get_width() // 2, 
                    SCREEN_HEIGHT // 2 - final_score_surface.get_height() // 2))
        
        # High score
        if score_int >= high_score:
            high_score_text = "NEW HIGH SCORE!"
            high_score_color = NEON_YELLOW
            
            # Animated effect for new high score
            scale = 1.0 + math.sin(time.time() * 5) * 0.1
            high_score_font = pygame.font.SysFont("Arial", int(36 * scale), bold=True)
        else:
            high_score_text = f"HIGH SCORE: {high_score}"
            high_score_color = NEON_BLUE
            high_score_font = pygame.font.SysFont("Arial", 36)
            
        high_score_surface = high_score_font.render(high_score_text, True, high_score_color)
        screen.blit(high_score_surface, 
                   (SCREEN_WIDTH // 2 - high_score_surface.get_width() // 2, 
                    SCREEN_HEIGHT // 2 + 50))
        
        # Game statistics
        stats_font = pygame.font.SysFont("Arial", 24)
        stats_texts = [
            f"Distance: {int(stats['distance_traveled'] / 100)} km",
            f"Obstacles Avoided: {stats['obstacles_avoided']}",
            f"Power-ups Collected: {stats['powerups_collected']}",
            f"Max Speed: {int(stats['max_speed'] * 3.6)} km/h",
            f"Time: {int(stats['game_time'])} seconds"
        ]
        
        for i, stat_text in enumerate(stats_texts):
            stat_surface = stats_font.render(stat_text, True, (200, 200, 200))
            screen.blit(stat_surface, 
                       (SCREEN_WIDTH // 2 - 150, 
                        SCREEN_HEIGHT // 2 + 100 + i * 30))
        
        # Restart text with animation
        restart_text = "Press SPACE to restart"
        restart_font = pygame.font.SysFont("Arial", 30)
        
        # Pulse animation
        pulse = (math.sin(time.time() * 2) + 1) / 2
        restart_color = (
            int(NEON_GREEN[0] * (0.7 + 0.3 * pulse)),
            int(NEON_GREEN[1] * (0.7 + 0.3 * pulse)),
            int(NEON_GREEN[2] * (0.7 + 0.3 * pulse))
        )
        
        restart_surface = restart_font.render(restart_text, True, restart_color)
        screen.blit(restart_surface, 
                   (SCREEN_WIDTH // 2 - restart_surface.get_width() // 2, 
                    SCREEN_HEIGHT - 100))

# Check for collision between player and obstacles
def check_collision(player_x, position):
    # Get current segment
    base_segment = int(position / SEGMENT_LENGTH)
    
    for obstacle in obstacles:
        # Calculate distance to obstacle
        obstacle_segment = int(obstacle.position / SEGMENT_LENGTH)
        segment_diff = obstacle_segment - base_segment
        
        # Only check obstacles in front of the player and within a certain range
        if 0 <= segment_diff < 5:
            # Calculate lane positions
            lane_width = ROAD_WIDTH / LANES
            player_lane = round(player_x / lane_width)
            
            # Check if in same lane
            if obstacle.lane == player_lane and not obstacle.passed:
                obstacle.passed = True
                return True
    
    return False

# Create title screen
def draw_title_screen():
    screen.fill(SKY)
    
    # Draw grid horizon (synthwave style)
    horizon_y = SCREEN_HEIGHT // 2
    grid_spacing = 20
    grid_depth = 20
    
    # Horizontal grid lines
    for i in range(grid_depth):
        y = horizon_y + i * (SCREEN_HEIGHT - horizon_y) / grid_depth
        intensity = 1 - (i / grid_depth)
        color = (int(NEON_PINK[0] * intensity), int(NEON_PINK[1] * intensity), int(NEON_PINK[2] * intensity))
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y), 2)
    
    # Vertical grid lines with perspective
    for i in range(-10, 11):
        start_x = SCREEN_WIDTH // 2 + i * grid_spacing
        end_x = SCREEN_WIDTH // 2 + i * grid_spacing * 10
        pygame.draw.line(screen, NEON_PINK, (start_x, horizon_y), (end_x, SCREEN_HEIGHT), 2)
    
    # Draw sun
    sun_y = SCREEN_HEIGHT // 4
    sun_radius = 80
    sun_color = (255, 60, 60)
    pygame.draw.circle(screen, sun_color, (SCREEN_WIDTH - sun_radius - 50, sun_y), sun_radius)
    
    # Title text
    font_title = pygame.font.SysFont("Arial", 72, bold=True)
    font_subtitle = pygame.font.SysFont("Arial", 36)
    font_instructions = pygame.font.SysFont("Arial", 24)
    
    title_text = font_title.render("QAutoRacer", True, NEON_BLUE)
    subtitle_text = font_subtitle.render("Synthwave Edition", True, NEON_PINK)
    start_text = font_instructions.render("Press SPACE to start", True, NEON_GREEN)
    controls_text = font_instructions.render("WASD or Arrow Keys to drive", True, NEON_GREEN)
    
    # Position and draw text
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, SCREEN_HEIGHT // 3 + title_text.get_height()))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT * 2 // 3))
    screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, SCREEN_HEIGHT * 2 // 3 + start_text.get_height() + 10))
    
    # Draw car silhouette
    car_width = 120
    car_height = 60
    car_x = SCREEN_WIDTH // 2
    car_y = SCREEN_HEIGHT // 2 + 50
    
    car_points = [
        (car_x - car_width // 2, car_y),
        (car_x - car_width // 3, car_y - car_height // 2),
        (car_x + car_width // 3, car_y - car_height // 2),
        (car_x + car_width // 2, car_y),
    ]
    
    pygame.draw.polygon(screen, NEON_BLUE, car_points)
    
    # Educational note
    edu_font = pygame.font.SysFont("Arial", 16)
    edu_text1 = edu_font.render("Educational Note: This game demonstrates pseudo-3D rendering techniques", True, NEON_GREEN)
    edu_text2 = edu_font.render("used in classic racing games from the 80s and 90s.", True, NEON_GREEN)
    
    screen.blit(edu_text1, (20, SCREEN_HEIGHT - 50))
    screen.blit(edu_text2, (20, SCREEN_HEIGHT - 30))

# Sound effects
try:
    engine_sound = pygame.mixer.Sound("assets/engine.wav")
    crash_sound = pygame.mixer.Sound("assets/crash.wav")
    score_sound = pygame.mixer.Sound("assets/score.wav")
    has_sound = True
except:
    has_sound = False
    print("Sound files not found. Continuing without sound.")

# Game states
STATE_TITLE = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2

# Main game loop
def main():
    global obstacles, last_obstacle_pos
    
    game_state = GameState()
    player_car = Car()
    obstacles = []
    last_obstacle_pos = 0
    
    # Generate initial obstacles
    for i in range(10):
        pos = last_obstacle_pos + random.randint(500, 1000)
        lane = random.randint(-1, 1)
        obstacles.append(Obstacle(pos, lane))
        last_obstacle_pos = pos
    
    current_state = STATE_TITLE
    running = True
    
    # Start engine sound if available
    if has_sound:
        engine_sound.play(-1)  # Loop indefinitely
        engine_sound.set_volume(0.0)
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    if current_state == STATE_TITLE:
                        current_state = STATE_PLAYING
                        game_state = GameState()
                        obstacles = []
                        last_obstacle_pos = 0
                        
                        # Generate initial obstacles
                        for i in range(10):
                            pos = last_obstacle_pos + random.randint(500, 1000)
                            lane = random.randint(-1, 1)
                            obstacles.append(Obstacle(pos, lane))
                            last_obstacle_pos = pos
                    elif current_state == STATE_GAME_OVER:
                        current_state = STATE_PLAYING
                        game_state = GameState()
                        obstacles = []
                        last_obstacle_pos = 0
                        
                        # Generate initial obstacles
                        for i in range(10):
                            pos = last_obstacle_pos + random.randint(500, 1000)
                            lane = random.randint(-1, 1)
                            obstacles.append(Obstacle(pos, lane))
                            last_obstacle_pos = pos
        
        # Title screen
        if current_state == STATE_TITLE:
            draw_title_screen()
        
        # Game playing state
        elif current_state == STATE_PLAYING:
            # Get keyboard input
            keys = pygame.key.get_pressed()
            
            # Acceleration and braking
            if keys[K_UP] or keys[K_w]:
                game_state.speed += game_state.acceleration * (game_state.max_speed - game_state.speed) / game_state.max_speed
            elif keys[K_DOWN] or keys[K_s]:
                game_state.speed += game_state.deceleration
            else:
                game_state.speed -= game_state.deceleration / 4
            
            # Limit speed
            game_state.speed = max(0, min(game_state.speed, game_state.max_speed))
            
            # Steering
            if game_state.speed > 0:
                if keys[K_LEFT] or keys[K_a]:
                    game_state.player_x -= game_state.handling * (game_state.speed / game_state.max_speed)
                if keys[K_RIGHT] or keys[K_d]:
                    game_state.player_x += game_state.handling * (game_state.speed / game_state.max_speed)
            
            # Apply centrifugal force (pull to outside of curves)
            segment = int(game_state.position / SEGMENT_LENGTH) % len(game_state.track_curvature)
            game_state.player_x += game_state.track_curvature[segment] * game_state.centrifugal * (game_state.speed / game_state.max_speed)
            
            # Limit player x position (stay on road)
            game_state.player_x = max(-2, min(2, game_state.player_x))
            
            # Update position based on speed
            game_state.position += game_state.speed
            
            # Update distance and score
            game_state.distance += game_state.speed
            game_state.score = int(game_state.distance / 100)
            
            # Check for collision
            if check_collision(game_state.player_x, game_state.position):
                if has_sound:
                    engine_sound.stop()
                    crash_sound.play()
                current_state = STATE_GAME_OVER
                game_state.game_over = True
            
            # Generate new obstacles as needed
            if game_state.position > last_obstacle_pos - 2000:
                pos = last_obstacle_pos + random.randint(500, 1000)
                lane = random.randint(-1, 1)
                obstacles.append(Obstacle(pos, lane))
                last_obstacle_pos = pos
                
                # Play score sound every 1000 points
                if has_sound and int(game_state.score / 1000) > int((game_state.score - game_state.speed / 100) / 1000):
                    score_sound.play()
            
            # Remove obstacles that are far behind
            obstacles = [o for o in obstacles if o.position > game_state.position - 1000]
            
            # Update engine sound volume based on speed
            if has_sound:
                engine_sound.set_volume(game_state.speed / game_state.max_speed * 0.7)
            
            # Draw everything
            segment = int(game_state.position / SEGMENT_LENGTH) % len(game_state.track_curvature)
            dt = clock.get_time()  # Get delta time since last frame
            draw_road(game_state.position, game_state.player_x, game_state.track_curvature[segment], game_state.hills[segment], dt)
            player_car.draw(0, 0, game_state.speed / game_state.max_speed)
            draw_hud(game_state.speed, game_state.score)
            
            # Educational info
            font = pygame.font.SysFont("Arial", 16)
            edu_text = font.render(f"Pseudo-3D Technique: {len(obstacles)} obstacles, {int(game_state.position / SEGMENT_LENGTH)} segments", True, NEON_GREEN)
            screen.blit(edu_text, (20, SCREEN_HEIGHT - 30))
        
        # Game over state
        elif current_state == STATE_GAME_OVER:
            # Draw everything but with game over overlay
            segment = int(game_state.position / SEGMENT_LENGTH) % len(game_state.track_curvature)
            draw_road(game_state.position, game_state.player_x, game_state.track_curvature[segment], game_state.hills[segment])
            player_car.draw(0, 0, 0)
            draw_hud(0, game_state.score, True)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()