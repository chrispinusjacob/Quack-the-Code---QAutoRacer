"""
Script to update the game with improved features:
- Progressive speed increases
- Difficulty levels
- Theme selection
- Background music handling
"""

import os
import re

def update_game_class():
    """Update the game_class.py file with new features"""
    
    # Read the current file
    with open('game_class.py', 'r') as f:
        content = f.read()
    
    # Add imports for difficulty and theme managers
    if "from difficulty_manager import difficulty_manager" not in content:
        import_pattern = r"from sound_manager import sound_manager"
        replacement = "from sound_manager import sound_manager\nfrom difficulty_manager import difficulty_manager\nfrom theme_manager import theme_manager"
        content = re.sub(import_pattern, replacement, content)
    
    # Update the update method to use difficulty manager for speed increases
    update_pattern = r"def update\(self\):(.*?)# Increase score based on time"
    update_replacement = r"""def update(self):
        dt = self.clock.get_time() / 1000.0  # Delta time in seconds
        
        if self.state == STATE_MAIN_MENU:
            self.main_menu.update(dt)
            return
        elif self.state == STATE_PAUSED:
            return
        elif self.game_over:
            # Update game over buttons
            if hasattr(self, 'game_over_buttons'):
                mouse_pos = pygame.mouse.get_pos()
                for button in self.game_over_buttons.values():
                    button.update(mouse_pos)
            return
        
        self.game_time += dt
        
        # Get current difficulty settings
        speed_increase_rate = difficulty_manager.get_speed_increase_rate()
        enemy_spawn_rate = difficulty_manager.get_enemy_spawn_rate()
        orb_spawn_rate = difficulty_manager.get_orb_spawn_rate()
        
        # Increase speed based on game time and difficulty
        self.scroll_speed += speed_increase_rate * dt * 60
        self.enemy_speed += speed_increase_rate * dt * 60
        
        # Update road segments
        for segment in self.road_segments:
            segment['y'] += self.scroll_speed
            if segment['y'] > SCREEN_HEIGHT:
                segment['y'] = min([s['y'] for s in self.road_segments]) - 100
        
        # Update stripes
        for stripe in self.stripes:
            stripe['y'] += self.scroll_speed
            if stripe['y'] > SCREEN_HEIGHT:
                stripe['y'] = min([s['y'] for s in self.stripes]) - 70
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.enemy_speed)
            
            # Check for collision with player
            if enemy.rect.colliderect(self.player.rect):
                self.game_over = True
                sound_manager.play_sound("crash")
        
        # Remove enemies that are off screen
        self.enemies = [e for e in self.enemies if e.y < SCREEN_HEIGHT + 100]
        
        # Update orbs
        for orb in self.orbs:
            orb.update(self.scroll_speed)
            
            # Check for collision with player
            if not orb.collected and orb.rect.colliderect(self.player.rect):
                orb.collected = True
                self.score += 100
                sound_manager.play_sound("pickup")
        
        # Remove orbs that are collected or off screen
        self.orbs = [o for o in self.orbs if not o.collected and o.y < SCREEN_HEIGHT + 100]
        
        # Spawn new enemies based on difficulty
        if random.random() < enemy_spawn_rate * dt * 60:
            lane = random.randint(0, LANE_COUNT-1)
            road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
            x = road_left + lane * LANE_WIDTH + (LANE_WIDTH - 40) // 2
            color = random.choice(theme_manager.get_colors()["enemy"])
            self.enemies.append(Car(x, -100, color))
        
        # Spawn new orbs based on difficulty
        if random.random() < orb_spawn_rate * dt * 60:
            road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
            x = road_left + random.randint(30, ROAD_WIDTH - 30)
            self.orbs.append(Orb(x, -30))
        
        # Update high score
        self.high_score = max(self.high_score, self.score)
        
        # Increase score based on time"""
    
    content = re.sub(update_pattern, update_replacement, content, flags=re.DOTALL)
    
    # Update the settings menu integration
    settings_pattern = r"elif self.state == STATE_SETTINGS:(.*?)new_state = self.settings_menu.handle_events\(events\)"
    settings_replacement = r"""elif self.state == STATE_SETTINGS:
            # Apply settings from settings menu
            if hasattr(self, 'settings_menu'):
                # Update difficulty
                difficulty_manager.set_difficulty(self.settings_menu.current_difficulty)
                
                # Update theme
                theme_manager.set_theme(self.settings_menu.current_theme)
                
            new_state = self.settings_menu.handle_events(events)"""
    
    content = re.sub(settings_pattern, settings_replacement, content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    with open('game_class.py', 'w') as f:
        f.write(content)
    
    print("Updated game_class.py with new features")

def update_settings_menu():
    """Update the settings_menu.py file to integrate with managers"""
    
    # Read the current file
    with open('settings_menu.py', 'r') as f:
        content = f.read()
    
    # Update imports to include managers
    if "from difficulty_manager import difficulty_manager" not in content:
        import_pattern = r"from sound_manager import sound_manager"
        replacement = "from sound_manager import sound_manager\nfrom difficulty_manager import difficulty_manager\nfrom theme_manager import theme_manager"
        content = re.sub(import_pattern, replacement, content)
    
    # Update the handle_events method to use managers
    handle_events_pattern = r"def handle_events\(self, events\):(.*?)return STATE_SETTINGS"
    handle_events_replacement = r"""def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # Make sure to stop any game sounds when returning to menu
                    sound_manager.stop_all_sounds()
                    return STATE_MAIN_MENU
        
        # Update all buttons
        for button in self.buttons.values():
            button.update(mouse_pos)
        
        # Check for button clicks
        if mouse_clicked:
            if self.buttons["theme"].is_clicked(mouse_pos, mouse_clicked):
                self.current_theme = (self.current_theme + 1) % len(self.themes)
                theme_manager.set_theme(self.current_theme)
                sound_manager.play_sound("click")
            elif self.buttons["theme_prev"].is_clicked(mouse_pos, mouse_clicked):
                self.current_theme = (self.current_theme - 1) % len(self.themes)
                theme_manager.set_theme(self.current_theme)
                sound_manager.play_sound("click")
            elif self.buttons["difficulty"].is_clicked(mouse_pos, mouse_clicked):
                self.current_difficulty = (self.current_difficulty + 1) % len(self.difficulties)
                difficulty_manager.set_difficulty(self.current_difficulty)
                sound_manager.play_sound("click")
            elif self.buttons["difficulty_prev"].is_clicked(mouse_pos, mouse_clicked):
                self.current_difficulty = (self.current_difficulty - 1) % len(self.difficulties)
                difficulty_manager.set_difficulty(self.current_difficulty)
                sound_manager.play_sound("click")
            elif self.buttons["music"].is_clicked(mouse_pos, mouse_clicked):
                self.music_on = sound_manager.toggle_music()
                sound_manager.play_sound("click")
            elif self.buttons["sound"].is_clicked(mouse_pos, mouse_clicked):
                self.sound_on = sound_manager.toggle_sound()
                if self.sound_on:
                    sound_manager.play_sound("click")
            elif self.buttons["back"].is_clicked(mouse_pos, mouse_clicked):
                # Make sure to stop any game sounds when returning to menu
                sound_manager.stop_all_sounds()
                sound_manager.play_sound("click")
                return STATE_MAIN_MENU
        
        return STATE_SETTINGS"""
    
    content = re.sub(handle_events_pattern, handle_events_replacement, content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    with open('settings_menu.py', 'w') as f:
        f.write(content)
    
    print("Updated settings_menu.py with manager integration")

def main():
    """Main function to update all game files"""
    try:
        update_game_class()
        update_settings_menu()
        print("All updates completed successfully!")
        print("The game now has:")
        print("- Progressive speed increases based on difficulty")
        print("- Proper difficulty levels (Easy, Medium, Hard)")
        print("- Theme selection with visual changes")
        print("- Improved background music handling")
    except Exception as e:
        print(f"Error updating game: {e}")

if __name__ == "__main__":
    main()