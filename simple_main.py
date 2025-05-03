import pygame
import sys
import math
import random
import time
from pygame.locals import *
from config import *

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("QAutoRacer - Synthwave Edition")
clock = pygame.time.Clock()

# Game state class
class GameState:
    def __init__(self):
        self.position = 0
        self.player_x = 0
        self.speed = 0
        self.max_speed = 300
        self.acceleration = 0.2
        self.deceleration = -0.3
        self.handling = 0.04
        self.centrifugal = CONFIG["centrifugal_factor"]
        self.drift = 0
        self.offroad = False
        self.score = 0
        self.distance = 0
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        
        # Generate track
        self.track_length = 10000
        self.track_curvature = [0] * self.track_length
        self.hills = [0] * self.track_length
        self.track_width = [1.0] * self.track_length
        
        # Generate a simple track
        for i in range(self.track_length):
            # Simple sine wave for curves
            self.track_curvature[i] = math.sin(i / 100) * 0.3
            # Simple hills
            self.hills[i] = math.sin(i / 200) * 0.05

# Simple car class
class Car:
    def __init__(self):
        self.width = 80
        self.height = 40
        self.color = NEON_PINK
        self.damage = 0
    
    def draw(self, x, y, speed_ratio):
        # Draw car body
        car_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - self.width // 2,
            SCREEN_HEIGHT - 150,
            self.width,
            self.height
        )
        pygame.draw.rect(screen, self.color, car_rect, border_radius=10)
        
        # Draw windshield
        windshield = pygame.Rect(
            SCREEN_WIDTH // 2 - self.width // 4,
            SCREEN_HEIGHT - 145,
            self.width // 2,
            self.height // 2 - 5
        )
        pygame.draw.rect(screen, (0, 0, 0), windshield, border_radius=5)

# Simple obstacle class
class Obstacle:
    def __init__(self, position, lane):
        self.position = position
        self.lane = lane  # -1 (left), 0 (center), 1 (right)
        self.width = 60
        self.height = 40
        self.passed = False
        self.color = random.choice([NEON_BLUE, NEON_GREEN, NEON_PURPLE, NEON_YELLOW])

