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