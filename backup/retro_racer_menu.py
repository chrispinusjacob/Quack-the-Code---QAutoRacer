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

# Draw settings screen
def draw_settings_screen():
    # Fill background
    screen.fill((0, 0, 0))
    
    # Draw starfield background
    for i in range(100):
        x = (i * 17) % SCREEN_WIDTH
        y = (i * 23) % SCREEN_HEIGHT
        size = random.randint(1, 3)
        color = (100, 100, 100)
        pygame.draw.circle(screen, color, (x, y), size)
    
    # Draw title
    title_font = get_font(48)
    title_text = "SETTINGS"
    title_surf = title_font.render(title_text, True, NEON_BLUE)
    screen.blit(title_surf, 
               (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                SCREEN_HEIGHT // 6))
    
    # Draw settings options
    font = get_font(24)
    
    # Theme setting
    theme_text = f"THEME: {CONFIG['track_theme'].upper()}"
    theme_surf = font.render(theme_text, True, NEON_GREEN)
    screen.blit(theme_surf, 
               (SCREEN_WIDTH // 2 - theme_surf.get_width() // 2, 
                SCREEN_HEIGHT // 3))
    
    # Difficulty setting
    difficulty = "MEDIUM"  # Default
    difficulty_text = f"DIFFICULTY: {difficulty}"
    difficulty_surf = font.render(difficulty_text, True, NEON_PURPLE)
    screen.blit(difficulty_surf, 
               (SCREEN_WIDTH // 2 - difficulty_surf.get_width() // 2, 
                SCREEN_HEIGHT // 3 + 50))
    
    # Music setting
    music_text = "MUSIC: ON"
    music_surf = font.render(music_text, True, NEON_YELLOW)
    screen.blit(music_surf, 
               (SCREEN_WIDTH // 2 - music_surf.get_width() // 2, 
                SCREEN_HEIGHT // 3 + 100))
    
    # Back instructions
    back_text = "Press ESC to return to Main Menu"
    back_surf = font.render(back_text, True, NEON_ORANGE)
    screen.blit(back_surf, 
               (SCREEN_WIDTH // 2 - back_surf.get_width() // 2, 
                SCREEN_HEIGHT * 2 // 3))

# Draw high scores screen
def draw_high_scores_screen():
    # Fill background
    screen.fill((0, 0, 0))
    
    # Draw starfield background
    for i in range(100):
        x = (i * 17) % SCREEN_WIDTH
        y = (i * 23) % SCREEN_HEIGHT
        size = random.randint(1, 3)
        color = (100, 100, 100)
        pygame.draw.circle(screen, color, (x, y), size)
    
    # Draw title
    title_font = get_font(48)
    title_text = "HIGH SCORES"
    title_surf = title_font.render(title_text, True, NEON_PURPLE)
    screen.blit(title_surf, 
               (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                SCREEN_HEIGHT // 6))
    
    # Draw high scores
    font = get_font(24)
    
    # Sample high scores (replace with actual high scores)
    high_scores = [
        {"name": "AAA", "score": 5000},
        {"name": "BBB", "score": 4000},
        {"name": "CCC", "score": 3000},
        {"name": "DDD", "score": 2000},
        {"name": "EEE", "score": 1000}
    ]
    
    # Try to load high scores from file
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
        screen.blit(score_surf, 
                   (SCREEN_WIDTH // 2 - score_surf.get_width() // 2, 
                    y_pos))
        y_pos += 40
    
    # Back instructions
    back_text = "Press ESC to return to Main Menu"
    back_surf = font.render(back_text, True, NEON_ORANGE)
    screen.blit(back_surf, 
               (SCREEN_WIDTH // 2 - back_surf.get_width() // 2, 
                SCREEN_HEIGHT * 2 // 3))

# Draw instructions screen
def draw_instructions_screen():
    # Fill background
    screen.fill((0, 0, 0))
    
    # Draw starfield background
    for i in range(100):
        x = (i * 17) % SCREEN_WIDTH
        y = (i * 23) % SCREEN_HEIGHT
        size = random.randint(1, 3)
        color = (100, 100, 100)
        pygame.draw.circle(screen, color, (x, y), size)
    
    # Draw title
    title_font = get_font(48)
    title_text = "INSTRUCTIONS"
    title_surf = title_font.render(title_text, True, NEON_YELLOW)
    screen.blit(title_surf, 
               (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 
                SCREEN_HEIGHT // 6))
    
    # Draw instructions
    font = get_font(24)
    instructions = [
        "Use LEFT/RIGHT arrows or A/D keys to steer",
        "Avoid crashing into other cars",
        "Collect orbs for extra points",
        "Press ESC to pause the game"
    ]
    
    y_pos = SCREEN_HEIGHT // 3
    for instruction in instructions:
        instr_surf = font.render(instruction, True, WHITE)
        screen.blit(instr_surf, 
                   (SCREEN_WIDTH // 2 - instr_surf.get_width() // 2, 
                    y_pos))
        y_pos += 40
    
    # Back instructions
    back_text = "Press ESC to return to Main Menu"
    back_surf = font.render(back_text, True, NEON_ORANGE)
    screen.blit(back_surf, 
               (SCREEN_WIDTH // 2 - back_surf.get_width() // 2, 
                SCREEN_HEIGHT * 2 // 3))