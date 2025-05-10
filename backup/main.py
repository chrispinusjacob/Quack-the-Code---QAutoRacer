import pygame
import sys
import math
import random
import os
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "QAutoGame '90"

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

# Game settings
ROAD_WIDTH = 400
LANE_COUNT = 3
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT
PLAYER_SPEED = 8
INITIAL_ENEMY_SPEED = 3
INITIAL_SCROLL_SPEED = 5
SPEED_INCREASE_RATE = 0.0001
ORB_SPAWN_RATE = 0.02
ENEMY_SPAWN_RATE = 0.03

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")
FONT_DIR = os.path.join(ASSET_DIR, "fonts")
SPRITE_DIR = os.path.join(ASSET_DIR, "sprites")

# Create directories if they don't exist
os.makedirs(SOUND_DIR, exist_ok=True)
os.makedirs(FONT_DIR, exist_ok=True)
os.makedirs(SPRITE_DIR, exist_ok=True)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Load or create assets
def create_car_sprite(color, width=40, height=60):
    """Create a simple pixel art car sprite"""
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Main body
    pygame.draw.rect(sprite, color, (5, 10, width-10, height-20))
    
    # Top part (cabin)
    pygame.draw.rect(sprite, color, (10, 5, width-20, 10))
    
    # Wheels
    wheel_color = (30, 30, 30)
    pygame.draw.rect(sprite, wheel_color, (2, 15, 6, 12))
    pygame.draw.rect(sprite, wheel_color, (width-8, 15, 6, 12))
    pygame.draw.rect(sprite, wheel_color, (2, height-27, 6, 12))
    pygame.draw.rect(sprite, wheel_color, (width-8, height-27, 6, 12))
    
    # Windshield
    pygame.draw.rect(sprite, (100, 200, 255), (12, 12, width-24, 8))
    
    # Headlights
    pygame.draw.rect(sprite, (255, 255, 200), (8, 5, 6, 4))
    pygame.draw.rect(sprite, (255, 255, 200), (width-14, 5, 6, 4))
    
    # Taillights
    pygame.draw.rect(sprite, (255, 0, 0), (8, height-9, 6, 4))
    pygame.draw.rect(sprite, (255, 0, 0), (width-14, height-9, 6, 4))
    
    return sprite

def create_orb_sprite(radius=15):
    """Create a glowing orb sprite"""
    size = radius * 2
    sprite = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Create glow effect with multiple circles
    for r in range(radius, 0, -2):
        alpha = 255 if r == radius else int(255 * (r / radius))
        color = (*NEON_CYAN[:3], alpha)
        pygame.draw.circle(sprite, color, (radius, radius), r)
    
    return sprite

def create_road_segment(width, height):
    """Create a road segment with lane markings"""
    segment = pygame.Surface((width, height))
    segment.fill((50, 50, 50))  # Dark gray road
    
    # Add lane markings
    lane_width = width // LANE_COUNT
    for lane in range(1, LANE_COUNT):
        x = lane * lane_width
        pygame.draw.line(segment, (255, 255, 255), (x, 0), (x, height), 2)
    
    return segment

def create_stripe(width, height):
    """Create a road stripe for the sides"""
    stripe = pygame.Surface((width, height))
    stripe.fill((255, 255, 255))
    return stripe

# Create pixel fonts
def get_font(size):
    try:
        return pygame.font.Font(os.path.join(FONT_DIR, "pixel.ttf"), size)
    except:
        return pygame.font.SysFont("Arial", size)

# Load or create sounds
try:
    engine_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "engine.mp3"))
    crash_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "crash.mp3"))
    pickup_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "score.mp3"))
    has_sound = True
except:
    has_sound = False
    print("Sound files not found. Creating placeholder sounds.")
    
    # Create simple sounds
    engine_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(
        pygame.surfarray.array3d(pygame.Surface((10, 10)))))
    crash_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(
        pygame.surfarray.array3d(pygame.Surface((10, 10)))))
    pickup_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(
        pygame.surfarray.array3d(pygame.Surface((10, 10)))))

