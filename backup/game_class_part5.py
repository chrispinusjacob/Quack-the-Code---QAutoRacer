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