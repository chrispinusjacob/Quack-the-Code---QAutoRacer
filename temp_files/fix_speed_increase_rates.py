import json
import os

print("Fixing difficulty speed increase rates...")

# First, check the difficulty settings in difficulty_settings.py
with open("difficulty_settings.py", "r") as f:
    difficulty_settings_content = f.read()

# Check if the difficulty presets have proper speed increase rates
if "speed_increase_rate" in difficulty_settings_content:
    print("Updating speed increase rates for each difficulty level...")
    
    # Modify the difficulty settings to have more appropriate speed increase rates
    
    # Find and replace the easy difficulty settings
    if "\"easy\": {" in difficulty_settings_content:
        print("Updating EASY difficulty speed increase rate...")
        
        # Make easy mode increase speed very slowly
        difficulty_settings_content = difficulty_settings_content.replace(
            "\"speed_increase_rate\": 0.00003,",
            "\"speed_increase_rate\": 0.00001,"
        )
        difficulty_settings_content = difficulty_settings_content.replace(
            "\"spawn_rate_increase\": 0.00002,",
            "\"spawn_rate_increase\": 0.000005,"
        )
        
        print("EASY difficulty updated with slower speed increase rate")
    
    # Find and replace the medium difficulty settings
    if "\"medium\": {" in difficulty_settings_content:
        print("Updating MEDIUM difficulty speed increase rate...")
        
        # Keep medium mode with moderate speed increase
        difficulty_settings_content = difficulty_settings_content.replace(
            "\"speed_increase_rate\": 0.0001,",
            "\"speed_increase_rate\": 0.00005,"
        )
        difficulty_settings_content = difficulty_settings_content.replace(
            "\"spawn_rate_increase\": 0.00005,",
            "\"spawn_rate_increase\": 0.00002,"
        )
        
        print("MEDIUM difficulty updated with moderate speed increase rate")
    
    # Find and replace the hard difficulty settings
    if "\"hard\": {" in difficulty_settings_content:
        print("Updating HARD difficulty speed increase rate...")
        
        # Make hard mode increase speed much faster
        difficulty_settings_content = difficulty_settings_content.replace(
            "\"speed_increase_rate\": 0.0002,",
            "\"speed_increase_rate\": 0.0003,"
        )
        difficulty_settings_content = difficulty_settings_content.replace(
            "\"spawn_rate_increase\": 0.0001,",
            "\"spawn_rate_increase\": 0.0002,"
        )
        
        print("HARD difficulty updated with faster speed increase rate")
    
    # Write the updated content back to the file
    with open("difficulty_settings.py", "w") as f:
        f.write(difficulty_settings_content)
    
    print("Speed increase rates updated for all difficulty levels")

# Create a test file to verify the updated difficulty settings
print("\nCreating a test file to verify updated difficulty settings...")

test_content = """import json
import os
import math
from difficulty_settings import DifficultySettings

print("\\nDifficulty Speed Increase Test\\n" + "="*30)

# Create a mock difficulty manager for testing
class MockDifficultyManager:
    def __init__(self):
        self.initial_enemy_speed = 0
        self.initial_scroll_speed = 0
        self.enemy_speed = 0
        self.scroll_speed = 0
        self.enemy_spawn_rate = 0
        self.orb_spawn_rate = 0
        self.speed_increase_rate = 0
        self.spawn_rate_increase = 0
        self.max_enemy_speed = 0
        self.max_scroll_speed = 0
        self.difficulty_level = ""
        self.game_time = 0
    
    def update(self, dt):
        \"\"\"Update difficulty based on elapsed time\"\"\"
        self.game_time += dt
        
        # Calculate difficulty factor (increases over time but with diminishing returns)
        difficulty_factor = 1.0 + math.log(1 + self.game_time / 60)
        
        # Update speeds with caps
        self.scroll_speed = min(
            self.max_scroll_speed,
            self.initial_scroll_speed + (self.speed_increase_rate * dt * 60 * difficulty_factor)
        )
        
        self.enemy_speed = min(
            self.max_enemy_speed,
            self.initial_enemy_speed + (self.speed_increase_rate * dt * 60 * difficulty_factor)
        )

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
    
    # Print the initial settings
    print(f"\\n{diff.upper()} Difficulty Settings:")
    print(f"  Initial Enemy Speed: {mock_manager.initial_enemy_speed}")
    print(f"  Initial Scroll Speed: {mock_manager.initial_scroll_speed}")
    print(f"  Speed Increase Rate: {mock_manager.speed_increase_rate}")
    print(f"  Spawn Rate Increase: {mock_manager.spawn_rate_increase}")
    
    # Simulate gameplay for 1, 2, and 5 minutes
    print("\\n  Speed progression over time:")
    
    # Set initial values
    mock_manager.enemy_speed = mock_manager.initial_enemy_speed
    mock_manager.scroll_speed = mock_manager.initial_scroll_speed
    
    # Simulate time passing
    for minutes in [1, 2, 5]:
        # Reset game time
        mock_manager.game_time = 0
        
        # Simulate gameplay for X minutes
        for _ in range(minutes * 60):  # X minutes * 60 seconds
            mock_manager.update(1.0)  # 1 second per update
        
        # Print the speeds after X minutes
        print(f"    After {minutes} minute(s):")
        print(f"      Enemy Speed: {mock_manager.enemy_speed:.2f}")
        print(f"      Scroll Speed: {mock_manager.scroll_speed:.2f}")

print("\\nTest complete! Run the game to verify the changes.")
"""

with open("verify_speed_increase.py", "w") as f:
    f.write(test_content)

print("Created verify_speed_increase.py to test updated difficulty settings")

# Reset to medium difficulty for testing
with open("difficulty_settings.json", "w") as f:
    json.dump({"difficulty": "medium"}, f)

print("\nReset difficulty to medium for testing")
print("\nSpeed increase rate fixes complete!")
print("Run verify_speed_increase.py to check the updated difficulty settings")
print("Then run the game to test the different difficulty levels")