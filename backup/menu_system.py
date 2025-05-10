import pygame
import sys
import math
import random
import os
import json
from pygame.locals import *
from config import *  # Import all constants and configurations

# Game states
STATE_MAIN_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_PAUSED = 3
STATE_SETTINGS = 4
STATE_HIGH_SCORES = 5
STATE_INSTRUCTIONS = 6

# Button class for menus
class Button:
    def __init__(self, x, y, width, height, text, color=NEON_BLUE, hover_color=NEON_PINK, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.click_sound = None
        self.hover_sound = None
        
        # Try to load sounds if available
        try:
            self.click_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "click.mp3"))
            self.hover_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "hover.mp3"))
        except:
            pass
        
    def draw(self, surface, font):
        # Draw button with hover effect
        color = self.hover_color if self.is_hovered else self.color
        
        # Draw button background with glow effect
        for i in range(5, 0, -1):
            glow_rect = pygame.Rect(
                self.rect.x - i, self.rect.y - i, 
                self.rect.width + i*2, self.rect.height + i*2
            )
            pygame.draw.rect(surface, (*color[:3], 50), glow_rect, border_radius=5)
        
        # Main button
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=5)  # Border
        
        # Button text
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos):
        # Check if hover state changed
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Play hover sound if just started hovering
        if not was_hovered and self.is_hovered and self.hover_sound:
            self.hover_sound.play()
        
    def is_clicked(self, mouse_pos, mouse_click):
        # Check if button was clicked
        clicked = self.rect.collidepoint(mouse_pos) and mouse_click
        if clicked and self.click_sound:
            self.click_sound.play()
        return clicked

