import json
import os
from difficulty_settings import DifficultySettings

print("Testing difficulty settings functionality...")

# Create a mock difficulty manager class for testing
class MockDifficultyManager:
    def __init__(self):
        self.initial_enemy_speed = 0
        self.initial_scroll_speed = 0
        self.initial_enemy_spawn_rate = 0
        self.initial_orb_spawn_rate = 0
        self.speed_increase_rate = 0
        self.spawn_rate_increase = 0
        self.max_enemy_speed = 0
        self.max_scroll_speed = 0
        self.max_enemy_spawn_rate = 0
        self.max_orb_spawn_rate = 0
        self.enemy_speed = 0
        self.scroll_speed = 0
        self.enemy_spawn_rate = 0
        self.orb_spawn_rate = 0
        self.difficulty_level = ""
        self.game_time = 0

# Test 1: Check if difficulty settings file exists
print("\nTest 1: Checking if difficulty_settings.json exists...")
if os.path.exists("difficulty_settings.json"):
    print("PASS: difficulty_settings.json exists")
    
    # Read the file content
    with open("difficulty_settings.json", "r") as f:
        content = f.read()
        print(f"Current content: {content}")
else:
    print("FAIL: difficulty_settings.json does not exist")
    print("Creating default difficulty_settings.json...")
    with open("difficulty_settings.json", "w") as f:
        json.dump({"difficulty": "medium"}, f)
    print("PASS: Created default difficulty_settings.json with medium difficulty")

# Test 2: Initialize DifficultySettings and check current difficulty
print("\nTest 2: Initializing DifficultySettings...")
difficulty_settings = DifficultySettings()
print(f"Current difficulty: {difficulty_settings.current_difficulty}")
print(f"Difficulty name: {difficulty_settings.get_difficulty_name()}")

# Test 3: Test changing difficulty
print("\nTest 3: Testing difficulty change functionality...")
difficulties = ["easy", "medium", "hard"]
for diff in difficulties:
    print(f"\nChanging difficulty to {diff}...")
    result = difficulty_settings.set_difficulty(diff)
    print(f"Change result: {result}")
    print(f"Current difficulty: {difficulty_settings.current_difficulty}")
    print(f"Difficulty name: {difficulty_settings.get_difficulty_name()}")
    
    # Check if the file was updated
    with open("difficulty_settings.json", "r") as f:
        content = json.load(f)
        print(f"File content: {content}")
        if content["difficulty"] == diff:
            print(f"PASS: File correctly updated to {diff}")
        else:
            print(f"FAIL: File not updated correctly. Expected {diff}, got {content['difficulty']}")

# Test 4: Test applying settings to difficulty manager
print("\nTest 4: Testing applying settings to difficulty manager...")
mock_manager = MockDifficultyManager()

# Try each difficulty level
for diff in difficulties:
    difficulty_settings.set_difficulty(diff)
    print(f"\nApplying {diff} difficulty settings...")
    settings = difficulty_settings.apply_to_difficulty_manager(mock_manager)
    
    # Check if settings were applied correctly
    print(f"Enemy speed: {mock_manager.enemy_speed}")
    print(f"Scroll speed: {mock_manager.scroll_speed}")
    print(f"Enemy spawn rate: {mock_manager.enemy_spawn_rate}")
    print(f"Orb spawn rate: {mock_manager.orb_spawn_rate}")
    print(f"Difficulty level: {mock_manager.difficulty_level}")
    
    # Verify settings match the expected values
    expected_settings = difficulty_settings.difficulty_presets[diff]
    if (mock_manager.enemy_speed == expected_settings["initial_enemy_speed"] and
        mock_manager.scroll_speed == expected_settings["initial_scroll_speed"] and
        mock_manager.difficulty_level == diff):
        print(f"PASS: {diff} settings applied correctly")
    else:
        print(f"FAIL: {diff} settings not applied correctly")

# Reset to medium difficulty for game
difficulty_settings.set_difficulty("medium")
print("\nReset to medium difficulty for game")

print("\nDifficulty settings test complete!")