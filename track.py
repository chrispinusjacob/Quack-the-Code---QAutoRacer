import pygame
import math
import random
import time
from config import *
from utils import ease_in_out, lerp, project, draw_segment, draw_stars

class Track:
    def __init__(self, length=10000):
        self.track_curvature = []
        self.hills = []
        self.track_width = []  # Variable track width
        self.track_sprites = []  # Decorative sprites along the track
        self.generate_track(length)
        
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
    
    def draw_road(self, screen, position, player_x, obstacles, power_ups, screen_shake=0, flash_effect=0, vignette_effect=0):
        # Get color scheme
        colors = get_color_scheme()
        
        # Draw sky
        screen.fill(colors["sky"])
        
        # Draw stars at night
        if CONFIG["night_mode"]:
            draw_stars(screen, position)
        
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
            segment = (base_segment + i) % len(self.track_curvature)
            
            # Calculate segment curve and hill
            curve = self.track_curvature[segment] * player_x
            hill = self.hills[segment]
            
            # Get track width for this segment
            track_width_multiplier = self.track_width[segment]
            
            # Project 3D points to 2D with camera shake
            p1_x = curve
            p1_y = hill
            p1_z = i * SEGMENT_LENGTH
            
            p2_x = self.track_curvature[(segment + 1) % len(self.track_curvature)] * player_x
            p2_y = self.hills[(segment + 1) % len(self.hills)]
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
            draw_segment(screen, x1, y1, w1 * 2, x2, y2, w2 * 2, grass_color, fog1, fog2)
            # Rumble strips
            draw_segment(screen, x1, y1, w1 * 1.2, x2, y2, w2 * 1.2, rumble_color, fog1, fog2)
            # Road
            draw_segment(screen, x1, y1, w1, x2, y2, w2, road_color, fog1, fog2)
            
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
                        screen,
                        x1 + w1 * lane_offset, y1, lane_w1,
                        x2 + w2 * lane_offset, y2, lane_w2,
                        colors["lane"],
                        fog1, fog2
                    )
            
            # Draw track sprites (decorations)
            from sprites import TrackSprite
            sprite = self.track_sprites[segment]
            if sprite:
                sprite_type, sprite_side = sprite
                track_sprite = TrackSprite(sprite_type, sprite_side)
                track_sprite.draw(screen, x1 + sprite_side * w1 * 1.5, y1, w1, w1, s1)
            
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
                    obstacle.draw(screen, x1 + obstacle_x, y1, obstacle_width, obstacle_height)
            
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
                        power_up.draw(screen, x1 + powerup_x, y1, powerup_width, powerup_height)
        
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
                f"Curvature: {self.track_curvature[segment]:.2f}",
                f"Hill: {self.hills[segment]:.2f}",
                f"Player X: {player_x:.2f}",
                f"Obstacles: {len(obstacles)}",
                f"Power-ups: {len(power_ups)}",
                f"Track Width: {track_width_multiplier:.2f}"
            ]
            
            for i, info in enumerate(debug_info):
                debug_text = debug_font.render(info, True, (255, 255, 255))
                screen.blit(debug_text, (10, SCREEN_HEIGHT - 20 * (len(debug_info) - i)))

    def draw_title_screen(self, screen):
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