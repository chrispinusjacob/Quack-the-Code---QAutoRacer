import json
import os
from difficulty_settings import DifficultySettings

print("\nDifficulty Settings Test\n" + "="*25)

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
    print(f"\n{diff.upper()} Difficulty Settings:")
    print(f"  Enemy Speed: {mock_manager.enemy_speed}")
    print(f"  Scroll Speed: {mock_manager.scroll_speed}")
    print(f"  Enemy Spawn Rate: {mock_manager.enemy_spawn_rate}")
    print(f"  Orb Spawn Rate: {mock_manager.orb_spawn_rate}")

print("\nTest complete! Run the game to verify the changes.")
