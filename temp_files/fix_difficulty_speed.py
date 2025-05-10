import json
import os

print("Fixing difficulty speed differences...")

# First, check the difficulty settings in difficulty_settings.py
with open("difficulty_settings.py", "r") as f:
    difficulty_settings_content = f.read()

# Check if the difficulty presets have proper speed differences
if "initial_enemy_speed" in difficulty_settings_content:
    print("Checking difficulty presets...")
    
    # Make sure there are clear differences between difficulty levels
    # Modify the difficulty settings to have more noticeable differences
    
    # Find and replace the easy difficulty settings
    if "\"easy\": {" in difficulty_settings_content:
        print("Updating EASY difficulty settings...")
        
        # Make easy mode significantly slower
        difficulty_settings_content = difficulty_settings_content.replace(
            "\"initial_enemy_speed\": 2.0,",
            "\"initial_enemy_speed\": 1.5,"
        )
        difficulty_settings_content = difficulty_settings_content.replace(
            "\"initial_scroll_speed\": 3.5,",
            "\"initial_scroll_speed\": 2.5,"
        )
        
        print("EASY difficulty updated with slower speeds")
    
    # Find and replace the hard difficulty settings
    if "\"hard\": {" in difficulty_settings_content:
        print("Updating HARD difficulty settings...")
        
        # Make hard mode significantly faster
        difficulty_settings_content = difficulty_settings_content.replace(
            "\"initial_enemy_speed\": 5.0,",
            "\"initial_enemy_speed\": 7.0,"
        )
        difficulty_settings_content = difficulty_settings_content.replace(
            "\"initial_scroll_speed\": 7.0,",
            "\"initial_scroll_speed\": 9.0,"
        )
        
        print("HARD difficulty updated with faster speeds")
    
    # Write the updated content back to the file
    with open("difficulty_settings.py", "w") as f:
        f.write(difficulty_settings_content)
    
    print("Difficulty presets updated with more noticeable speed differences")

# Now check if the difficulty is being properly applied in the game
with open("improved_game.py", "r") as f:
    improved_game_content = f.read()

# Make sure the difficulty is being reset when starting a new game
if "def reset(self):" in improved_game_content:
    print("Checking game reset method...")
    
    # Find the reset method
    lines = improved_game_content.split("\n")
    reset_method_found = False
    reset_method_start = 0
    
    for i, line in enumerate(lines):
        if "def reset(self):" in line:
            reset_method_found = True
            reset_method_start = i
            break
    
    if reset_method_found:
        # Check if the difficulty is being reset
        reset_method_end = len(lines)
        for i in range(reset_method_start, len(lines)):
            if "def " in lines[i] and i > reset_method_start + 1:
                reset_method_end = i
                break
        
        reset_method_content = "\n".join(lines[reset_method_start:reset_method_end])
        
        if "self.difficulty.reset()" in reset_method_content:
            print("Difficulty is being reset when starting a new game")
        else:
            print("Adding difficulty reset to the game reset method...")
            
            # Find where to insert the difficulty reset
            for i in range(reset_method_start, reset_method_end):
                if "self.game_time = 0" in lines[i]:
                    # Add difficulty reset after game time reset
                    lines.insert(i + 1, "        # Reset difficulty to initial values")
                    lines.insert(i + 2, "        self.difficulty.reset()")
                    print("Added difficulty reset to the game reset method")
                    break
            
            # Write the modified content back to the file
            with open("improved_game.py", "w") as f:
                f.write("\n".join(lines))

# Check if the difficulty settings are being reapplied when changing difficulty
with open("settings.py", "r") as f:
    settings_content = f.read()

if "self.difficulty_settings.set_difficulty(new_difficulty)" in settings_content:
    print("Difficulty settings are being updated when changing difficulty in settings")
else:
    print("WARNING: Difficulty settings might not be properly updated when changing difficulty")

# Create a test file to verify difficulty settings
print("\nCreating a test file to verify difficulty settings...")

test_content = """import json
import os
from difficulty_settings import DifficultySettings

print("\\nDifficulty Settings Test\\n" + "="*25)

# Create a mock difficulty manager for testing
class MockDifficultyManager:
    def __init__(self):
        self.enemy_speed = 0
        self.scroll_speed = 0
        self.enemy_spawn_rate = 0
        self.orb_spawn_rate = 0
        self.difficulty_level = ""

# Initialize difficulty settings
difficulty_settings = DifficultySettings()

# Test each difficulty level
difficulties = ["easy", "medium", "hard"]
for diff in difficulties:
    # Set the difficulty
    difficulty_settings.set_difficulty(diff)
    
    # Create a mock manager
    mock_manager = MockDifficultyManager()
    
    # Apply settings to the mock manager
    settings = difficulty_settings.apply_to_difficulty_manager(mock_manager)
    
    # Print the settings
    print(f"\\n{diff.upper()} Difficulty Settings:")
    print(f"  Enemy Speed: {mock_manager.enemy_speed}")
    print(f"  Scroll Speed: {mock_manager.scroll_speed}")
    print(f"  Enemy Spawn Rate: {mock_manager.enemy_spawn_rate}")
    print(f"  Orb Spawn Rate: {mock_manager.orb_spawn_rate}")

print("\\nTest complete! Run the game to verify the changes.")
"""

with open("verify_difficulty_speeds.py", "w") as f:
    f.write(test_content)

print("Created verify_difficulty_speeds.py to test difficulty settings")

# Reset to medium difficulty for testing
with open("difficulty_settings.json", "w") as f:
    json.dump({"difficulty": "medium"}, f)

print("\nReset difficulty to medium for testing")
print("\nDifficulty speed fixes complete!")
print("Run verify_difficulty_speeds.py to check the updated difficulty settings")
print("Then run the game to test the different difficulty levels")