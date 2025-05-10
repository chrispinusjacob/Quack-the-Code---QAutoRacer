import pygame
import sys
import os

print("Updating all titles and copyright information...")

# List of files to check
files_to_check = [
    "main_menu.py",
    "settings.py",
    "high_scores.py",
    "instructions.py",
    "improved_game.py",
    "game_manager.py",
    "game_hud.py"
]

# Update each file
for filename in files_to_check:
    if os.path.exists(filename):
        print(f"Checking {filename}...")
        
        with open(filename, "r") as f:
            content = f.read()
        
        # Replace any remaining instances of "QAutoGame '90" with "QAutoGame"
        content = content.replace("QAutoGame '90", "QAutoGame")
        content = content.replace("QAutoGame '90", "QAutoGame")
        
        # Update copyright year if needed
        content = content.replace("© 2023", "© 2025")
        
        # Update window title
        content = content.replace('pygame.display.set_caption("QAutoGame \'90")', 'pygame.display.set_caption("QAutoGame")')
        
        with open(filename, "w") as f:
            f.write(content)
        
        print(f"Updated {filename}")

print("All titles and copyright information have been updated!")