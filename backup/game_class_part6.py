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