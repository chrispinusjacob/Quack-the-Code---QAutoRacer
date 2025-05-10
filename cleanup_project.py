import os
import shutil
import glob

print("Cleaning up and organizing QAutoGame project files...")

# Create a directory for temporary files
if not os.path.exists("temp_files"):
    os.makedirs("temp_files")
    print("Created temp_files directory for non-essential files")

# List of essential files to keep in the main directory
essential_files = [
    "button.py",
    "difficulty_manager.py",
    "difficulty_settings.py",
    "difficulty_settings.json",
    "game_hud.py",
    "game_manager.py",
    "game_objects.py",
    "high_scores.py",
    "high_scores.json",
    "improved_game.py",
    "instructions.py",
    "main_menu.py",
    "QAutoGame.py",
    "README.md",
    "requirements.txt",
    "run_final_game.bat",
    "settings.py",
    "settings_manager.py",
    "sound_manager.py"
]

# Move non-essential files to temp_files directory
print("\nMoving non-essential files to temp_files directory...")
for file in glob.glob("*.py"):
    if file not in essential_files and not file == "cleanup_project.py":
        try:
            shutil.move(file, os.path.join("temp_files", file))
            print(f"Moved {file} to temp_files directory")
        except Exception as e:
            print(f"Error moving {file}: {e}")

# Move non-essential batch files to temp_files directory
for file in glob.glob("*.bat"):
    if file != "run_final_game.bat":
        try:
            shutil.move(file, os.path.join("temp_files", file))
            print(f"Moved {file} to temp_files directory")
        except Exception as e:
            print(f"Error moving {file}: {e}")

# Create a production-ready README.md file
readme_content = """# QAutoGame

A retro-style racing game developed with Python and Pygame.

## Copyright
Copyright 2025 by Chrispinus Jacob  
Powered by Amazon Q

## Game Description
QAutoGame is a retro-style racing game where you control a car and navigate through traffic while collecting orbs to increase your score. The game features multiple difficulty levels, customizable settings, and a high score system.

## Features
- Three difficulty levels: Easy, Medium, and Hard
- Customizable sound and music settings
- High score tracking
- Retro-style graphics and sound effects

## Controls
- LEFT ARROW / A: Move car left
- RIGHT ARROW / D: Move car right
- P or ESC: Pause game
- SPACE: Restart (when game over)
- Arrow keys: Navigate menus
- Enter: Select menu option

## Requirements
- Python 3.6+
- Pygame 2.0+

## Installation
1. Ensure Python is installed on your system
2. Install required packages: `pip install -r requirements.txt`
3. Run the game: `python game_manager.py` or double-click `run_final_game.bat`

## Files
- `game_manager.py`: Main entry point for the game
- `main_menu.py`: Main menu interface
- `improved_game.py`: Core game logic
- `settings.py`: Settings menu and configuration
- `high_scores.py`: High score tracking and display
- `instructions.py`: Game instructions screen
- `difficulty_settings.py`: Difficulty level configuration
- `sound_manager.py`: Audio management
"""

with open("README.md", "w") as f:
    f.write(readme_content)
print("\nCreated production-ready README.md file")

# Create a requirements.txt file if it doesn't exist
if not os.path.exists("requirements.txt"):
    with open("requirements.txt", "w") as f:
        f.write("pygame>=2.0.0\n")
    print("Created requirements.txt file")

print("\nCleanup complete! Project is now organized for production.")
print("\nEssential files kept in the main directory:")
for file in essential_files:
    if os.path.exists(file):
        print(f"- {file}")

print("\nNext: Adding keyboard navigation to menus...")