# Game classes
class Car:
    def __init__(self, x, y, color=NEON_BLUE, is_player=False):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.color = color
        self.is_player = is_player
        self.speed = PLAYER_SPEED if is_player else INITIAL_ENEMY_SPEED
        self.sprite = create_car_sprite(color, self.width, self.height)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Animation variables
        self.frame = 0
        self.exhaust_particles = []
    
    def update(self, dt=1.0):
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Add exhaust particles for player
        if self.is_player and random.random() < 0.2:
            self.exhaust_particles.append({
                'x': self.x + self.width // 2,
                'y': self.y + self.height,
                'size': random.uniform(2, 5),
                'life': random.randint(10, 20),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(1, 2)
            })
        
        # Update exhaust particles
        new_particles = []
        for p in self.exhaust_particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1
            p['size'] *= 0.9
            
            if p['life'] > 0 and p['size'] > 0.5:
                new_particles.append(p)
        
        self.exhaust_particles = new_particles
        
        # Animation frame
        self.frame += 1
    
    def draw(self, surface):
        # Draw exhaust particles
        for p in self.exhaust_particles:
            alpha = min(255, int(p['life'] * 10))
            pygame.draw.circle(surface, (100, 100, 100, alpha), 
                             (int(p['x']), int(p['y'])), 
                             int(p['size']))
        
        # Draw car with slight animation
        y_offset = math.sin(self.frame * 0.2) * 2 if self.is_player else 0
        surface.blit(self.sprite, (self.x, self.y + y_offset))
        
        # Draw headlight glow for player
        if self.is_player:
            glow_size = 10 + math.sin(self.frame * 0.1) * 2
            glow_surf = pygame.Surface((int(glow_size*2), int(glow_size*2)), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 200, 50), (int(glow_size), int(glow_size)), int(glow_size))
            surface.blit(glow_surf, (self.x + 8 - glow_size, self.y + 5 - glow_size))
            surface.blit(glow_surf, (self.x + self.width - 8 - glow_size, self.y + 5 - glow_size))

class Orb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.sprite = create_orb_sprite(self.radius)
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius*2, self.radius*2)
        self.collected = False
        
        # Animation variables
        self.frame = random.randint(0, 100)
    
    def update(self, scroll_speed):
        self.y += scroll_speed
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius
        self.frame += 1
    
    def draw(self, surface):
        # Pulsating effect
        scale = 1.0 + math.sin(self.frame * 0.1) * 0.2
        scaled_sprite = pygame.transform.scale(
            self.sprite, 
            (int(self.radius*2*scale), int(self.radius*2*scale))
        )
        surface.blit(
            scaled_sprite, 
            (self.x - int(self.radius*scale), self.y - int(self.radius*scale))
        )

