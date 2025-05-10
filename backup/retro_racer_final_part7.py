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