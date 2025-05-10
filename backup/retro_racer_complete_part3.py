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