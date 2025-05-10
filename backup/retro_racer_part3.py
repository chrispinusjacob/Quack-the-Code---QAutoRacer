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