import pygame
import sys
import math
import random
import os
from pygame.locals import *

# Import game modules
from game_objects import Car, Orb, create_road_segment, create_stripe
from difficulty_manager import DifficultyManager
from button import Button

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "QAutoGame"

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

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
FONT_DIR = os.path.join(ASSET_DIR, "fonts")

# Create directories if they don't exist
os.makedirs(FONT_DIR, exist_ok=True)

# Create pixel fonts
def get_font(size):
    try:
        return pygame.font.Font(os.path.join(FONT_DIR, "pixel.ttf"), size)
    except:
        return pygame.font.SysFont("Arial", size)

class Game:
    def __init__(self, screen=None, clock=None, sound_manager=None):
        # Use provided screen and clock or create new ones
        if screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption(TITLE)
        else:
            self.screen = screen
            
        if clock is None:
            self.clock = pygame.time.Clock()
        else:
            self.clock = clock
            
        if sound_manager is None:
            from sound_manager import SoundManager
            self.sound_manager = SoundManager()
        else:
            self.sound_manager = sound_manager
        
        # Game state
        self.running = True
        self.game_over = False
        self.paused = False
        self.score = 0
        self.high_score = 0
        self.player = Car(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100, NEON_PINK, True)
        self.enemies = []
        self.orbs = []
        self.road_segments = []
        self.stripes = []
        self.game_time = 0
        
        # Initialize difficulty manager
        self.difficulty = DifficultyManager()
        
        # Try to load difficulty settings
        try:
            from difficulty_settings import DifficultySettings
            self.difficulty_settings = DifficultySettings()
            # Apply saved difficulty settings
            self.difficulty_settings.apply_to_difficulty_manager(self.difficulty)
            print(f"Applied {self.difficulty_settings.current_difficulty} difficulty to game")
        except ImportError:
            print("Difficulty settings module not found, using default settings")
            self.difficulty_settings = None
        
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
        
        # Create pause menu buttons
        button_width = 250
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.pause_buttons = [
            Button(button_x, 250, button_width, button_height, 
                  "RESUME", get_font(30), 
                  text_color=WHITE, hover_color=NEON_GREEN, 
                  border_color=NEON_GREEN, sound_manager=self.sound_manager),
            
            Button(button_x, 320, button_width, button_height, 
                  "RESTART", get_font(30), 
                  text_color=WHITE, hover_color=NEON_BLUE, 
                  border_color=NEON_BLUE, sound_manager=self.sound_manager),
            
            Button(button_x, 390, button_width, button_height, 
                  "MAIN MENU", get_font(30), 
                  text_color=WHITE, hover_color=NEON_PURPLE, 
                  border_color=NEON_PURPLE, sound_manager=self.sound_manager)
        ]
        
        # Create game over buttons
        self.game_over_buttons = [
            Button(button_x, 350, button_width, button_height, 
                  "RESTART", get_font(30), 
                  text_color=WHITE, hover_color=NEON_GREEN, 
                  border_color=NEON_GREEN, sound_manager=self.sound_manager),
            
            Button(button_x, 420, button_width, button_height, 
                  "MAIN MENU", get_font(30), 
                  text_color=WHITE, hover_color=NEON_BLUE, 
                  border_color=NEON_BLUE, sound_manager=self.sound_manager)
        ]
        
        # Start engine sound
        self.sound_manager.play("engine", -1)  # Loop indefinitely
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                return {"action": "quit"}
            
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.game_over:
                        self.running = False
                        return {"action": "menu", "score": self.score}
                    else:
                        self.paused = not self.paused
                        # Stop engine sound when pausing
                        if self.paused:
                            self.sound_manager.stop("engine")
                        else:
                            self.sound_manager.play("engine", -1)
                        
                elif event.key == K_SPACE and self.game_over:
                    self.reset()
                    
                elif event.key == K_p and not self.game_over:
                    self.paused = not self.paused
                    # Stop engine sound when pausing
                    if self.paused:
                        self.sound_manager.stop("engine")
                    else:
                        self.sound_manager.play("engine", -1)
            
            # Handle pause menu button clicks
            if self.paused:
                for i, button in enumerate(self.pause_buttons):
                    if button.is_clicked(event):
                        if i == 0:  # Resume
                            self.paused = False
                            self.sound_manager.play("engine", -1)
                        elif i == 1:  # Restart
                            self.reset()
                            self.paused = False
                        elif i == 2:  # Main Menu
                            self.sound_manager.stop("engine")
                            self.running = False
                            return {"action": "menu", "score": self.score}
            
            # Handle game over button clicks
            if self.game_over:
                for i, button in enumerate(self.game_over_buttons):
                    if button.is_clicked(event):
                        if i == 0:  # Restart
                            self.reset()
                        elif i == 1:  # Main Menu
                            self.sound_manager.stop("engine")
                            self.running = False
                            return {"action": "menu", "score": self.score}
        
        # Skip other input processing if paused or game over
        if self.paused or self.game_over:
            return None
        
        # Continuous movement
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.player.x -= self.player.speed
        if keys[K_RIGHT] or keys[K_d]:
            self.player.x += self.player.speed
        
        # Keep player within road boundaries
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH
        self.player.x = max(road_left + 5, min(road_right - self.player.width - 5, self.player.x))
        
        return None
    
    def update(self):
        if self.game_over or self.paused:
            # Update buttons even when paused
            dt = self.clock.get_time() / 1000.0
            
            if self.paused:
                for button in self.pause_buttons:
                    button.update(dt)
            
            if self.game_over:
                for button in self.game_over_buttons:
                    button.update(dt)
                    
            return
        
        dt = self.clock.get_time() / 1000.0  # Delta time in seconds
        self.game_time += dt
        
        # Update difficulty
        self.difficulty.update(dt)

        # Direct speed control based on difficulty level
        if self.difficulty.difficulty_level == "easy":
            self.difficulty.enemy_speed = 1.5 + (self.game_time / 60.0) * 0.5  # Slow increase
            self.difficulty.scroll_speed = 2.5 + (self.game_time / 60.0) * 0.5
        elif self.difficulty.difficulty_level == "medium":
            self.difficulty.enemy_speed = 3.0 + (self.game_time / 30.0) * 0.8  # Medium increase
            self.difficulty.scroll_speed = 5.0 + (self.game_time / 30.0) * 0.8
        elif self.difficulty.difficulty_level == "hard":
            self.difficulty.enemy_speed = 7.0 + (self.game_time / 15.0) * 1.2  # Fast increase
            self.difficulty.scroll_speed = 9.0 + (self.game_time / 15.0) * 1.2

        # Cap speeds at maximum values
        self.difficulty.enemy_speed = min(self.difficulty.enemy_speed, self.difficulty.max_enemy_speed)
        self.difficulty.scroll_speed = min(self.difficulty.scroll_speed, self.difficulty.max_scroll_speed)
        
        # Update player
        self.player.update(dt)
        
        # Update road segments
        for segment in self.road_segments:
            segment['y'] += self.difficulty.scroll_speed
            if segment['y'] > SCREEN_HEIGHT:
                segment['y'] -= len(self.road_segments) * segment['sprite'].get_height()
        
        # Update stripes
        for stripe in self.stripes:
            stripe['y'] += self.difficulty.scroll_speed
            if stripe['y'] > SCREEN_HEIGHT:
                stripe['y'] -= len(self.stripes) * (stripe['sprite'].get_height() + 40)
        
        # Update enemies
        for enemy in self.enemies:
            # Apply difficulty-based speed variations to make enemies more dynamic
            difficulty_factor = 1.0
            if hasattr(self.difficulty, 'difficulty_level'):
                if self.difficulty.difficulty_level == "easy":
                    # Enemies move at consistent speed in easy mode
                    difficulty_factor = 1.0
                elif self.difficulty.difficulty_level == "medium":
                    # Some speed variation in medium mode
                    difficulty_factor = 0.9 + random.random() * 0.2
                elif self.difficulty.difficulty_level == "hard":
                    # High speed variation in hard mode
                    difficulty_factor = 0.8 + random.random() * 0.4
            
            # Update enemy position with difficulty-based speed
            enemy.y += self.difficulty.enemy_speed * difficulty_factor
            enemy.update(dt)
            
            # Check for collision with player
            if enemy.rect.colliderect(self.player.rect):
                self.game_over = True
                self.sound_manager.stop("engine")
                self.sound_manager.play("crash")
        
        # Remove enemies that are off screen
        self.enemies = [e for e in self.enemies if e.y < SCREEN_HEIGHT + 100]
        
        # Update orbs
        for orb in self.orbs:
            orb.update(self.difficulty.scroll_speed)
            
            # Check for collision with player
            if not orb.collected and orb.rect.colliderect(self.player.rect):
                orb.collected = True
                
                # Points vary by difficulty
                points = 1
                if hasattr(self.difficulty, 'difficulty_level'):
                    if self.difficulty.difficulty_level == "easy":
                        points = 1
                    elif self.difficulty.difficulty_level == "medium":
                        points = 2
                    elif self.difficulty.difficulty_level == "hard":
                        points = 3
                
                self.score += points
                self.sound_manager.play("pickup")
        
        # Remove orbs that are collected or off screen
        self.orbs = [o for o in self.orbs if not o.collected and o.y < SCREEN_HEIGHT + 100]
        
        # Spawn new enemies with difficulty-based positioning
        if random.random() < self.difficulty.enemy_spawn_rate * dt * 60:
            # Lane selection varies by difficulty
            lane = 0
            if hasattr(self.difficulty, 'difficulty_level'):
                if self.difficulty.difficulty_level == "easy":
                    # More predictable lane placement in easy mode
                    lane = random.randint(0, LANE_COUNT-1)
                elif self.difficulty.difficulty_level == "medium":
                    # Sometimes spawn enemies in adjacent lanes in medium mode
                    if len(self.enemies) > 0 and random.random() < 0.3:
                        last_enemy = self.enemies[-1]
                        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
                        last_lane = int((last_enemy.x - road_left) / LANE_WIDTH)
                        possible_lanes = [i for i in range(LANE_COUNT) if abs(i - last_lane) == 1]
                        if possible_lanes:
                            lane = random.choice(possible_lanes)
                        else:
                            lane = random.randint(0, LANE_COUNT-1)
                    else:
                        lane = random.randint(0, LANE_COUNT-1)
                elif self.difficulty.difficulty_level == "hard":
                    # Sometimes spawn enemies in the same lane in hard mode
                    if len(self.enemies) > 0 and random.random() < 0.4:
                        last_enemy = self.enemies[-1]
                        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
                        last_lane = int((last_enemy.x - road_left) / LANE_WIDTH)
                        lane = last_lane  # Same lane as last enemy
                    else:
                        lane = random.randint(0, LANE_COUNT-1)
            else:
                lane = random.randint(0, LANE_COUNT-1)
            
            road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
            x = road_left + lane * LANE_WIDTH + (LANE_WIDTH - 40) // 2
            color = random.choice([NEON_GREEN, NEON_BLUE, NEON_PURPLE, NEON_YELLOW, NEON_ORANGE])
            self.enemies.append(Car(x, -100, color))
        
        # Spawn new orbs
        if random.random() < self.difficulty.orb_spawn_rate * dt * 60:
            road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
            x = road_left + random.randint(30, ROAD_WIDTH - 30)
            self.orbs.append(Orb(x, -30))
        
        # Update high score
        self.high_score = max(self.high_score, self.score)
        
        # Increase score based on time - removed to make points only increment by collecting orbs
    
    def draw(self):
        # Fill background
        self.screen.fill(BLACK)
        
        # Draw starfield background
        for i in range(100):
            x = (i * 17) % SCREEN_WIDTH
            y = (i * 23) % SCREEN_HEIGHT
            size = random.randint(1, 3)
            brightness = 100 + int(math.sin(self.game_time + i) * 50)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (x, y), size)
        
        # Draw road
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        
        # Draw road segments
        for segment in self.road_segments:
            self.screen.blit(segment['sprite'], (road_left, segment['y']))
        
        # Draw stripes
        for stripe in self.stripes:
            # Left stripe
            self.screen.blit(stripe['sprite'], (road_left - 15, stripe['y']))
            # Right stripe
            self.screen.blit(stripe['sprite'], (road_left + ROAD_WIDTH + 5, stripe['y']))
        
        # Draw orbs
        for orb in self.orbs:
            orb.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw HUD
        self.draw_hud()
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
        
        # Draw pause screen
        if self.paused:
            self.draw_pause()
        
        pygame.display.flip()
    
    def draw_hud(self):
        # Get difficulty level name if available
        difficulty_name = "MEDIUM"
        if hasattr(self.difficulty, 'difficulty_settings') and self.difficulty.difficulty_settings:
            difficulty_name = self.difficulty.difficulty_settings.get_difficulty_name()
        
        # Use the game HUD class if available
        try:
            from game_hud import GameHUD
            
            # Create HUD if not already created
            if not hasattr(self, 'hud'):
                self.hud = GameHUD(self.screen, get_font)
            
            # Update and draw HUD
            speed_percent = self.difficulty.get_difficulty_percentage()
            self.hud.update(
                self.clock.get_time() / 1000.0,
                self.score,
                self.high_score,
                speed_percent,
                difficulty_name
            )
            self.hud.draw()
            
        except ImportError:
            # Fallback to original HUD if GameHUD is not available
            # Create a semi-transparent HUD background
            hud_surface = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
            hud_surface.fill((0, 0, 0, 150))
            self.screen.blit(hud_surface, (0, 0))
            
            # Draw score
            font = get_font(24)
            score_text = f"SCORE: {self.score}"
            score_surface = font.render(score_text, True, NEON_PINK)
            self.screen.blit(score_surface, (20, 15))
            
            # Draw high score
            high_score_text = f"HIGH SCORE: {self.high_score}"
            high_score_surface = font.render(high_score_text, True, NEON_CYAN)
            self.screen.blit(high_score_surface, (SCREEN_WIDTH - 20 - high_score_surface.get_width(), 15))
            
            # Draw speed indicator
            speed_percent = self.difficulty.get_difficulty_percentage()
            speed_text = f"SPEED: {speed_percent}%"
            speed_surface = font.render(speed_text, True, NEON_GREEN)
            
            # Draw difficulty level
            difficulty_text = f"DIFFICULTY: {difficulty_name}"
            difficulty_surface = font.render(difficulty_text, True, NEON_YELLOW)
            
            # Position speed and difficulty in the center
            center_width = SCREEN_WIDTH // 2
            self.screen.blit(speed_surface, (center_width - speed_surface.get_width() - 10, 15))
            self.screen.blit(difficulty_surface, (center_width + 10, 15))
    
    def draw_game_over(self):
        # Create overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        font_large = get_font(72)
        game_over_text = "GAME OVER"
        game_over_surface = font_large.render(game_over_text, True, NEON_PINK)
        
        # Add glow effect
        for i in range(10, 0, -2):
            glow_surface = font_large.render(game_over_text, True, (*NEON_PINK[:3], 25 * i))
            self.screen.blit(glow_surface, 
                       (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2 + random.randint(-i, i), 
                        SCREEN_HEIGHT // 3 - game_over_surface.get_height() // 2 + random.randint(-i, i)))
        
        self.screen.blit(game_over_surface, 
                   (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, 
                    SCREEN_HEIGHT // 3 - game_over_surface.get_height() // 2))
        
        # Draw final score
        font_medium = get_font(36)
        final_score_text = f"FINAL SCORE: {self.score}"
        final_score_surface = font_medium.render(final_score_text, True, NEON_GREEN)
        self.screen.blit(final_score_surface, 
                   (SCREEN_WIDTH // 2 - final_score_surface.get_width() // 2, 
                    SCREEN_HEIGHT // 2 - 30))
        
        # Draw buttons
        for button in self.game_over_buttons:
            button.draw(self.screen)
    
    def draw_pause(self):
        # Create overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause text
        font_large = get_font(72)
        pause_text = "PAUSED"
        pause_surface = font_large.render(pause_text, True, NEON_YELLOW)
        
        # Add glow effect
        for i in range(10, 0, -2):
            glow_surface = font_large.render(pause_text, True, (*NEON_YELLOW[:3], 25 * i))
            self.screen.blit(glow_surface, 
                       (SCREEN_WIDTH // 2 - pause_surface.get_width() // 2 + random.randint(-i, i), 
                        SCREEN_HEIGHT // 4 - pause_surface.get_height() // 2 + random.randint(-i, i)))
        
        self.screen.blit(pause_surface, 
                   (SCREEN_WIDTH // 2 - pause_surface.get_width() // 2, 
                    SCREEN_HEIGHT // 4 - pause_surface.get_height() // 2))
        
        # Draw buttons
        for button in self.pause_buttons:
            button.draw(self.screen)
    
    def reset(self):
        self.game_over = False
        self.paused = False
        self.score = 0
        self.player = Car(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100, NEON_PINK, True)
        self.enemies = []
        self.orbs = []
        self.game_time = 0
        self.difficulty.reset()
        
        # Restart engine sound
        self.sound_manager.play("engine", -1)
    
    def run(self):
        # Main game loop
        while self.running:
            result = self.handle_events()
            if result:
                return result
                
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Return to menu by default
        return {"action": "menu", "score": self.score}

# Start the game if run directly
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    from sound_manager import SoundManager
    sound_manager = SoundManager()
    
    game = Game(screen, clock, sound_manager)
    result = game.run()
    
    pygame.quit()
    sys.exit()