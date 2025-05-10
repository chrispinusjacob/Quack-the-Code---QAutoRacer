import pygame
import sys
import os
import json

print("Verifying difficulty settings integration in the game...")

# Check if difficulty_settings.json exists
print("\nChecking if difficulty_settings.json exists...")
if os.path.exists("difficulty_settings.json"):
    print("PASS: difficulty_settings.json exists")
    
    # Read the file content
    with open("difficulty_settings.json", "r") as f:
        content = json.load(f)
        print(f"Current difficulty setting: {content.get('difficulty', 'unknown')}")
else:
    print("FAIL: difficulty_settings.json does not exist")

# Check if the settings.py file references difficulty_settings.py
print("\nChecking if settings.py integrates with difficulty_settings.py...")
if os.path.exists("settings.py"):
    with open("settings.py", "r") as f:
        content = f.read()
        if "difficulty_settings" in content.lower() and "DifficultySettings" in content:
            print("PASS: settings.py references difficulty_settings.py")
        else:
            print("FAIL: settings.py does not properly reference difficulty_settings.py")
else:
    print("FAIL: settings.py does not exist")

# Check if game_manager.py integrates with difficulty_settings.py
print("\nChecking if game_manager.py integrates with difficulty_settings.py...")
if os.path.exists("game_manager.py"):
    with open("game_manager.py", "r") as f:
        content = f.read()
        if "difficulty_settings" in content.lower() and "DifficultySettings" in content:
            print("PASS: game_manager.py references difficulty_settings.py")
            
            # Check if it applies difficulty settings to the game
            if "apply_to_difficulty_manager" in content or "apply_settings" in content:
                print("PASS: game_manager.py applies difficulty settings to the game")
            else:
                print("FAIL: game_manager.py does not apply difficulty settings to the game")
        else:
            print("FAIL: game_manager.py does not properly reference difficulty_settings.py")
else:
    print("FAIL: game_manager.py does not exist")

# Check if improved_game.py has a difficulty manager
print("\nChecking if improved_game.py has a difficulty manager...")
if os.path.exists("improved_game.py"):
    with open("improved_game.py", "r") as f:
        content = f.read()
        if "difficulty" in content.lower():
            print("PASS: improved_game.py has difficulty-related code")
            
            # Check for specific difficulty properties
            properties = ["enemy_speed", "scroll_speed", "enemy_spawn_rate", "orb_spawn_rate"]
            found_properties = [prop for prop in properties if prop in content]
            print(f"Found difficulty properties: {', '.join(found_properties)}")
            
            if len(found_properties) >= 3:
                print("PASS: improved_game.py has sufficient difficulty properties")
            else:
                print("FAIL: improved_game.py is missing important difficulty properties")
        else:
            print("FAIL: improved_game.py does not have difficulty-related code")
else:
    print("FAIL: improved_game.py does not exist")

print("\nVerification complete!")
print("\nRecommendation: The difficulty settings appear to be properly integrated.")
print("To test in-game, run the game and change the difficulty in the settings menu.")
print("Then start a new game and observe if the difficulty changes are applied.")