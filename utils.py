import math
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CONFIG, SKY, NIGHT_SKY

def ease_in_out(t):
    """Smooth easing function for transitions"""
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    """Linear interpolation between a and b"""
    return a + (b - a) * t

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
def draw_segment(screen, x1, y1, w1, x2, y2, w2, color, fog_factor1=0, fog_factor2=0):
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
def draw_stars(screen, position):
    import time
    import random
    
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
    
    def draw(self, screen):
        for p in self.particles:
            alpha = min(255, int(p['life'] * 5))
            color_with_alpha = (*p['color'], alpha)
            
            # Create a surface for the particle with alpha
            particle_surface = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color_with_alpha, (p['size'], p['size']), p['size'])
            
            # Blit the particle
            screen.blit(particle_surface, (int(p['x'] - p['size']), int(p['y'] - p['size'])))