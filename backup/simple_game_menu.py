import pygame
import sys
import math
import random
import os
import json
from pygame.locals import *
from config import *  # Import all constants and configurations

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("QAutoGame '90")
clock = pygame.time.Clock()

# Game states
STATE_MAIN_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_PAUSED = 3
STATE_SETTINGS = 4
STATE_HIGH_SCORES = 5
STATE_INSTRUCTIONS = 6

# Colors (for convenience)
NEON_CYAN = (0, 255, 255)

# Asset paths
FONT_DIR = os.path.join(ASSET_DIR, "fonts")
SPRITE_DIR = os.path.join(ASSET_DIR, "sprites")

# Create directories if they don't exist
os.makedirs(FONT_DIR, exist_ok=True)
os.makedirs(SPRITE_DIR, exist_ok=True)

# Simple Button class
class SimpleButton:
    def __init__(self, x, y, width, height, text, color=NEON_BLUE, hover_color=NEON_PINK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface, font):
        # Draw button with hover effect
        color = self.hover_color if self.is_hovered else self.color
        
        # Main button
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=5)  # Border
        
        # Button text
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos):
        # Check if hover state changed
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        # Check if button was clicked
        return self.rect.collidepoint(mouse_pos) and mouse_click

# Get font function
def get_font(size):
    try:
        return pygame.font.Font(os.path.join(FONT_DIR, "pixel.ttf"), size)
    except:
        return pygame.font.SysFont("Arial", size)

# Load sounds
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

# Create menu buttons
def create_main_menu_buttons():
    button_width = 200
    button_height = 50
    button_spacing = 20
    start_y = SCREEN_HEIGHT // 3
    
    buttons = {
        "start": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y,
            button_width, button_height,
            "START GAME", NEON_GREEN
        ),
        "settings": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + button_height + button_spacing,
            button_width, button_height,
            "SETTINGS", NEON_BLUE
        ),
        "high_scores": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + (button_height + button_spacing) * 2,
            button_width, button_height,
            "HIGH SCORES", NEON_PURPLE
        ),
        "instructions": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + (button_height + button_spacing) * 3,
            button_width, button_height,
            "INSTRUCTIONS", NEON_YELLOW
        ),
        "exit": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + (button_height + button_spacing) * 4,
            button_width, button_height,
            "EXIT", NEON_ORANGE
        )
    }
    
    return buttons

def create_pause_menu_buttons():
    button_width = 200
    button_height = 50
    button_spacing = 20
    start_y = SCREEN_HEIGHT // 3
    
    buttons = {
        "resume": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y,
            button_width, button_height,
            "RESUME", NEON_GREEN
        ),
        "restart": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + button_height + button_spacing,
            button_width, button_height,
            "RESTART", NEON_BLUE
        ),
        "main_menu": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + (button_height + button_spacing) * 2,
            button_width, button_height,
            "MAIN MENU", NEON_PURPLE
        ),
        "quit": SimpleButton(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + (button_height + button_spacing) * 3,
            button_width, button_height,
            "QUIT GAME", NEON_ORANGE
        )
    }
    
    return buttons

