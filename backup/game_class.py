import pygame
import sys
import math
import random
import os
import json
from pygame.locals import *
from config import *
from button import Button
from main_menu import MainMenu, STATE_MAIN_MENU, STATE_PLAYING, STATE_GAME_OVER, STATE_PAUSED, STATE_SETTINGS, STATE_HIGH_SCORES, STATE_INSTRUCTIONS
from main_menu import NEON_PINK, NEON_BLUE, NEON_GREEN, NEON_PURPLE, NEON_YELLOW, NEON_ORANGE, NEON_CYAN
from sound_manager import sound_manager
from difficulty_manager import difficulty_manager
from theme_manager import theme_manager
from pause_menu import PauseMenu

# Game settings
ROAD_WIDTH = 400
LANE_COUNT = 3
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT
PLAYER_SPEED = 8
INITIAL_ENEMY_SPEED = 3
INITIAL_SCROLL_SPEED = 5
# Speed increase rates for different difficulty levels
SPEED_INCREASE_RATE_EASY = 0.0001
SPEED_INCREASE_RATE_MEDIUM = 0.0003
SPEED_INCREASE_RATE_HARD = 0.0005
SPEED_INCREASE_RATE = SPEED_INCREASE_RATE_MEDIUM  # Default
ORB_SPAWN_RATE = 0.02
ENEMY_SPAWN_RATE = 0.03

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.state = STATE_MAIN_MENU  # Start at main menu
        self.game_over = False
        self.score = 0
        self.high_score = 0
        self.scroll_speed = INITIAL_SCROLL_SPEED
        self.enemy_speed = INITIAL_ENEMY_SPEED
        self.player = None
        self.enemies = []
        self.orbs = []
        self.road_segments = []
        self.stripes = []
        self.game_time = 0
        
        # Import settings menu class
        from settings_menu import SettingsMenu
        
        # Create menu objects
        self.main_menu = MainMenu(screen, self.get_font)
        self.pause_menu = PauseMenu(screen, self.get_font)
        self.settings_menu = SettingsMenu(screen, self.get_font)
        
        # Load sounds
        self.load_sounds()
        
        # Initialize game elements
        self.initialize_game()
    
    def get_font(self, size):
        try:
            font_dir = os.path.join(ASSET_DIR, "fonts")
            return pygame.font.Font(os.path.join(font_dir, "pixel.ttf"), size)
        except:
            return pygame.font.SysFont("Arial", size)
    
    def load_sounds(self):
        # Use the centralized sound manager
        self.has_sound = sound_manager.load_sounds(SOUND_DIR)
    
    def initialize_game(self):
        # Create player
        self.player = Car(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100, NEON_PINK, True)
        
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
    
    def handle_events(self):
        events = pygame.event.get()
        
        for event in events:
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.state == STATE_PLAYING:
                        self.state = STATE_PAUSED
                        sound_manager.stop_engine_sound()
                    elif self.state == STATE_PAUSED:
                        self.state = STATE_PLAYING
                        if not self.game_over:
                            sound_manager.play_engine_sound()
                    elif self.state in [STATE_SETTINGS, STATE_INSTRUCTIONS, STATE_HIGH_SCORES]:
                        print(f"Returning to main menu from {self.state}")
                        # Stop all sounds
                        sound_manager.stop_all_sounds()
                        self.state = STATE_MAIN_MENU
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Handle game over menu button clicks
                if self.game_over and hasattr(self, 'game_over_buttons'):
                    mouse_pos = pygame.mouse.get_pos()
                    if self.game_over_buttons["restart"].is_clicked(mouse_pos, True):
                        print("Restarting game from game over screen")
                        self.save_high_score()
                        self.reset()
                        self.state = STATE_PLAYING
                        if self.has_sound:
                            sound_manager.play_engine_sound()
                    elif self.game_over_buttons["main_menu"].is_clicked(mouse_pos, True):
                        print("Returning to main menu from game over screen")
                        self.save_high_score()
                        
                        # Stop all sounds
                        sound_manager.stop_all_sounds()
                        
                        self.reset()
                        self.state = STATE_MAIN_MENU
                        
                        # Restart menu music
                        if hasattr(self.main_menu, 'menu_music') and self.main_menu.menu_music:
                            sound_manager.play_menu_music()
            # Add more control keys for player movement
            elif event.type == KEYDOWN:
                if event.key in [K_LEFT, K_a] and self.state == STATE_PLAYING and not self.game_over:
                    self.player.x -= self.player.speed * 2  # Quick move left
                elif event.key in [K_RIGHT, K_d] and self.state == STATE_PLAYING and not self.game_over:
                    self.player.x += self.player.speed * 2  # Quick move right
        
        # Handle menu states
        if self.state == STATE_MAIN_MENU:
            new_state = self.main_menu.handle_events(events)
            if new_state != self.state:
                # Stop all sounds when changing states
                sound_manager.stop_all_sounds()
                
                self.state = new_state
                if new_state == STATE_PLAYING:
                    # Start engine sound when starting game
                    sound_manager.play_engine_sound()
                    print("Starting game from main menu")
        elif self.state == STATE_PAUSED:
            new_state = self.pause_menu.handle_events(events)
            if new_state == -1:  # Special code for restart
                self.save_high_score()
                self.reset()
                self.state = STATE_PLAYING
                sound_manager.play_engine_sound()
                print("Restarting game from pause menu")
            elif new_state != self.state:
                if new_state == STATE_PLAYING:
                    # Resume engine sound when resuming game
                    if not self.game_over:
                        sound_manager.play_engine_sound()
                    print("Resuming game from pause menu")
                elif new_state == STATE_MAIN_MENU:
                    # Stop all sounds
                    sound_manager.stop_all_sounds()
                    print("Returning to main menu from pause menu")
                    # Restart menu music
                    if hasattr(self.main_menu, 'menu_music') and self.main_menu.menu_music:
                        sound_manager.play_menu_music()
                self.state = new_state
        elif self.state == STATE_SETTINGS:
            # Apply settings from settings menu
            if hasattr(self, 'settings_menu'):
                # Update difficulty
                difficulty_manager.set_difficulty(self.settings_menu.current_difficulty)
                
                # Update theme
                theme_manager.set_theme(self.settings_menu.current_theme)
                
            new_state = self.settings_menu.handle_events(events)
            if new_state != self.state:
                print(f"Changing state from settings: {self.state} to {new_state}")
                # Stop all sounds
                sound_manager.stop_all_sounds()
                
                self.state = new_state
                
                # Restart menu music if returning to main menu
                if new_state == STATE_MAIN_MENU and hasattr(self.main_menu, 'menu_music') and self.main_menu.menu_music:
                    sound_manager.play_menu_music()
        
        # Continuous movement (only when playing)
        if self.state == STATE_PLAYING and not self.game_over:
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
        dt = self.clock.get_time() / 1000.0  # Delta time in seconds
        
        if self.state == STATE_MAIN_MENU:
            self.main_menu.update(dt)
            return
        elif self.state == STATE_PAUSED:
            return
        elif self.game_over:
            # Update game over buttons
            if hasattr(self, 'game_over_buttons'):
                mouse_pos = pygame.mouse.get_pos()
                for button in self.game_over_buttons.values():
                    button.update(mouse_pos)
            return
        
        self.game_time += dt
        
        # Get current difficulty settings
        speed_increase_rate = difficulty_manager.get_speed_increase_rate()
        enemy_spawn_rate = difficulty_manager.get_enemy_spawn_rate()
        orb_spawn_rate = difficulty_manager.get_orb_spawn_rate()
        
        # Increase speed based on game time and difficulty
        self.scroll_speed += speed_increase_rate * dt * 60
        self.enemy_speed += speed_increase_rate * dt * 60
        
        # Update road segments
        for segment in self.road_segments:
            segment['y'] += self.scroll_speed
            if segment['y'] > SCREEN_HEIGHT:
                segment['y'] = min([s['y'] for s in self.road_segments]) - 100
        
        # Update stripes
        for stripe in self.stripes:
            stripe['y'] += self.scroll_speed
            if stripe['y'] > SCREEN_HEIGHT:
                stripe['y'] = min([s['y'] for s in self.stripes]) - 70
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.enemy_speed)
            
            # Check for collision with player
            if enemy.rect.colliderect(self.player.rect):
                self.game_over = True
                sound_manager.play_sound("crash")
        
        # Remove enemies that are off screen
        self.enemies = [e for e in self.enemies if e.y < SCREEN_HEIGHT + 100]
        
        # Update orbs
        for orb in self.orbs:
            orb.update(self.scroll_speed)
            
            # Check for collision with player
            if not orb.collected and orb.rect.colliderect(self.player.rect):
                orb.collected = True
                self.score += 100
                sound_manager.play_sound("pickup")
        
        # Remove orbs that are collected or off screen
        self.orbs = [o for o in self.orbs if not o.collected and o.y < SCREEN_HEIGHT + 100]
        
        # Spawn new enemies based on difficulty
        if random.random() < enemy_spawn_rate * dt * 60:
            lane = random.randint(0, LANE_COUNT-1)
            road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
            x = road_left + lane * LANE_WIDTH + (LANE_WIDTH - 40) // 2
            color = random.choice(theme_manager.get_colors()["enemy"])
            self.enemies.append(Car(x, -100, color))
        
        # Spawn new orbs based on difficulty
        if random.random() < orb_spawn_rate * dt * 60:
            road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
            x = road_left + random.randint(30, ROAD_WIDTH - 30)
            self.orbs.append(Orb(x, -30))
        
        # Update high score
        self.high_score = max(self.high_score, self.score)
        
        # Increase score based on time
        self.score += int(dt * 10)
    
    def draw(self):
        # Fill background
        self.screen.fill((0, 0, 0))
        
        # Draw starfield background
        for i in range(100):
            x = (i * 17) % SCREEN_WIDTH
            y = (i * 23) % SCREEN_HEIGHT
            size = random.randint(1, 3)
            brightness = 100 + int(math.sin(self.game_time + i) * 50)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (x, y), size)
        
        # Draw appropriate screen based on state
        if self.state == STATE_MAIN_MENU:
            self.main_menu.draw()
            pygame.display.flip()
            return
        elif self.state == STATE_SETTINGS:
            self.settings_menu.draw()
            pygame.display.flip()
            return
        elif self.state == STATE_HIGH_SCORES:
            self.draw_high_scores_screen()
            pygame.display.flip()
            return
        elif self.state == STATE_INSTRUCTIONS:
            self.draw_instructions_screen()
            pygame.display.flip()
            return
        
        # Draw game elements (only for playing state)
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
        
        # Draw pause menu if paused
        if self.state == STATE_PAUSED:
            self.pause_menu.draw()
        
        pygame.display.flip()
    
    def draw_hud(self):
        # Create a semi-transparent HUD background
        hud_surface = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 150))
        self.screen.blit(hud_surface, (0, 0))
        
        # Draw score
        font = self.get_font(24)
        score_text = f"SCORE: {self.score}"
        score_surface = font.render(score_text, True, NEON_PINK)
        self.screen.blit(score_surface, (20, 15))
        
        # Draw high score
        high_score_text = f"HIGH SCORE: {self.high_score}"
        high_score_surface = font.render(high_score_text, True, NEON_CYAN)
        self.screen.blit(high_score_surface, (SCREEN_WIDTH - 20 - high_score_surface.get_width(), 15))
        
        # Try to load high scores from file to ensure we're showing the highest score
        try:
            with open(os.path.join(os.path.dirname(__file__), "high_scores.json"), 'r') as f:
                loaded_scores = json.load(f)
                if loaded_scores and loaded_scores[0]["score"] > self.high_score:
                    self.high_score = loaded_scores[0]["score"]
        except:
            pass
        
        # Draw speed indicator
        speed_percent = min(1.0, (self.scroll_speed - INITIAL_SCROLL_SPEED) / 10)
        speed_text = f"SPEED: {int(speed_percent * 100)}%"
        speed_surface = font.render(speed_text, True, NEON_GREEN)
        self.screen.blit(speed_surface, (SCREEN_WIDTH // 2 - speed_surface.get_width() // 2, 15))
    
    def draw_game_over(self):
        # Create overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        font_large = self.get_font(72)
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
        font_medium = self.get_font(36)
        final_score_text = f"FINAL SCORE: {self.score}"
        final_score_surface = font_medium.render(final_score_text, True, NEON_GREEN)
        self.screen.blit(final_score_surface, 
                   (SCREEN_WIDTH // 2 - final_score_surface.get_width() // 2, 
                    SCREEN_HEIGHT // 2))
        
        # Draw game over menu buttons
        if not hasattr(self, 'game_over_buttons'):
            button_width = 200
            button_height = 50
            button_spacing = 20
            start_y = SCREEN_HEIGHT * 2 // 3
            
            self.game_over_buttons = {
                "restart": Button(
                    SCREEN_WIDTH // 2 - button_width // 2,
                    start_y,
                    button_width, button_height,
                    "RESTART", NEON_YELLOW
                ),
                "main_menu": Button(
                    SCREEN_WIDTH // 2 - button_width // 2,
                    start_y + button_height + button_spacing,
                    button_width, button_height,
                    "MAIN MENU", NEON_BLUE
                )
            }
        
        # Draw buttons
        button_font = self.get_font(24)
        for button in self.game_over_buttons.values():
            button.draw(self.screen, button_font)
    
    def draw_settings_screen(self):
        # Create overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Draw title
        title_font = self.get_font(48)
        title_text = "SETTINGS"
        title_surf = title_font.render(title_text, True, NEON_BLUE)
        
        # Add glow effect
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_BLUE[:3], 25 * i))
            self.screen.blit(glow_surf, 
                       (SCREEN_WIDTH // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        SCREEN_HEIGHT // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
        
        self.screen.blit(title_surf, 
                   (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                    SCREEN_HEIGHT // 6 - title_surf.get_height() // 2))
        
        # Draw settings options
        font = self.get_font(24)
        
        # Theme setting
        theme_text = f"THEME: SYNTHWAVE"
        theme_surf = font.render(theme_text, True, NEON_GREEN)
        self.screen.blit(theme_surf, 
                   (SCREEN_WIDTH // 2 - theme_surf.get_width() // 2, 
                    SCREEN_HEIGHT // 3))
        
        # Difficulty setting
        difficulty_text = f"DIFFICULTY: MEDIUM"
        difficulty_surf = font.render(difficulty_text, True, NEON_PURPLE)
        self.screen.blit(difficulty_surf, 
                   (SCREEN_WIDTH // 2 - difficulty_surf.get_width() // 2, 
                    SCREEN_HEIGHT // 3 + 50))
        
        # Music setting
        music_text = "MUSIC: ON"
        music_surf = font.render(music_text, True, NEON_YELLOW)
        self.screen.blit(music_surf, 
                   (SCREEN_WIDTH // 2 - music_surf.get_width() // 2, 
                    SCREEN_HEIGHT // 3 + 100))
        
        # Back instructions
        back_text = "Press ESC to return to Main Menu"
        back_surf = font.render(back_text, True, NEON_ORANGE)
        self.screen.blit(back_surf, 
                   (SCREEN_WIDTH // 2 - back_surf.get_width() // 2, 
                    SCREEN_HEIGHT * 2 // 3))
    
    def draw_high_scores_screen(self):
        # Create overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Draw title
        title_font = self.get_font(48)
        title_text = "HIGH SCORES"
        title_surf = title_font.render(title_text, True, NEON_PURPLE)
        
        # Add glow effect
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_PURPLE[:3], 25 * i))
            self.screen.blit(glow_surf, 
                       (SCREEN_WIDTH // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        SCREEN_HEIGHT // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
        
        self.screen.blit(title_surf, 
                   (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                    SCREEN_HEIGHT // 6 - title_surf.get_height() // 2))
        
        # Draw high scores
        font = self.get_font(24)
        
        # Load high scores from file
        high_scores = [
            {"name": "AAA", "score": 5000},
            {"name": "BBB", "score": 4000},
            {"name": "CCC", "score": 3000},
            {"name": "DDD", "score": 2000},
            {"name": "EEE", "score": 1000}
        ]
        
        try:
            with open(os.path.join(os.path.dirname(__file__), "high_scores.json"), 'r') as f:
                loaded_scores = json.load(f)
                if loaded_scores:
                    high_scores = loaded_scores
        except:
            pass
        
        y_pos = SCREEN_HEIGHT // 3
        for i, score in enumerate(high_scores[:10]):  # Show top 10 scores
            score_text = f"{i+1}. {score['name']} - {score['score']}"
            score_surf = font.render(score_text, True, NEON_CYAN)
            self.screen.blit(score_surf, 
                       (SCREEN_WIDTH // 2 - score_surf.get_width() // 2, 
                        y_pos))
            y_pos += 40
        
        # Back instructions
        back_text = "Press ESC to return to Main Menu"
        back_surf = font.render(back_text, True, NEON_ORANGE)
        self.screen.blit(back_surf, 
                   (SCREEN_WIDTH // 2 - back_surf.get_width() // 2, 
                    SCREEN_HEIGHT * 2 // 3 + 50))
    
    def draw_instructions_screen(self):
        # Create overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Draw title
        title_font = self.get_font(48)
        title_text = "INSTRUCTIONS"
        title_surf = title_font.render(title_text, True, NEON_YELLOW)
        
        # Add glow effect
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_YELLOW[:3], 25 * i))
            self.screen.blit(glow_surf, 
                       (SCREEN_WIDTH // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        SCREEN_HEIGHT // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
        
        self.screen.blit(title_surf, 
                   (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                    SCREEN_HEIGHT // 6 - title_surf.get_height() // 2))
        
        # Draw instructions
        font = self.get_font(24)
        instructions = [
            "Use LEFT/RIGHT arrows or A/D keys to steer",
            "Avoid crashing into other cars",
            "Collect orbs for extra points",
            "Press ESC to pause the game",
            "The game gets faster over time"
        ]
        
        y_pos = SCREEN_HEIGHT // 3
        for instruction in instructions:
            instr_surf = font.render(instruction, True, (255, 255, 255))
            self.screen.blit(instr_surf, 
                       (SCREEN_WIDTH // 2 - instr_surf.get_width() // 2, 
                        y_pos))
            y_pos += 40
        
        # Back instructions
        back_text = "Press ESC to return to Main Menu"
        back_surf = font.render(back_text, True, NEON_ORANGE)
        self.screen.blit(back_surf, 
                   (SCREEN_WIDTH // 2 - back_surf.get_width() // 2, 
                    SCREEN_HEIGHT * 2 // 3 + 50))
    
    def save_high_score(self):
        # Save high score to file if it's better than existing scores
        try:
            scores = []
            try:
                with open(os.path.join(os.path.dirname(__file__), "high_scores.json"), 'r') as f:
                    scores = json.load(f)
            except:
                scores = []
            
            # Add current score if it's high enough
            if self.score > 0:
                # Get player initials (default to "AAA")
                player_name = "AAA"
                
                # Add to scores and sort
                scores.append({"name": player_name, "score": self.score})
                scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]  # Keep top 10
                
                # Save back to file
                with open(os.path.join(os.path.dirname(__file__), "high_scores.json"), 'w') as f:
                    json.dump(scores, f)
        except:
            pass
            
    def reset(self):
        self.game_over = False
        self.score = 0
        self.scroll_speed = INITIAL_SCROLL_SPEED
        self.enemy_speed = INITIAL_ENEMY_SPEED
        self.player = Car(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100, NEON_PINK, True)
        self.enemies = []
        self.orbs = []
        self.game_time = 0
        
        # Remove game over buttons reference to recreate them next time
        if hasattr(self, 'game_over_buttons'):
            delattr(self, 'game_over_buttons')
        
        # Restart engine sound
        if self.has_sound:
            sound_manager.play_engine_sound()
    
    def run(self):
        # Main game loop
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Helper classes
class Car:
    def __init__(self, x, y, color=(0, 191, 255), is_player=False):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.color = color
        self.is_player = is_player
        self.speed = PLAYER_SPEED if is_player else INITIAL_ENEMY_SPEED
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Create sprite
        self.sprite = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Main body
        pygame.draw.rect(self.sprite, color, (5, 10, self.width-10, self.height-20))
        
        # Top part (cabin)
        pygame.draw.rect(self.sprite, color, (10, 5, self.width-20, 10))
        
        # Wheels
        wheel_color = (30, 30, 30)
        pygame.draw.rect(self.sprite, wheel_color, (2, 15, 6, 12))
        pygame.draw.rect(self.sprite, wheel_color, (self.width-8, 15, 6, 12))
        pygame.draw.rect(self.sprite, wheel_color, (2, self.height-27, 6, 12))
        pygame.draw.rect(self.sprite, wheel_color, (self.width-8, self.height-27, 6, 12))
        
        # Windshield
        pygame.draw.rect(self.sprite, (100, 200, 255), (12, 12, self.width-24, 8))
        
        # Headlights
        pygame.draw.rect(self.sprite, (255, 255, 200), (8, 5, 6, 4))
        pygame.draw.rect(self.sprite, (255, 255, 200), (self.width-14, 5, 6, 4))
        
        # Taillights
        pygame.draw.rect(self.sprite, (255, 0, 0), (8, self.height-9, 6, 4))
        pygame.draw.rect(self.sprite, (255, 0, 0), (self.width-14, self.height-9, 6, 4))
        
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
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius*2, self.radius*2)
        self.collected = False
        
        # Create sprite
        self.sprite = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        
        # Create glow effect with multiple circles
        for r in range(self.radius, 0, -2):
            alpha = 255 if r == self.radius else int(255 * (r / self.radius))
            color = (*NEON_CYAN[:3], alpha)
            pygame.draw.circle(self.sprite, color, (self.radius, self.radius), r)
        
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

# Helper functions
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