class MainMenu:
    def __init__(self, screen, font_function):
        self.screen = screen
        self.get_font = font_function
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.state = STATE_MAIN_MENU
        self.time = 0
        
        # Try to load menu music
        self.menu_music = None
        try:
            self.menu_music = pygame.mixer.Sound(os.path.join(SOUND_DIR, "menu_music.mp3"))
            self.menu_music.play(-1)
        except:
            pass
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = self.screen_height // 3
        
        self.buttons = {
            "start": Button(
                self.screen_width // 2 - button_width // 2,
                start_y,
                button_width, button_height,
                "START GAME", NEON_GREEN
            ),
            "settings": Button(
                self.screen_width // 2 - button_width // 2,
                start_y + button_height + button_spacing,
                button_width, button_height,
                "SETTINGS", NEON_BLUE
            ),
            "high_scores": Button(
                self.screen_width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 2,
                button_width, button_height,
                "HIGH SCORES", NEON_PURPLE
            ),
            "instructions": Button(
                self.screen_width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 3,
                button_width, button_height,
                "INSTRUCTIONS", NEON_YELLOW
            ),
            "exit": Button(
                self.screen_width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 4,
                button_width, button_height,
                "EXIT", NEON_ORANGE
            )
        }
        
        # Random tips for the menu screen
        self.tips = [
            "TIP: Use arrow keys or A/D to steer your car",
            "TIP: Collect orbs for extra points",
            "TIP: The game gets faster over time",
            "TIP: Press ESC to pause the game",
            "TIP: Try different color schemes in settings"
        ]
        self.current_tip = random.choice(self.tips)
        self.tip_timer = 0
        
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
        
        # Update all buttons
        for button in self.buttons.values():
            button.update(mouse_pos)
        
        # Check for button clicks
        if mouse_clicked:
            if self.buttons["start"].is_clicked(mouse_pos, mouse_clicked):
                if self.menu_music:
                    self.menu_music.stop()
                return STATE_PLAYING
            elif self.buttons["settings"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_SETTINGS
            elif self.buttons["high_scores"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_HIGH_SCORES
            elif self.buttons["instructions"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_INSTRUCTIONS
            elif self.buttons["exit"].is_clicked(mouse_pos, mouse_clicked):
                pygame.quit()
                sys.exit()
        
        return self.state
    
    def update(self, dt):
        self.time += dt
        
        # Update tip every 5 seconds
        self.tip_timer += dt
        if self.tip_timer > 5:
            self.current_tip = random.choice(self.tips)
            self.tip_timer = 0
    
    def draw(self):
        # Fill background
        self.screen.fill((0, 0, 0))
        
        # Draw starfield background
        for i in range(100):
            x = (i * 17) % self.screen_width
            y = (i * 23) % self.screen_height
            size = random.randint(1, 3)
            brightness = 100 + int(math.sin(self.time + i) * 50)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (x, y), size)
        
        # Draw title
        title_font = self.get_font(72)
        title_text = "QAutoGame '90"
        title_surf = title_font.render(title_text, True, NEON_PINK)
        
        # Add glow effect to title
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_PINK[:3], 25 * i))
            self.screen.blit(glow_surf, 
                       (self.screen_width // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        self.screen_height // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
        
        self.screen.blit(title_surf, 
                   (self.screen_width // 2 - title_surf.get_width() // 2, 
                    self.screen_height // 6 - title_surf.get_height() // 2))
        
        # Draw all buttons
        button_font = self.get_font(24)
        for button in self.buttons.values():
            button.draw(self.screen, button_font)
            
        # Draw tip at the bottom
        tip_font = self.get_font(18)
        tip_surf = tip_font.render(self.current_tip, True, NEON_CYAN)
        self.screen.blit(tip_surf, 
                       (self.screen_width // 2 - tip_surf.get_width() // 2, 
                        self.screen_height - 50))

class PauseMenu:
    def __init__(self, screen, font_function):
        self.screen = screen
        self.get_font = font_function
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = self.screen_height // 3
        
        self.buttons = {
            "resume": Button(
                self.screen_width // 2 - button_width // 2,
                start_y,
                button_width, button_height,
                "RESUME", NEON_GREEN
            ),
            "restart": Button(
                self.screen_width // 2 - button_width // 2,
                start_y + button_height + button_spacing,
                button_width, button_height,
                "RESTART", NEON_BLUE
            ),
            "main_menu": Button(
                self.screen_width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 2,
                button_width, button_height,
                "MAIN MENU", NEON_PURPLE
            ),
            "quit": Button(
                self.screen_width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 3,
                button_width, button_height,
                "QUIT GAME", NEON_ORANGE
            )
        }
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return STATE_PLAYING
        
        # Update all buttons
        for button in self.buttons.values():
            button.update(mouse_pos)
        
        # Check for button clicks
        if mouse_clicked:
            if self.buttons["resume"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_PLAYING
            elif self.buttons["restart"].is_clicked(mouse_pos, mouse_clicked):
                # Return special code to indicate restart
                return -1
            elif self.buttons["main_menu"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_MAIN_MENU
            elif self.buttons["quit"].is_clicked(mouse_pos, mouse_clicked):
                pygame.quit()
                sys.exit()
        
        return STATE_PAUSED
    
    def draw(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause title
        title_font = self.get_font(48)
        title_text = "PAUSED"
        title_surf = title_font.render(title_text, True, NEON_YELLOW)
        
        # Add glow effect to title
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_YELLOW[:3], 25 * i))
            self.screen.blit(glow_surf, 
                       (self.screen_width // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        self.screen_height // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
        
        self.screen.blit(title_surf, 
                   (self.screen_width // 2 - title_surf.get_width() // 2, 
                    self.screen_height // 6 - title_surf.get_height() // 2))
        
        # Draw all buttons
        button_font = self.get_font(24)
        for button in self.buttons.values():
            button.draw(self.screen, button_font)

class SettingsMenu:
    def __init__(self, screen, font_function):
        self.screen = screen
        self.get_font = font_function
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = self.screen_height // 3
        
        self.buttons = {
            "music_toggle": Button(
                self.screen_width // 2 - button_width // 2,
                start_y,
                button_width, button_height,
                "MUSIC: ON", NEON_GREEN
            ),
            "difficulty": Button(
                self.screen_width // 2 - button_width // 2,
                start_y + button_height + button_spacing,
                button_width, button_height,
                "DIFFICULTY: MEDIUM", NEON_BLUE
            ),
            "theme": Button(
                self.screen_width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 2,
                button_width, button_height,
                f"THEME: {CONFIG['track_theme'].upper()}", NEON_PURPLE
            ),
            "back": Button(
                self.screen_width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 3,
                button_width, button_height,
                "BACK", NEON_ORANGE
            )
        }
        
        # Settings state
        self.music_on = True
        self.difficulty = "MEDIUM"  # EASY, MEDIUM, HARD
        self.themes = ["synthwave", "cyberpunk", "retrowave", "night"]
        self.current_theme_index = self.themes.index(CONFIG["track_theme"])
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return STATE_MAIN_MENU
        
        # Update all buttons
        for button in self.buttons.values():
            button.update(mouse_pos)
        
        # Check for button clicks
        if mouse_clicked:
            if self.buttons["music_toggle"].is_clicked(mouse_pos, mouse_clicked):
                self.music_on = not self.music_on
                self.buttons["music_toggle"].text = f"MUSIC: {'ON' if self.music_on else 'OFF'}"
                # TODO: Actually toggle music
            elif self.buttons["difficulty"].is_clicked(mouse_pos, mouse_clicked):
                if self.difficulty == "EASY":
                    self.difficulty = "MEDIUM"
                elif self.difficulty == "MEDIUM":
                    self.difficulty = "HARD"
                else:
                    self.difficulty = "EASY"
                self.buttons["difficulty"].text = f"DIFFICULTY: {self.difficulty}"
                # TODO: Actually change difficulty
            elif self.buttons["theme"].is_clicked(mouse_pos, mouse_clicked):
                self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
                theme = self.themes[self.current_theme_index]
                CONFIG["track_theme"] = theme
                self.buttons["theme"].text = f"THEME: {theme.upper()}"
            elif self.buttons["back"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_MAIN_MENU
        
        return STATE_SETTINGS
    
    def draw(self):
        # Fill background with current theme color
        theme_color = COLOR_SCHEMES[CONFIG["track_theme"]]["sky"]
        self.screen.fill(theme_color)
        
        # Draw starfield background
        for i in range(100):
            x = (i * 17) % self.screen_width
            y = (i * 23) % self.screen_height
            size = random.randint(1, 3)
            color = (200, 200, 200)
            pygame.draw.circle(self.screen, color, (x, y), size)
        
        # Draw title
        title_font = self.get_font(48)
        title_text = "SETTINGS"
        title_surf = title_font.render(title_text, True, NEON_YELLOW)
        
        # Add glow effect to title
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_YELLOW[:3], 25 * i))
            self.screen.blit(glow_surf, 
                       (self.screen_width // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        self.screen_height // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
        
        self.screen.blit(title_surf, 
                   (self.screen_width // 2 - title_surf.get_width() // 2, 
                    self.screen_height // 6 - title_surf.get_height() // 2))
        
        # Draw all buttons
        button_font = self.get_font(24)
        for button in self.buttons.values():
            button.draw(self.screen, button_font)

class InstructionsMenu:
    def __init__(self, screen, font_function):
        self.screen = screen
        self.get_font = font_function
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Create back button
        button_width = 200
        button_height = 50
        self.back_button = Button(
            self.screen_width // 2 - button_width // 2,
            self.screen_height - 100,
            button_width, button_height,
            "BACK", NEON_ORANGE
        )
        
        # Instructions text
        self.instructions = [
            "HOW TO PLAY",
            "",
            "CONTROLS:",
            "- LEFT ARROW or A: Move left",
            "- RIGHT ARROW or D: Move right",
            "- ESC: Pause game",
            "",
            "OBJECTIVE:",
            "- Avoid crashing into other cars",
            "- Collect orbs for extra points",
            "- Survive as long as possible",
            "",
            "TIPS:",
            "- The game gets faster over time",
            "- Your score increases with time and orbs"
        ]
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return STATE_MAIN_MENU
        
        # Update back button
        self.back_button.update(mouse_pos)
        
        # Check for button click
        if mouse_clicked and self.back_button.is_clicked(mouse_pos, mouse_clicked):
            return STATE_MAIN_MENU
        
        return STATE_INSTRUCTIONS
    
    def draw(self):
        # Fill background
        self.screen.fill((0, 0, 0))
        
        # Draw starfield background
        for i in range(100):
            x = (i * 17) % self.screen_width
            y = (i * 23) % self.screen_height
            size = random.randint(1, 3)
            color = (100, 100, 100)
            pygame.draw.circle(self.screen, color, (x, y), size)
        
        # Draw title
        title_font = self.get_font(48)
        title_text = "INSTRUCTIONS"
        title_surf = title_font.render(title_text, True, NEON_CYAN)
        
        # Add glow effect to title
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_CYAN[:3], 25 * i))
            self.screen.blit(glow_surf, 
                       (self.screen_width // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        50 + random.randint(-i, i)))
        
        self.screen.blit(title_surf, 
                   (self.screen_width // 2 - title_surf.get_width() // 2, 
                    50))
        
        # Draw instructions text
        text_font = self.get_font(20)
        y_pos = 150
        for line in self.instructions:
            if line == "":
                y_pos += 15  # Add extra space for empty lines
            else:
                text_surf = text_font.render(line, True, NEON_GREEN if line.endswith(":") else (255, 255, 255))
                self.screen.blit(text_surf, 
                           (self.screen_width // 2 - text_surf.get_width() // 2, 
                            y_pos))
            y_pos += 30
        
        # Draw back button
        button_font = self.get_font(24)
        self.back_button.draw(self.screen, button_font)

class HighScoresMenu:
    def __init__(self, screen, font_function):
        self.screen = screen
        self.get_font = font_function
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Create buttons
        button_width = 200
        button_height = 50
        self.buttons = {
            "back": Button(
                self.screen_width // 2 - button_width // 2,
                self.screen_height - 100,
                button_width, button_height,
                "BACK", NEON_ORANGE
            ),
            "reset": Button(
                self.screen_width // 2 - button_width // 2,
                self.screen_height - 160,
                button_width, button_height,
                "RESET SCORES", NEON_RED
            )
        }
        
        # Load high scores
        self.high_scores = self.load_high_scores()
    
    def load_high_scores(self, filename="high_scores.json"):
        """Load high scores from a JSON file"""
        filepath = os.path.join(os.path.dirname(__file__), filename)
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return empty scores if file doesn't exist or is invalid
            return [{"name": "AAA", "score": 5000},
                    {"name": "BBB", "score": 4000},
                    {"name": "CCC", "score": 3000},
                    {"name": "DDD", "score": 2000},
                    {"name": "EEE", "score": 1000}]
    
    def save_high_scores(self, scores, filename="high_scores.json"):
        """Save high scores to a JSON file"""
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, 'w') as f:
            json.dump(scores, f)
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return STATE_MAIN_MENU
        
        # Update all buttons
        for button in self.buttons.values():
            button.update(mouse_pos)
        
        # Check for button clicks
        if mouse_clicked:
            if self.buttons["back"].is_clicked(mouse_pos, mouse_clicked):
                return STATE_MAIN_MENU
            elif self.buttons["reset"].is_clicked(mouse_pos, mouse_clicked):
                self.high_scores = [{"name": "AAA", "score": 5000},
                                   {"name": "BBB", "score": 4000},
                                   {"name": "CCC", "score": 3000},
                                   {"name": "DDD", "score": 2000},
                                   {"name": "EEE", "score": 1000}]
                self.save_high_scores(self.high_scores)
        
        return STATE_HIGH_SCORES
    
    def draw(self):
        # Fill background
        self.screen.fill((0, 0, 0))
        
        # Draw starfield background
        for i in range(100):
            x = (i * 17) % self.screen_width
            y = (i * 23) % self.screen_height
            size = random.randint(1, 3)
            color = (100, 100, 100)
            pygame.draw.circle(self.screen, color, (x, y), size)
        
        # Draw title
        title_font = self.get_font(48)
        title_text = "HIGH SCORES"
        title_surf = title_font.render(title_text, True, NEON_PURPLE)
        
        # Add glow effect to title
        for i in range(10, 0, -2):
            glow_surf = title_font.render(title_text, True, (*NEON_PURPLE[:3], 25 * i))
            self.screen.blit(glow_surf, 
                       (self.screen_width // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                        50 + random.randint(-i, i)))
        
        self.screen.blit(title_surf, 
                   (self.screen_width // 2 - title_surf.get_width() // 2, 
                    50))
        
        # Draw high scores
        score_font = self.get_font(28)
        y_pos = 150
        for i, score_data in enumerate(self.high_scores[:10]):  # Show top 10 scores
            rank_text = f"{i+1}."
            name_text = score_data["name"]
            score_text = str(score_data["score"])
            
            # Rank
            rank_surf = score_font.render(rank_text, True, NEON_YELLOW)
            self.screen.blit(rank_surf, (self.screen_width // 4, y_pos))
            
            # Name
            name_surf = score_font.render(name_text, True, NEON_GREEN)
            self.screen.blit(name_surf, (self.screen_width // 4 + 50, y_pos))
            
            # Score
            score_surf = score_font.render(score_text, True, NEON_PINK)
            self.screen.blit(score_surf, (self.screen_width // 4 + 200, y_pos))
            
            y_pos += 40
        
        # Draw buttons
        button_font = self.get_font(24)
        for button in self.buttons.values():
            button.draw(self.screen, button_font)

# Save and load functions
def save_high_scores(scores, filename="high_scores.json"):
    """Save high scores to a JSON file"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'w') as f:
        json.dump(scores, f)

def load_high_scores(filename="high_scores.json"):
    """Load high scores from a JSON file"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty scores if file doesn't exist or is invalid
        return []

def save_game_state(state, filename="game_save.json"):
    """Save game state to a JSON file"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'w') as f:
        json.dump(state, f)

def load_game_state(filename="game_save.json"):
    """Load game state from a JSON file"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return None if file doesn't exist or is invalid
        return None