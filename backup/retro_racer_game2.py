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