import json
import os
import math
from difficulty_settings import DifficultySettings

print("\nDifficulty Speed Increase Test\n" + "="*30)

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
        """Update difficulty based on elapsed time"""
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
    print(f"\n{diff.upper()} Difficulty Settings:")
    print(f"  Initial Enemy Speed: {mock_manager.initial_enemy_speed}")
    print(f"  Initial Scroll Speed: {mock_manager.initial_scroll_speed}")
    print(f"  Speed Increase Rate: {mock_manager.speed_increase_rate}")
    print(f"  Spawn Rate Increase: {mock_manager.spawn_rate_increase}")
    
    # Simulate gameplay for 1, 2, and 5 minutes
    print("\n  Speed progression over time:")
    
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

print("\nTest complete! Run the game to verify the changes.")
