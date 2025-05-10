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