# Draw the road
def draw_road(position, player_x, curvature, hill, dt=0):
    # Get color scheme
    colors = get_color_scheme()
    
    # Draw sky
    screen.fill(colors["sky"])
    
    # Draw ground
    pygame.draw.rect(screen, colors["ground"], (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    
    # Draw road segments
    segment_count = CONFIG["draw_distance"]
    segment_size = SCREEN_HEIGHT / (segment_count / 2)
    
    # Base segment
    base_segment = int(position / SEGMENT_LENGTH)
    
    # Camera height and depth
    camera_height = CONFIG["camera_height"]
    camera_depth = CONFIG["camera_depth"]
    
    # Draw segments from far to near
    for i in range(segment_count):
        # Current segment
        segment = (base_segment + i) % len(game_state.track_curvature)
        
        # Calculate segment position
        segment_position = (segment * SEGMENT_LENGTH) - position
        
        # Project 3D coordinates to 2D screen
        scale = camera_depth / (segment_position + 0.1)
        
        # Apply curvature and player position
        curve_offset = game_state.track_curvature[segment] * i * i
        player_offset = player_x * scale
        
        # Calculate screen coordinates
        screen_x = SCREEN_WIDTH // 2 + (curve_offset - player_offset) * scale
        screen_y = SCREEN_HEIGHT // 2 + (camera_height / (segment_position + 0.1))
        
        # Calculate road width
        road_width = ROAD_WIDTH * scale
        
        # Draw road segment
        if i % 2 == 0:
            road_color = colors["road"]
            grass_color = colors["grass_light"]
            rumble_color = colors["rumble_light"]
        else:
            road_color = colors["road"]
            grass_color = colors["grass_dark"]
            rumble_color = colors["rumble_dark"]
        
        # Draw grass
        pygame.draw.rect(screen, grass_color, (0, int(screen_y), SCREEN_WIDTH, int(segment_size) + 1))
        
        # Draw road
        road_left = int(screen_x - road_width // 2)
        road_right = int(screen_x + road_width // 2)
        pygame.draw.rect(screen, road_color, (road_left, int(screen_y), road_right - road_left, int(segment_size) + 1))
        
        # Draw rumble strips
        rumble_width = road_width // 20
        pygame.draw.rect(screen, rumble_color, (road_left, int(screen_y), rumble_width, int(segment_size) + 1))
        pygame.draw.rect(screen, rumble_color, (road_right - rumble_width, int(screen_y), rumble_width, int(segment_size) + 1))
        
        # Draw lane markers
        if i % 8 == 0:
            lane_width = road_width // LANES
            for lane in range(1, LANES):
                lane_x = int(screen_x - road_width // 2 + lane * lane_width)
                pygame.draw.rect(screen, colors["lane"], (lane_x - 1, int(screen_y), 2, int(segment_size) + 1))

# Draw HUD
def draw_hud(speed, score, game_over=False):
    # Speed display
    speed_kmh = int(speed * 3.6)  # Convert to km/h
    speed_text = f"SPEED: {speed_kmh} KM/H"
    font = pygame.font.SysFont("Arial", 24, bold=True)
    speed_surface = font.render(speed_text, True, NEON_GREEN)
    screen.blit(speed_surface, (20, 20))
    
    # Score display
    score_text = f"SCORE: {int(score)}"
    score_surface = font.render(score_text, True, NEON_PINK)
    screen.blit(score_surface, (20, 50))
    
    # Game over screen
    if game_over:
        # Create overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Game over text
        font_large = pygame.font.SysFont("Arial", 72, bold=True)
        game_over_text = "GAME OVER"
        game_over_surface = font_large.render(game_over_text, True, NEON_PINK)
        screen.blit(game_over_surface, 
                   (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, 
                    SCREEN_HEIGHT // 3))
        
        # Final score
        score_font = pygame.font.SysFont("Arial", 48)
        final_score_text = f"FINAL SCORE: {int(score)}"
        final_score_surface = score_font.render(final_score_text, True, NEON_GREEN)
        screen.blit(final_score_surface, 
                   (SCREEN_WIDTH // 2 - final_score_surface.get_width() // 2, 
                    SCREEN_HEIGHT // 2))
        
        # Restart text
        restart_text = "Press SPACE to restart"
        restart_font = pygame.font.SysFont("Arial", 30)
        restart_surface = restart_font.render(restart_text, True, NEON_GREEN)
        screen.blit(restart_surface, 
                   (SCREEN_WIDTH // 2 - restart_surface.get_width() // 2, 
                    SCREEN_HEIGHT - 100))

# Check for collision
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

# Draw title screen
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

# Sound effects
try:
    engine_sound = pygame.mixer.Sound("assets/sounds/engine.mp3")
    crash_sound = pygame.mixer.Sound("assets/sounds/crash.mp3")
    score_sound = pygame.mixer.Sound("assets/sounds/score.mp3")
    has_sound = True
except Exception as e:
    has_sound = False
    print(f"Sound files not found: {e}. Continuing without sound.")

# Game states
STATE_TITLE = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2

# Game objects
game_state = GameState()
player_car = Car()
obstacles = []
last_obstacle_pos = 0

# Main game loop
def main():
    global game_state, player_car, obstacles, last_obstacle_pos
    
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
                        game_state.start_time = pygame.time.get_ticks()
                        player_car = Car()
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
                        game_state.start_time = pygame.time.get_ticks()
                        player_car = Car()
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
            
            # Get delta time since last frame
            dt = clock.get_time()
            
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
            draw_road(game_state.position, game_state.player_x, game_state.track_curvature[segment], game_state.hills[segment], 0)
            player_car.draw(0, 0, 0)
            draw_hud(0, game_state.score, True)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()