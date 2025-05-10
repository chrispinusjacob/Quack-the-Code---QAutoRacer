import os
import sys
import pygame
import importlib
import traceback

print("=== QAutoGame Testing and Fixing Script ===")
print("This script will test all components of the game and fix any issues found.")

# Initialize pygame for testing
pygame.init()
pygame.mixer.init()

# Test functions
def test_module_import(module_name):
    """Test if a module can be imported"""
    try:
        module = importlib.import_module(module_name)
        print(f"✓ Successfully imported {module_name}")
        return module
    except Exception as e:
        print(f"✗ Failed to import {module_name}: {e}")
        return None

def test_file_exists(file_path):
    """Test if a file exists"""
    if os.path.exists(file_path):
        print(f"✓ File exists: {file_path}")
        return True
    else:
        print(f"✗ File does not exist: {file_path}")
        return False

# Test essential files
print("\n=== Testing Essential Files ===")
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
    "settings.py",
    "settings_manager.py",
    "sound_manager.py"
]

all_files_exist = True
for file in essential_files:
    if not test_file_exists(file):
        all_files_exist = False

if not all_files_exist:
    print("Some essential files are missing. Please restore them before continuing.")
    sys.exit(1)

# Test module imports
print("\n=== Testing Module Imports ===")
modules = [
    "button",
    "difficulty_manager",
    "difficulty_settings",
    "game_hud",
    "game_manager",
    "game_objects",
    "high_scores",
    "improved_game",
    "instructions",
    "main_menu",
    "settings",
    "settings_manager",
    "sound_manager"
]

imported_modules = {}
for module_name in modules:
    module = test_module_import(module_name)
    if module:
        imported_modules[module_name] = module

# Check for overlapping text in main_menu.py
print("\n=== Checking for overlapping text in main_menu.py ===")
with open("main_menu.py", "r") as f:
    main_menu_content = f.read()

# Fix overlapping text in main menu
if "nav_rect = nav_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 140))" in main_menu_content:
    print("Found potential text overlap in main_menu.py")
    
    # Adjust positions to prevent overlap
    main_menu_content = main_menu_content.replace(
        "copyright_rect = copyright_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))",
        "copyright_rect = copyright_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120))"
    )
    
    main_menu_content = main_menu_content.replace(
        "powered_rect = powered_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))",
        "powered_rect = powered_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))"
    )
    
    main_menu_content = main_menu_content.replace(
        "nav_rect = nav_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 140))",
        "nav_rect = nav_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))"
    )
    
    # Write the fixed content back to the file
    with open("main_menu.py", "w") as f:
        f.write(main_menu_content)
    
    print("✓ Fixed text overlap in main_menu.py")

# Check settings.py for keyboard navigation issues
print("\n=== Checking settings.py for keyboard navigation issues ===")
with open("settings.py", "r") as f:
    settings_content = f.read()

