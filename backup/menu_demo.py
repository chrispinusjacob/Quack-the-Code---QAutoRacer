import pygame
import sys
import math
import random
import os
from pygame.locals import *
from config import *  # Import all constants and configurations
from menu_system import *  # Import the menu system

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("QAutoGame '90 - Menu Demo")
clock = pygame.time.Clock()

# Create pixel fonts
def get_font(size):
    try:
        return pygame.font.Font(os.path.join(FONT_DIR, "pixel.ttf"), size)
    except:
        return pygame.font.SysFont("Arial", size)

# Create menu objects
main_menu = MainMenu(screen, get_font)
pause_menu = PauseMenu(screen, get_font)
settings_menu = SettingsMenu(screen, get_font)
instructions_menu = InstructionsMenu(screen, get_font)
high_scores_menu = HighScoresMenu(screen, get_font)

# Game state
current_state = STATE_MAIN_MENU
running = True
game_time = 0

# Main game loop
while running:
    dt = clock.get_time() / 1000.0  # Delta time in seconds
    game_time += dt
    
    # Handle events
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if current_state == STATE_PLAYING:
                    current_state = STATE_PAUSED
                elif current_state == STATE_PAUSED:
                    current_state = STATE_PLAYING
                elif current_state in [STATE_SETTINGS, STATE_INSTRUCTIONS, STATE_HIGH_SCORES]:
                    current_state = STATE_MAIN_MENU
    
    # Handle menu states
    if current_state == STATE_MAIN_MENU:
        new_state = main_menu.handle_events(events)
        if new_state != current_state:
            current_state = new_state
        main_menu.update(dt)
    elif current_state == STATE_PAUSED:
        new_state = pause_menu.handle_events(events)
        if new_state != current_state and new_state != -1:
            current_state = new_state
    elif current_state == STATE_SETTINGS:
        new_state = settings_menu.handle_events(events)
        if new_state != current_state:
            current_state = new_state
    elif current_state == STATE_INSTRUCTIONS:
        new_state = instructions_menu.handle_events(events)
        if new_state != current_state:
            current_state = new_state
    elif current_state == STATE_HIGH_SCORES:
        new_state = high_scores_menu.handle_events(events)
        if new_state != current_state:
            current_state = new_state
    
    # Draw appropriate screen based on state
    if current_state == STATE_MAIN_MENU:
        main_menu.draw()
    elif current_state == STATE_PLAYING:
        # Draw simple game screen
        screen.fill(BLACK)
        
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
        # Draw simple game screen (as background)
        screen.fill(BLACK)
        
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
        
        # Draw pause menu
        pause_menu.draw()
    elif current_state == STATE_SETTINGS:
        settings_menu.draw()
    elif current_state == STATE_INSTRUCTIONS:
        instructions_menu.draw()
    elif current_state == STATE_HIGH_SCORES:
        high_scores_menu.draw()
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()