class Game:
    def __init__(self):
        self.running = True
        self.game_over = False
        self.score = 0
        self.high_score = 0
        self.scroll_speed = INITIAL_SCROLL_SPEED
        self.enemy_speed = INITIAL_ENEMY_SPEED
        self.player = Car(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100, NEON_PINK, True)
        self.enemies = []
        self.orbs = []
        self.road_segments = []
        self.stripes = []
        self.game_time = 0
        
        # Create road segments
        segment_height = 100
        for i in range(SCREEN_HEIGHT // segment_height + 2):
            self.road_segments.append({
                'y': i * segment_height - segment_height,
                'sprite': create_road_segment(ROAD_WIDTH, segment_height)
            })
        
        # Create road stripes
        stripe_height = 30
        stripe_gap = 40
        for i in range(SCREEN_HEIGHT // (stripe_height + stripe_gap) * 2):
            self.stripes.append({
                'y': i * (stripe_height + stripe_gap) - stripe_height,
                'sprite': create_stripe(10, stripe_height)
            })
        
        # Start engine sound
        if has_sound:
            engine_sound.play(-1)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_SPACE and self.game_over:
                    self.reset()
        
        # Continuous movement
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[K_LEFT] or keys[K_a]:
                self.player.x -= self.player.speed
            if keys[K_RIGHT] or keys[K_d]:
                self.player.x += self.player.speed
            
            # Keep player within road boundaries
            road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
            road_right = road_left + ROAD_WIDTH
            self.player.x = max(road_left + 5, min(road_right - self.player.width - 5, self.player.x))
    
    def update(self):
        if self.game_over:
            return
        
        dt = clock.get_time() / 1000.0  # Delta time in seconds
        self.game_time += dt
        
        # Increase speed over time
        self.scroll_speed += SPEED_INCREASE_RATE * dt * 60
        self.enemy_speed += SPEED_INCREASE_RATE * dt * 60
        
        # Update player
        self.player.update(dt)
        
        # Update road segments
        for segment in self.road_segments:
            segment['y'] += self.scroll_speed
            if segment['y'] > SCREEN_HEIGHT:
                segment['y'] -= len(self.road_segments) * segment['sprite'].get_height()
        
        # Update stripes
        for stripe in self.stripes:
            stripe['y'] += self.scroll_speed
            if stripe['y'] > SCREEN_HEIGHT:
                stripe['y'] -= len(self.stripes) * (stripe['sprite'].get_height() + 40)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.y += self.enemy_speed
            enemy.update(dt)
            
            # Check for collision with player
            if enemy.rect.colliderect(self.player.rect):
                self.game_over = True
                if has_sound:
                    engine_sound.stop()
                    crash_sound.play()
        
        # Remove enemies that are off screen
        self.enemies = [e for e in self.enemies if e.y < SCREEN_HEIGHT + 100]
        
        # Update orbs
        for orb in self.orbs:
            orb.update(self.scroll_speed)
            
            # Check for collision with player
            if not orb.collected and orb.rect.colliderect(self.player.rect):
                orb.collected = True
                self.score += 100
                if has_sound:
                    pickup_sound.play()
        
        # Remove orbs that are collected or off screen
        self.orbs = [o for o in self.orbs if not o.collected and o.y < SCREEN_HEIGHT + 100]
        
        # Spawn new enemies
        if random.random() < ENEMY_SPAWN_RATE * dt * 60:
            lane = random.randint(0, LANE_COUNT-1)
            road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
            x = road_left + lane * LANE_WIDTH + (LANE_WIDTH - 40) // 2
            color = random.choice([NEON_GREEN, NEON_BLUE, NEON_PURPLE, NEON_YELLOW, NEON_ORANGE])
            self.enemies.append(Car(x, -100, color))
        
        # Spawn new orbs
        if random.random() < ORB_SPAWN_RATE * dt * 60:
            road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
            x = road_left + random.randint(30, ROAD_WIDTH - 30)
            self.orbs.append(Orb(x, -30))
        
        # Update high score
        self.high_score = max(self.high_score, self.score)
        
        # Increase score based on time
        self.score += int(dt * 10)
    
    def draw(self):
        # Fill background
        screen.fill(BLACK)
        
        # Draw starfield background
        for i in range(100):
            x = (i * 17) % SCREEN_WIDTH
            y = (i * 23) % SCREEN_HEIGHT
            size = random.randint(1, 3)
            brightness = 100 + int(math.sin(self.game_time + i) * 50)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (x, y), size)
        
        # Draw road
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        
        # Draw road segments
        for segment in self.road_segments:
            screen.blit(segment['sprite'], (road_left, segment['y']))
        
        # Draw stripes
        for stripe in self.stripes:
            # Left stripe
            screen.blit(stripe['sprite'], (road_left - 15, stripe['y']))
            # Right stripe
            screen.blit(stripe['sprite'], (road_left + ROAD_WIDTH + 5, stripe['y']))
        
        # Draw orbs
        for orb in self.orbs:
            orb.draw(screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # Draw player
        self.player.draw(screen)
        
        # Draw HUD
        self.draw_hud()
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_hud(self):
        # Create a semi-transparent HUD background
        hud_surface = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 150))
        screen.blit(hud_surface, (0, 0))
        
        # Draw score
        font = get_font(24)
        score_text = f"SCORE: {self.score}"
        score_surface = font.render(score_text, True, NEON_PINK)
        screen.blit(score_surface, (20, 15))
        
        # Draw high score
        high_score_text = f"HIGH SCORE: {self.high_score}"
        high_score_surface = font.render(high_score_text, True, NEON_CYAN)
        screen.blit(high_score_surface, (SCREEN_WIDTH - 20 - high_score_surface.get_width(), 15))
        
        # Draw speed indicator
        speed_percent = min(1.0, (self.scroll_speed - INITIAL_SCROLL_SPEED) / 10)
        speed_text = f"SPEED: {int(speed_percent * 100)}%"
        speed_surface = font.render(speed_text, True, NEON_GREEN)
        screen.blit(speed_surface, (SCREEN_WIDTH // 2 - speed_surface.get_width() // 2, 15))
    
    def draw_game_over(self):
        # Create overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Draw game over text
        font_large = get_font(72)
        game_over_text = "GAME OVER"
        game_over_surface = font_large.render(game_over_text, True, NEON_PINK)
        
        # Add glow effect
        for i in range(10, 0, -2):
            glow_surface = font_large.render(game_over_text, True, (*NEON_PINK[:3], 25 * i))
            screen.blit(glow_surface, 
                       (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2 + random.randint(-i, i), 
                        SCREEN_HEIGHT // 3 - game_over_surface.get_height() // 2 + random.randint(-i, i)))
        
        screen.blit(game_over_surface, 
                   (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, 
                    SCREEN_HEIGHT // 3 - game_over_surface.get_height() // 2))
        
        # Draw final score
        font_medium = get_font(36)
        final_score_text = f"FINAL SCORE: {self.score}"
        final_score_surface = font_medium.render(final_score_text, True, NEON_GREEN)
        screen.blit(final_score_surface, 
                   (SCREEN_WIDTH // 2 - final_score_surface.get_width() // 2, 
                    SCREEN_HEIGHT // 2))
        
        # Draw restart instructions
        font_small = get_font(24)
        restart_text = "PRESS SPACE TO RESTART"
        restart_surface = font_small.render(restart_text, True, NEON_YELLOW)
        screen.blit(restart_surface, 
                   (SCREEN_WIDTH // 2 - restart_surface.get_width() // 2, 
                    SCREEN_HEIGHT * 2 // 3))
    
    def reset(self):
        self.game_over = False
        self.score = 0
        self.scroll_speed = INITIAL_SCROLL_SPEED
        self.enemy_speed = INITIAL_ENEMY_SPEED
        self.player = Car(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100, NEON_PINK, True)
        self.enemies = []
        self.orbs = []
        self.game_time = 0
        
        # Restart engine sound
        if has_sound:
            engine_sound.play(-1)
    
    def run(self):
        # Main game loop
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()