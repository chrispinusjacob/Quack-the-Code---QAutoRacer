import os

print("Fixing speed stuck at 0 issue...")

# First, check the difficulty_manager.py file
with open("difficulty_manager.py", "r") as f:
    difficulty_manager_content = f.read()

# Check if there's an issue with the update method
if "def update(self, dt):" in difficulty_manager_content:
    print("Checking difficulty manager update method...")
    
    # Make sure the speed is actually being updated
    if "self.enemy_speed = min(" in difficulty_manager_content and "self.scroll_speed = min(" in difficulty_manager_content:
        print("Speed update code exists, checking for issues...")
        
        # Check if the speed increase rate is too small
        if "self.speed_increase_rate * dt * 60" in difficulty_manager_content:
            print("Increasing the speed update multiplier...")
            
            # Increase the multiplier to make speed changes more noticeable
            difficulty_manager_content = difficulty_manager_content.replace(
                "self.speed_increase_rate * dt * 60",
                "self.speed_increase_rate * dt * 600"  # 10x increase
            )
            
            print("Speed update multiplier increased by 10x")
    
    # Write the updated content back to the file
    with open("difficulty_manager.py", "w") as f:
        f.write(difficulty_manager_content)

# Now check the difficulty_settings.py file
with open("difficulty_settings.py", "r") as f:
    difficulty_settings_content = f.read()

# Check if the speed increase rates are too small
if "speed_increase_rate" in difficulty_settings_content:
    print("\nChecking difficulty settings speed increase rates...")
    
    # Increase the speed increase rates for all difficulty levels
    
    # Easy difficulty
    if "\"easy\": {" in difficulty_settings_content:
        print("Updating EASY difficulty speed increase rate...")
        
        # Find the current speed increase rate
        import re
        easy_rate_match = re.search(r"\"speed_increase_rate\": ([\d\.e-]+),", difficulty_settings_content)
        if easy_rate_match:
            current_rate = float(easy_rate_match.group(1))
            new_rate = max(0.001, current_rate * 100)  # At least 0.001
            
            difficulty_settings_content = difficulty_settings_content.replace(
                f"\"speed_increase_rate\": {current_rate},",
                f"\"speed_increase_rate\": {new_rate},"
            )
            
            print(f"EASY speed increase rate updated from {current_rate} to {new_rate}")
    
    # Medium difficulty
    if "\"medium\": {" in difficulty_settings_content:
        print("Updating MEDIUM difficulty speed increase rate...")
        
        # Find the current speed increase rate
        import re
        medium_rate_match = re.search(r"\"medium\"[\s\S]*?\"speed_increase_rate\": ([\d\.e-]+),", difficulty_settings_content)
        if medium_rate_match:
            current_rate = float(medium_rate_match.group(1))
            new_rate = max(0.002, current_rate * 100)  # At least 0.002
            
            difficulty_settings_content = re.sub(
                r"(\"medium\"[\s\S]*?\"speed_increase_rate\": )([\d\.e-]+)(,)",
                f"\\1{new_rate}\\3",
                difficulty_settings_content
            )
            
            print(f"MEDIUM speed increase rate updated to approximately {new_rate}")
    
    # Hard difficulty
    if "\"hard\": {" in difficulty_settings_content:
        print("Updating HARD difficulty speed increase rate...")
        
        # Find the current speed increase rate
        import re
        hard_rate_match = re.search(r"\"hard\"[\s\S]*?\"speed_increase_rate\": ([\d\.e-]+),", difficulty_settings_content)
        if hard_rate_match:
            current_rate = float(hard_rate_match.group(1))
            new_rate = max(0.003, current_rate * 100)  # At least 0.003
            
            difficulty_settings_content = re.sub(
                r"(\"hard\"[\s\S]*?\"speed_increase_rate\": )([\d\.e-]+)(,)",
                f"\\1{new_rate}\\3",
                difficulty_settings_content
            )
            
            print(f"HARD speed increase rate updated to approximately {new_rate}")
    
    # Write the updated content back to the file
    with open("difficulty_settings.py", "w") as f:
        f.write(difficulty_settings_content)
    
    print("Speed increase rates updated for all difficulty levels")

# Create a direct fix for the improved_game.py file
print("\nChecking improved_game.py for speed issues...")

