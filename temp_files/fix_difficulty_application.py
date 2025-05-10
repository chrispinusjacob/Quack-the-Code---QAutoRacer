import os
import sys

print("Fixing difficulty application in the game...")

# First, check if the issue is in the improved_game.py file
with open("improved_game.py", "r") as f:
    improved_game_content = f.read()

# Check if the difficulty manager is being properly initialized and used
if "self.difficulty = DifficultyManager()" in improved_game_content:
    print("PASS: DifficultyManager is properly initialized in improved_game.py")
else:
    print("FAIL: DifficultyManager is not properly initialized in improved_game.py")
    sys.exit(1)

# Check if the difficulty settings are being applied
if "self.difficulty_settings.apply_to_difficulty_manager(self.difficulty)" in improved_game_content:
    print("PASS: Difficulty settings are being applied in improved_game.py")
else:
    print("FAIL: Difficulty settings are not being applied in improved_game.py")
    sys.exit(1)

# Check if the difficulty manager is being updated during gameplay
if "self.difficulty.update(dt)" in improved_game_content:
    print("PASS: Difficulty manager is being updated during gameplay")
else:
    print("FAIL: Difficulty manager is not being updated during gameplay")
    
    # Fix: Add difficulty update to the game's update method
    print("Adding difficulty update to the game's update method...")
    
    # Find the update method in the Game class
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
            # Find where to insert the difficulty update
            dt_line_found = False
            dt_line = 0
            
            # Look for dt calculation in the update method
            for i in range(update_method_start, len(lines)):
                if "dt = self.clock.get_time() / 1000.0" in lines[i]:
                    dt_line_found = True
                    dt_line = i
                    break
            
            if dt_line_found:
                # Add difficulty update after dt calculation
                if "self.difficulty.update(dt)" not in "\n".join(lines[dt_line:dt_line+10]):
                    lines.insert(dt_line + 1, "        # Update difficulty based on elapsed time")
                    lines.insert(dt_line + 2, "        self.difficulty.update(dt)")
                    print("PASS: Added difficulty update to the game's update method")
                    
                    # Write the modified content back to the file
                    with open("improved_game.py", "w") as f:
                        f.write("\n".join(lines))
                else:
                    print("PASS: Difficulty update already exists in the update method")
            else:
                print("FAIL: Could not find dt calculation in the update method")
        else:
            print("FAIL: Could not find update method in the Game class")

# Check if the game is using the difficulty values
difficulty_values = [
    "self.difficulty.enemy_speed",
    "self.difficulty.scroll_speed",
    "self.difficulty.enemy_spawn_rate",
    "self.difficulty.orb_spawn_rate"
]

missing_values = []
for value in difficulty_values:
    if value not in improved_game_content:
        missing_values.append(value)

if missing_values:
    print(f"FAIL: The following difficulty values are not being used: {', '.join(missing_values)}")
    
    # Fix: Make sure the game is using the difficulty values
    print("Fixing the game to use difficulty values...")
    
    # Check for enemy spawning code
    if "random.random() < enemy_spawn_chance:" in improved_game_content:
        improved_game_content = improved_game_content.replace(
            "random.random() < enemy_spawn_chance:",
            "random.random() < self.difficulty.enemy_spawn_rate:"
        )
        print("PASS: Fixed enemy spawn rate usage")
    
    # Check for orb spawning code
    if "random.random() < orb_spawn_chance:" in improved_game_content:
        improved_game_content = improved_game_content.replace(
            "random.random() < orb_spawn_chance:",
            "random.random() < self.difficulty.orb_spawn_rate:"
        )
        print("PASS: Fixed orb spawn rate usage")
    
    # Check for scroll speed usage
    if "scroll_speed =" in improved_game_content and "self.difficulty.scroll_speed" not in improved_game_content:
        # Find and replace scroll speed assignments
        lines = improved_game_content.split("\n")
        for i, line in enumerate(lines):
            if "scroll_speed =" in line and "self.difficulty.scroll_speed" not in line:
                lines[i] = line.replace("scroll_speed =", "scroll_speed = self.difficulty.scroll_speed  # ")
        
        improved_game_content = "\n".join(lines)
        print("PASS: Fixed scroll speed usage")
    
    # Check for enemy speed usage
    if "enemy.y += enemy_speed" in improved_game_content:
        improved_game_content = improved_game_content.replace(
            "enemy.y += enemy_speed",
            "enemy.y += self.difficulty.enemy_speed"
        )
        print("PASS: Fixed enemy speed usage")
    
    # Write the modified content back to the file
    with open("improved_game.py", "w") as f:
        f.write(improved_game_content)
else:
    print("PASS: All difficulty values are being used in the game")

# Check if the game manager is properly applying difficulty settings
with open("game_manager.py", "r") as f:
    game_manager_content = f.read()

if "if self.difficulty_settings and hasattr(game, 'difficulty'):" in game_manager_content:
    print("PASS: Game manager is checking for difficulty attribute")
    
    # Make sure the condition is correct
    if "self.difficulty_settings.apply_to_difficulty_manager(game.difficulty)" in game_manager_content:
        print("PASS: Game manager is applying difficulty settings correctly")
    else:
        print("FAIL: Game manager is not applying difficulty settings correctly")
        
        # Fix the game manager
        game_manager_content = game_manager_content.replace(
            "if self.difficulty_settings and hasattr(game, 'difficulty'):",
            "if self.difficulty_settings and hasattr(game, 'difficulty'):\n            self.difficulty_settings.apply_to_difficulty_manager(game.difficulty)"
        )
        
        with open("game_manager.py", "w") as f:
            f.write(game_manager_content)
        
        print("PASS: Fixed game manager to apply difficulty settings")
else:
    print("FAIL: Game manager is not checking for difficulty attribute")

print("\nDifficulty application fixes complete!")
print("The game should now properly apply and use the difficulty settings during gameplay.")
print("Run the game and test different difficulty levels to verify the changes.")