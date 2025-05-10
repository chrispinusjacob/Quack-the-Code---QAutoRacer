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