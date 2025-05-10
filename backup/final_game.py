

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

class Game:
    def __init__(self):
        self.running = True
        self.state = STATE_MAIN_MENU  # Start at main menu
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
        
        # Create menu buttons
        self.main_menu_buttons = create_main_menu_buttons()
        self.pause_menu_buttons = create_pause_menu_buttons()
        
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
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in events:
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.state == STATE_PLAYING:
                        self.state = STATE_PAUSED
                        if has_sound:
                            engine_sound.stop()
                    elif self.state == STATE_PAUSED:
                        self.state = STATE_PLAYING
                        if has_sound and not self.game_over:
                            engine_sound.play(-1)
                    elif self.state in [STATE_SETTINGS, STATE_INSTRUCTIONS, STATE_HIGH_SCORES]:
                        self.state = STATE_MAIN_MENU
                elif event.key == K_SPACE and self.game_over:
                    self.reset()
        
        # Handle menu states
        if self.state == STATE_MAIN_MENU:
            # Update main menu buttons
            for button in self.main_menu_buttons.values():
                button.update(mouse_pos)
            
            # Check for button clicks
            if mouse_clicked:
                if self.main_menu_buttons["start"].is_clicked(mouse_pos, mouse_clicked):
                    self.state = STATE_PLAYING
                    if has_sound:
                        engine_sound.play(-1)
                elif self.main_menu_buttons["settings"].is_clicked(mouse_pos, mouse_clicked):
                    self.state = STATE_SETTINGS
                elif self.main_menu_buttons["high_scores"].is_clicked(mouse_pos, mouse_clicked):
                    self.state = STATE_HIGH_SCORES
                elif self.main_menu_buttons["instructions"].is_clicked(mouse_pos, mouse_clicked):
                    self.state = STATE_INSTRUCTIONS
                elif self.main_menu_buttons["exit"].is_clicked(mouse_pos, mouse_clicked):
                    self.running = False
        
        elif self.state == STATE_PAUSED:
            # Update pause menu buttons
            for button in self.pause_menu_buttons.values():
                button.update(mouse_pos)
            
            # Check for button clicks
            if mouse_clicked:
                if self.pause_menu_buttons["resume"].is_clicked(mouse_pos, mouse_clicked):
                    self.state = STATE_PLAYING
                    if has_sound and not self.game_over:
                        engine_sound.play(-1)
                elif self.pause_menu_buttons["restart"].is_clicked(mouse_pos, mouse_clicked):
                    self.reset()
                    self.state = STATE_PLAYING
                    if has_sound:
                        engine_sound.play(-1)
                elif self.pause_menu_buttons["main_menu"].is_clicked(mouse_pos, mouse_clicked):
                    self.state = STATE_MAIN_MENU
                elif self.pause_menu_buttons["quit"].is_clicked(mouse_pos, mouse_clicked):
                    self.running = False
        
        # Only process game controls if in playing state
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
        dt = clock.get_time() / 1000.0  # Delta time in seconds
        
        # Update menu states
        if self.state == STATE_MAIN_MENU:
            self.game_time += dt  # Keep time running for animations
            return
        elif self.state == STATE_PAUSED or self.state == STATE_SETTINGS or self.state == STATE_INSTRUCTIONS or self.state == STATE_HIGH_SCORES:
            return
        elif self.game_over:
            return
        
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
        screen.fill((0, 0, 0))
        
        # Draw starfield background
        for i in range(100):
            x = (i * 17) % SCREEN_WIDTH
            y = (i * 23) % SCREEN_HEIGHT
            size = random.randint(1, 3)
            brightness = 100 + int(math.sin(self.game_time + i) * 50)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (x, y), size)
        
        # Draw appropriate screen based on state
        if self.state == STATE_MAIN_MENU:
            draw_main_menu(self.main_menu_buttons, self.game_time)
        elif self.state == STATE_SETTINGS:
            draw_settings_screen()
        elif self.state == STATE_HIGH_SCORES:
            draw_high_scores_screen()
        elif self.state == STATE_INSTRUCTIONS:
            draw_instructions_screen()
        else:
            # Draw game elements (only if playing or paused)
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
            
            # Draw pause menu if paused
            if self.state == STATE_PAUSED:
                draw_pause_menu(self.pause_menu_buttons)
        
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
        
        # Save high score
        self.save_high_score()
    
    def save_high_score(self):
        # Load existing high scores
        high_scores = []
        try:
            with open(os.path.join(os.path.dirname(__file__), "high_scores.json"), 'r') as f:
                high_scores = json.load(f)
        except:
            high_scores = []
        
        # Add current score
        high_scores.append({"name": "YOU", "score": self.score})
        
        # Sort and keep top 10
        high_scores.sort(key=lambda x: x["score"], reverse=True)
        high_scores = high_scores[:10]
        
        # Save back to file
        with open(os.path.join(os.path.dirname(__file__), "high_scores.json"), 'w') as f:
            json.dump(high_scores, f)
    
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