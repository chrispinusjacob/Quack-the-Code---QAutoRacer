import pygame
import random
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, NEON_PINK, NEON_BLUE, NEON_GREEN, NEON_RED

class ParticleSystem:
    """Particle system for visual effects"""
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

class Car:
    """Player car with advanced features"""
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
        self.suspension_compression = self.lerp(self.suspension_compression, target_compression, 0.2)
        
        # Update color based on damage
        if self.flash_timer > 0:
            self.flash_timer -= 1
            self.color = NEON_RED if self.flash_timer % 4 < 2 else self.base_color
        else:
            damage_factor = self.damage / 100
            self.color = (
                self.lerp(self.base_color[0], 150, damage_factor),
                self.lerp(self.base_color[1], 150, damage_factor),
                self.lerp(self.base_color[2], 150, damage_factor)
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
        
    def draw(self, screen, x, y, speed_ratio, drift=0, boosting=False):
        # Apply drift to visual position
        visual_x = x + drift * 10
        
        # Draw particles first (behind car)
        self.exhaust_particles.draw(screen)
        self.boost_particles.draw(screen)
        self.skid_particles.draw(screen)
        
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
    
    def lerp(self, a, b, t):
        """Linear interpolation between a and b"""
        return a + (b - a) * t

class Obstacle:
    """Obstacle class for things the player must avoid"""
    def __init__(self, position, lane):
        self.position = position
        self.lane = lane  # -1 (left), 0 (center), 1 (right)
        self.width = 60
        self.height = 40
        self.passed = False
        self.hit = False
        self.type = random.choice(['car', 'barrier', 'truck', 'oil', 'cone'])
        
        # Color schemes based on current game settings
        from config import get_color_scheme
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
        from config import ROAD_WIDTH, LANES
        lane_width = ROAD_WIDTH / LANES
        return (self.lane * lane_width) - (lane_width)
        
    def draw(self, screen, x, y, w, h):
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

class PowerUp:
    """Power-up class for special items the player can collect"""
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