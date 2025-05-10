import os

print("Fixing speed issues with direct approach...")

# First, check the difficulty_manager.py file
with open("difficulty_manager.py", "r") as f:
    difficulty_manager_content = f.read()

# Increase the speed update multiplier
if "self.speed_increase_rate * dt * 60" in difficulty_manager_content:
    print("Increasing the speed update multiplier...")
    
    # Increase the multiplier to make speed changes more noticeable
    difficulty_manager_content = difficulty_manager_content.replace(
        "self.speed_increase_rate * dt * 60",
        "self.speed_increase_rate * dt * 600"  # 10x increase
    )
    
    # Write the updated content back to the file
    with open("difficulty_manager.py", "w") as f:
        f.write(difficulty_manager_content)
    
    print("Speed update multiplier increased by 10x")

# Now directly modify the difficulty_settings.py file
with open("difficulty_settings.py", "r") as f:
    content = f.read()

# Replace the speed increase rates with much higher values
print("\nUpdating difficulty settings with higher speed increase rates...")

# Update easy difficulty
content = content.replace(
    "\"speed_increase_rate\": 0.00001,",
    "\"speed_increase_rate\": 0.001,"
)

# Update medium difficulty
content = content.replace(
    "\"speed_increase_rate\": 0.00005,",
    "\"speed_increase_rate\": 0.002,"
)

# Update hard difficulty
content = content.replace(
    "\"speed_increase_rate\": 0.0003,",
    "\"speed_increase_rate\": 0.004,"
)

# Write the updated content back to the file
with open("difficulty_settings.py", "w") as f:
    f.write(content)

print("Updated all difficulty speed increase rates")

# Add direct speed control to the improved_game.py file
print("\nAdding direct speed control to the game...")

with open("improved_game.py", "r") as f:
    game_content = f.read()

# Find the update method
if "def update(self):" in game_content:
    # Split the content into lines
    lines = game_content.split("\n")
    update_lines = []
    in_update_method = False
    update_method_start = 0
    
    # Find the update method
    for i, line in enumerate(lines):
        if "def update(self):" in line:
            in_update_method = True
            update_method_start = i
        elif in_update_method and line.strip().startswith("def "):
            in_update_method = False
        
        if in_update_method:
            update_lines.append(line)
    
    # Check if we need to add direct speed control
    if "self.difficulty.update(dt)" in "\n".join(update_lines):
        # Find where to insert the direct speed control
        for i, line in enumerate(lines):
            if "self.difficulty.update(dt)" in line:
                # Add direct speed control after difficulty update
                direct_speed_code = [
                    "",
                    "        # Direct speed control based on difficulty level",
                    "        if self.difficulty.difficulty_level == \"easy\":",
                    "            self.difficulty.enemy_speed = 1.5 + (self.game_time / 60.0) * 0.5  # Slow increase",
                    "            self.difficulty.scroll_speed = 2.5 + (self.game_time / 60.0) * 0.5",
                    "        elif self.difficulty.difficulty_level == \"medium\":",
                    "            self.difficulty.enemy_speed = 3.0 + (self.game_time / 30.0) * 0.8  # Medium increase",
                    "            self.difficulty.scroll_speed = 5.0 + (self.game_time / 30.0) * 0.8",
                    "        elif self.difficulty.difficulty_level == \"hard\":",
                    "            self.difficulty.enemy_speed = 7.0 + (self.game_time / 15.0) * 1.2  # Fast increase",
                    "            self.difficulty.scroll_speed = 9.0 + (self.game_time / 15.0) * 1.2",
                    "",
                    "        # Cap speeds at maximum values",
                    "        self.difficulty.enemy_speed = min(self.difficulty.enemy_speed, self.difficulty.max_enemy_speed)",
                    "        self.difficulty.scroll_speed = min(self.difficulty.scroll_speed, self.difficulty.max_scroll_speed)",
                ]
                
                # Insert the direct speed control code
                for j, code_line in enumerate(direct_speed_code):
                    lines.insert(i + j + 1, code_line)
                
                print("Direct speed control added after difficulty update")
                break
        
        # Write the modified content back to the file
        with open("improved_game.py", "w") as f:
            f.write("\n".join(lines))
    else:
        print("Could not find difficulty update in the update method")
else:
    print("Could not find update method in the Game class")

print("\nSpeed fixes complete!")
print("The game should now have noticeable speed differences between difficulty levels")
print("and the speed should increase over time.")
print("\nRun the game to test the changes.")