# Draw main menu
def draw_main_menu(buttons, game_time):
    # Fill background
    screen.fill((0, 0, 0))
    
    # Draw starfield background
    for i in range(100):
        x = (i * 17) % SCREEN_WIDTH
        y = (i * 23) % SCREEN_HEIGHT
        size = random.randint(1, 3)
        brightness = 100 + int(math.sin(game_time + i) * 50)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(screen, color, (x, y), size)
    
    # Draw title
    title_font = get_font(72)
    title_text = "QAutoGame '90"
    title_surf = title_font.render(title_text, True, NEON_PINK)
    
    # Add glow effect to title
    for i in range(10, 0, -2):
        glow_surf = title_font.render(title_text, True, NEON_PINK)
        screen.blit(glow_surf, 
                   (SCREEN_WIDTH // 2 - title_surf.get_width() // 2 + random.randint(-i, i), 
                    SCREEN_HEIGHT // 6 - title_surf.get_height() // 2 + random.randint(-i, i)))
    
    screen.blit(title_surf, 
               (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                SCREEN_HEIGHT // 6 - title_surf.get_height() // 2))
    
    # Draw all buttons
    button_font = get_font(24)
    for button in buttons.values():
        button.draw(screen, button_font)
        
    # Draw tip at the bottom
    tips = [
        "TIP: Use arrow keys or A/D to steer your car",
        "TIP: Collect orbs for extra points",
        "TIP: The game gets faster over time",
        "TIP: Press ESC to pause the game",
        "TIP: Try different color schemes in settings"
    ]
    tip_text = tips[int(game_time / 5) % len(tips)]
    tip_font = get_font(18)
    tip_surf = tip_font.render(tip_text, True, NEON_CYAN)
    screen.blit(tip_surf, 
               (SCREEN_WIDTH // 2 - tip_surf.get_width() // 2, 
                SCREEN_HEIGHT - 50))

# Draw pause menu
def draw_pause_menu(buttons):
    # Create semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    # Draw pause title
    title_font = get_font(48)
    title_text = "PAUSED"
    title_surf = title_font.render(title_text, True, NEON_YELLOW)
    
    screen.blit(title_surf, 
               (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                SCREEN_HEIGHT // 6 - title_surf.get_height() // 2))
    
    # Draw all buttons
    button_font = get_font(24)
    for button in buttons.values():
        button.draw(screen, button_font)

# Main function
def main():
    # Game state
    current_state = STATE_MAIN_MENU
    game_time = 0
    running = True
    
    # Create menu buttons
    main_menu_buttons = create_main_menu_buttons()
    pause_menu_buttons = create_pause_menu_buttons()
    
    # Main game loop
    while running:
        # Calculate delta time
        dt = clock.get_time() / 1000.0
        game_time += dt
        
        # Handle events
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
                print(f"Mouse clicked at: {mouse_pos}")  # Debug print
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if current_state == STATE_PLAYING:
                        current_state = STATE_PAUSED
                    elif current_state == STATE_PAUSED:
                        current_state = STATE_PLAYING
                    elif current_state in [STATE_SETTINGS, STATE_INSTRUCTIONS, STATE_HIGH_SCORES]:
                        current_state = STATE_MAIN_MENU
        
        # Update buttons based on current state
        if current_state == STATE_MAIN_MENU:
            for button in main_menu_buttons.values():
                button.update(mouse_pos)
            
            # Check for button clicks
            if mouse_clicked:
                if main_menu_buttons["start"].is_clicked(mouse_pos, mouse_clicked):
                    print("Start button clicked!")
                    current_state = STATE_PLAYING
                elif main_menu_buttons["settings"].is_clicked(mouse_pos, mouse_clicked):
                    print("Settings button clicked!")
                    current_state = STATE_SETTINGS
                elif main_menu_buttons["high_scores"].is_clicked(mouse_pos, mouse_clicked):
                    print("High Scores button clicked!")
                    current_state = STATE_HIGH_SCORES
                elif main_menu_buttons["instructions"].is_clicked(mouse_pos, mouse_clicked):
                    print("Instructions button clicked!")
                    current_state = STATE_INSTRUCTIONS
                elif main_menu_buttons["exit"].is_clicked(mouse_pos, mouse_clicked):
                    print("Exit button clicked!")
                    running = False
        
        elif current_state == STATE_PAUSED:
            for button in pause_menu_buttons.values():
                button.update(mouse_pos)
            
            # Check for button clicks
            if mouse_clicked:
                if pause_menu_buttons["resume"].is_clicked(mouse_pos, mouse_clicked):
                    print("Resume button clicked!")
                    current_state = STATE_PLAYING
                elif pause_menu_buttons["restart"].is_clicked(mouse_pos, mouse_clicked):
                    print("Restart button clicked!")
                    # Reset game here
                    current_state = STATE_PLAYING
                elif pause_menu_buttons["main_menu"].is_clicked(mouse_pos, mouse_clicked):
                    print("Main Menu button clicked!")
                    current_state = STATE_MAIN_MENU
                elif pause_menu_buttons["quit"].is_clicked(mouse_pos, mouse_clicked):
                    print("Quit button clicked!")
                    running = False
        
        # Draw based on current state
        if current_state == STATE_MAIN_MENU:
            draw_main_menu(main_menu_buttons, game_time)
        
        elif current_state == STATE_PLAYING:
            # Draw simple game screen
            screen.fill((0, 0, 0))
            
            # Draw starfield background
            for i in range(100):
                x = (i * 17) % SCREEN_WIDTH
                y = (i * 23) % SCREEN_HEIGHT
                size = random.randint(1, 3)
                brightness = 100 + int(math.sin(game_time + i) * 50)
                color = (brightness, brightness, brightness)
                pygame.draw.circle(screen, color, (x, y), size)
            
            # Draw game text
            font = get_font(36)
            text = "Game Running - Press ESC to Pause"
            text_surf = font.render(text, True, NEON_GREEN)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text_surf, text_rect)
            
            # Draw time
            time_text = f"Time: {game_time:.1f}s"
            time_surf = font.render(time_text, True, NEON_BLUE)
            screen.blit(time_surf, (20, 20))
        
        elif current_state == STATE_PAUSED:
            # First draw the game screen (simplified)
            screen.fill((0, 0, 0))
            
            # Draw starfield background
            for i in range(100):
                x = (i * 17) % SCREEN_WIDTH
                y = (i * 23) % SCREEN_HEIGHT
                size = random.randint(1, 3)
                brightness = 100 + int(math.sin(game_time + i) * 50)
                color = (brightness, brightness, brightness)
                pygame.draw.circle(screen, color, (x, y), size)
            
            # Draw game text
            font = get_font(36)
            text = "Game Running - Press ESC to Pause"
            text_surf = font.render(text, True, NEON_GREEN)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text_surf, text_rect)
            
            # Then draw the pause menu
            draw_pause_menu(pause_menu_buttons)
        
        elif current_state == STATE_SETTINGS:
            # Draw settings screen
            screen.fill((0, 0, 0))
            font = get_font(48)
            text = "SETTINGS"
            text_surf = font.render(text, True, NEON_BLUE)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(text_surf, text_rect)
            
            # Back instructions
            font_small = get_font(24)
            back_text = "Press ESC to return to Main Menu"
            back_surf = font_small.render(back_text, True, NEON_YELLOW)
            back_rect = back_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
            screen.blit(back_surf, back_rect)
        
        elif current_state == STATE_HIGH_SCORES:
            # Draw high scores screen
            screen.fill((0, 0, 0))
            font = get_font(48)
            text = "HIGH SCORES"
            text_surf = font.render(text, True, NEON_PURPLE)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(text_surf, text_rect)
            
            # Back instructions
            font_small = get_font(24)
            back_text = "Press ESC to return to Main Menu"
            back_surf = font_small.render(back_text, True, NEON_YELLOW)
            back_rect = back_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
            screen.blit(back_surf, back_rect)
        
        elif current_state == STATE_INSTRUCTIONS:
            # Draw instructions screen
            screen.fill((0, 0, 0))
            font = get_font(48)
            text = "INSTRUCTIONS"
            text_surf = font.render(text, True, NEON_YELLOW)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(text_surf, text_rect)
            
            # Instructions text
            instructions = [
                "Use LEFT/RIGHT arrows or A/D keys to steer",
                "Avoid crashing into other cars",
                "Collect orbs for extra points",
                "Press ESC to pause the game"
            ]
            
            font_small = get_font(24)
            y_pos = 200
            for line in instructions:
                line_surf = font_small.render(line, True, (255, 255, 255))
                line_rect = line_surf.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                screen.blit(line_surf, line_rect)
                y_pos += 50
            
            # Back instructions
            back_text = "Press ESC to return to Main Menu"
            back_surf = font_small.render(back_text, True, NEON_YELLOW)
            back_rect = back_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
            screen.blit(back_surf, back_rect)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()