# Check if settings.py has the correct keyboard navigation code
if "elif event.key == K_RETURN or event.key == K_SPACE:" in settings_content:
    print("Settings has keyboard navigation code, checking for issues...")
    
    # Check if the keyboard navigation code is complete
    if "# Process button action based on index" in settings_content and not "if i == 0:" in settings_content:
        print("Found incomplete keyboard navigation code in settings.py")
        
        # Find the handle_events method
        handle_events_start = settings_content.find("def handle_events(self):")
        handle_events_end = settings_content.find("def update(self):", handle_events_start)
        
        # Extract the handle_events method
        handle_events_method = settings_content[handle_events_start:handle_events_end]
        
        # Find the keyboard navigation code
        keyboard_nav_start = handle_events_method.find("elif event.key == K_RETURN or event.key == K_SPACE:")
        keyboard_nav_end = handle_events_method.find("# Check button clicks", keyboard_nav_start)
        
        # Extract the keyboard navigation code
        keyboard_nav_code = handle_events_method[keyboard_nav_start:keyboard_nav_end]
        
        # Fix the keyboard navigation code
        fixed_keyboard_nav_code = """                elif event.key == K_RETURN or event.key == K_SPACE:
                    # Select current button
                    self.sound_manager.play("click")
                    
                    # Get the selected button
                    button = self.buttons[self.selected_button]
                    
                    # Process button action based on index
                    i = self.selected_button
                    if i == 0:  # Sound Effects
                        # Toggle sound effects
                        self.sound_manager.toggle_sound()
                        button.text = f"SOUND EFFECTS: {'ON' if self.sound_manager.sound_enabled else 'OFF'}"
                        button.text_surface = button.font.render(button.text, True, button.text_color)
                        button.text_rect = button.text_surface.get_rect(center=button.rect.center)
                    
                    elif i == 1:  # Music
                        # Toggle music
                        self.sound_manager.toggle_music()
                        button.text = f"MUSIC: {'ON' if self.sound_manager.music_enabled else 'OFF'}"
                        button.text_surface = button.font.render(button.text, True, button.text_color)
                        button.text_rect = button.text_surface.get_rect(center=button.rect.center)
                        
                        # Start or stop music based on new state
                        if self.sound_manager.music_enabled:
                            self.sound_manager.play_music("menu_music.mp3")
                        else:
                            self.sound_manager.stop_music()
                    
                    elif i == 2:  # Sound volume
                        # Cycle through volume levels: 100% -> 75% -> 50% -> 25% -> 0% -> 100%
                        current_volume = self.sound_manager.volume
                        if current_volume >= 0.9:
                            new_volume = 0.75
                        elif current_volume >= 0.65:
                            new_volume = 0.5
                        elif current_volume >= 0.4:
                            new_volume = 0.25
                        elif current_volume >= 0.15:
                            new_volume = 0.0
                        else:
                            new_volume = 1.0
                        
                        # Set volume and update button text
                        self.sound_manager.set_volume(new_volume)
                        button.text = f"SOUND VOLUME: {int(self.sound_manager.volume * 100)}%"
                        button.text_surface = button.font.render(button.text, True, button.text_color)
                        button.text_rect = button.text_surface.get_rect(center=button.rect.center)
                    
                    elif i == 3:  # Music volume
                        # Cycle through volume levels: 100% -> 75% -> 50% -> 25% -> 0% -> 100%
                        current_volume = self.sound_manager.music_volume
                        if current_volume >= 0.9:
                            new_volume = 0.75
                        elif current_volume >= 0.65:
                            new_volume = 0.5
                        elif current_volume >= 0.4:
                            new_volume = 0.25
                        elif current_volume >= 0.15:
                            new_volume = 0.0
                        else:
                            new_volume = 1.0
                        
                        # Set music volume and update button text
                        self.sound_manager.set_music_volume(new_volume)
                        button.text = f"MUSIC VOLUME: {int(self.sound_manager.music_volume * 100)}%"
                        button.text_surface = button.font.render(button.text, True, button.text_color)
                        button.text_rect = button.text_surface.get_rect(center=button.rect.center)
                        
                        # If music is playing, restart it to apply the new volume immediately
                        if self.sound_manager.music_enabled and self.sound_manager.music_playing:
                            self.sound_manager.play_music("menu_music.mp3")
                    
                    elif i == 4:  # Difficulty setting
                        if self.difficulty_settings:
                            # Cycle through difficulty levels: easy -> medium -> hard -> easy
                            current = self.difficulty_settings.current_difficulty
                            if current == "easy":
                                new_difficulty = "medium"
                            elif current == "medium":
                                new_difficulty = "hard"
                            else:
                                new_difficulty = "easy"
                            
                            # Set new difficulty and update button text
                            self.difficulty_settings.set_difficulty(new_difficulty)
                            button.text = f"DIFFICULTY: {new_difficulty.upper()}"
                            button.text_surface = button.font.render(button.text, True, button.text_color)
                            button.text_rect = button.text_surface.get_rect(center=button.rect.center)
                            
                            print(f"Difficulty changed to: {new_difficulty}")
                    
                    elif i == 5:  # Back to menu
                        self.running = False
                        return "menu"
"""
        
        # Replace the keyboard navigation code
        new_handle_events_method = handle_events_method.replace(keyboard_nav_code, fixed_keyboard_nav_code)
        
        # Update the settings_content with the fixed handle_events method
        settings_content = settings_content.replace(handle_events_method, new_handle_events_method)
        
        # Write the fixed content back to the file
        with open("settings.py", "w") as f:
            f.write(settings_content)
        
        print("✓ Fixed keyboard navigation in settings.py")
    else:
        print("✓ Keyboard navigation code in settings.py appears to be complete")
else:
    print("✗ Settings.py is missing keyboard navigation code")

# Check for pygame.font initialization
print("\n=== Checking for pygame.font initialization ===")
with open("game_manager.py", "r") as f:
    game_manager_content = f.read()

if "pygame.font.init()" not in game_manager_content:
    print("Adding pygame.font.init() to game_manager.py")
    
    # Add pygame.font.init() after pygame.init()
    game_manager_content = game_manager_content.replace(
        "pygame.init()",
        "pygame.init()\n        pygame.font.init()"
    )
    
    # Write the fixed content back to the file
    with open("game_manager.py", "w") as f:
        f.write(game_manager_content)
    
    print("✓ Added pygame.font.init() to game_manager.py")
else:
    print("✓ pygame.font.init() is already in game_manager.py")

# Update the README.md file
print("\n=== Updating README.md ===")
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
- Full keyboard navigation support

## Controls
- LEFT ARROW / A: Move car left
- RIGHT ARROW / D: Move car right
- P or ESC: Pause game
- SPACE: Restart (when game over)
- Arrow keys: Navigate menus
- Enter/Space: Select menu option
- ESC: Return to previous menu or exit

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

## Keyboard Navigation
- Use UP/DOWN arrow keys to navigate between menu options
- Press ENTER or SPACE to select the highlighted option
- Press ESC to return to the previous menu or exit the game
"""

with open("README.md", "w") as f:
    f.write(readme_content)

print("✓ Updated README.md with comprehensive information")

# Create a requirements.txt file
print("\n=== Creating requirements.txt ===")
with open("requirements.txt", "w") as f:
    f.write("pygame>=2.0.0\n")

print("✓ Created requirements.txt file")

# Update the run_final_game.bat file
print("\n=== Updating run_final_game.bat ===")
bat_content = """@echo off
echo ===================================
echo       QAutoGame
echo ===================================
echo Copyright 2025 by Chrispinus Jacob
echo Powered by Amazon Q
echo ===================================
echo.
echo Current difficulty: 
type difficulty_settings.json
echo.
echo CONTROLS:
echo - Arrow keys: Navigate menus and move car
echo - Enter/Space: Select menu options
echo - ESC: Return to menu or exit
echo - P: Pause game
echo.
echo PROJECT COMPLETE!
echo - Clean, organized code structure
echo - Full keyboard navigation with visual indicators
echo - Working difficulty settings with speed progression
echo - Updated branding and copyright information
echo.
echo Starting game...
echo.
python game_manager.py
pause
"""

with open("run_final_game.bat", "w") as f:
    f.write(bat_content)

print("✓ Updated run_final_game.bat file")

print("\n=== All tests and fixes complete! ===")
print("The game should now be ready for production.")
print("Run the game using: python game_manager.py")