with open("improved_game.py", "r") as f:
    improved_game_content = f.read()

# Check if the game is using the difficulty values correctly
if "self.difficulty.enemy_speed" in improved_game_content and "self.difficulty.scroll_speed" in improved_game_content:
    print("Game is using difficulty speed values correctly")
else:
    print("Game might not be using difficulty speed values correctly, checking...")
    
    # Check for enemy speed usage
    if "enemy.y +=" in improved_game_content and "self.difficulty.enemy_speed" not in improved_game_content:
        print("Fixing enemy speed usage...")
        
        # Replace enemy speed usage
        improved_game_content = improved_game_content.replace(
            "enemy.y += enemy_speed",
            "enemy.y += self.difficulty.enemy_speed"
        )
        
        print("Enemy speed usage fixed")
    
    # Check for scroll speed usage
    if "segment['y'] +=" in improved_game_content and "self.difficulty.scroll_speed" not in improved_game_content:
        print("Fixing scroll speed usage...")
        
        # Replace scroll speed usage
        improved_game_content = improved_game_content.replace(
            "segment['y'] += scroll_speed",
            "segment['y'] += self.difficulty.scroll_speed"
        )
        
        print("Scroll speed usage fixed")
    
    # Write the updated content back to the file
    with open("improved_game.py", "w") as f:
        f.write(improved_game_content)

# Add a direct speed setting to the game's update method
print("\nAdding direct speed setting to the game's update method...")

with open("improved_game.py", "r") as f:
    improved_game_content = f.read()

# Find the update method
if "def update(self):" in improved_game_content:
    # Split the content into lines
    lines = improved_game_content.split("\n")
    update_method_found = False
    update_method_start = 0
    
    # Find the update method
    for i, line in enumerate(lines):
        if "def update(self):" in line:
            update_method_found = True
            update_method_start = i
            break
    
    if update_method_found:
        # Find where to insert the direct speed setting
        dt_line_found = False
        dt_line = 0
        
        # Look for dt calculation in the update method
        for i in range(update_method_start, len(lines)):
            if "dt = self.clock.get_time() / 1000.0" in lines[i]:
                dt_line_found = True
                dt_line = i
                break
        
        if dt_line_found:
            # Add direct speed setting after dt calculation
            direct_speed_code = [
                "        # Direct speed setting based on difficulty level",
                "        if hasattr(self.difficulty, 'difficulty_level'):",
                "            if self.difficulty.difficulty_level == \"easy\":",
                "                self.difficulty.enemy_speed = 1.5 + (self.game_time / 60.0) * 0.5  # Slow increase",
                "                self.difficulty.scroll_speed = 2.5 + (self.game_time / 60.0) * 0.5",
                "            elif self.difficulty.difficulty_level == \"medium\":",
                "                self.difficulty.enemy_speed = 3.0 + (self.game_time / 30.0) * 0.8  # Medium increase",
                "                self.difficulty.scroll_speed = 5.0 + (self.game_time / 30.0) * 0.8",
                "            elif self.difficulty.difficulty_level == \"hard\":",
                "                self.difficulty.enemy_speed = 7.0 + (self.game_time / 15.0) * 1.2  # Fast increase",
                "                self.difficulty.scroll_speed = 9.0 + (self.game_time / 15.0) * 1.2",
                "            # Cap speeds at maximum values",
                "            self.difficulty.enemy_speed = min(self.difficulty.enemy_speed, self.difficulty.max_enemy_speed)",
                "            self.difficulty.scroll_speed = min(self.difficulty.scroll_speed, self.difficulty.max_scroll_speed)"
            ]
            
            # Insert the direct speed setting code
            for j, code_line in enumerate(direct_speed_code):
                lines.insert(dt_line + j + 1, code_line)
            
            print("Direct speed setting added to the game's update method")
            
            # Write the modified content back to the file
            with open("improved_game.py", "w") as f:
                f.write("\n".join(lines))
        else:
            print("Could not find dt calculation in the update method")
    else:
        print("Could not find update method in the Game class")

print("\nSpeed stuck issue fixes complete!")
print("The game should now have noticeable speed differences between difficulty levels")
print("and the speed should increase over time.")
print("\nRun the game to test the changes.")