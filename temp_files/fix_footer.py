import pygame
import sys
import os

print("Removing retro footer and updating copyright information...")

with open("main_menu.py", "r") as f:
    content = f.read()

# Remove the retro footer and replace with QAutoGame copyright
content = content.replace('footer_text = "© 2023 QAutoGame © 2025"', 'footer_text = "QAutoGame © 2025"')

with open("main_menu.py", "w") as f:
    f.write(content)

print("Footer has been updated!")

# Also check and update any other screens that might have the footer
for filename in ["settings.py", "high_scores.py", "instructions.py", "improved_game.py"]:
    if os.path.exists(filename):
        print(f"Checking {filename} for footer text...")
        
        with open(filename, "r") as f:
            content = f.read()
        
        if "QAutoGame © 2025" in content:
            content = content.replace('footer_text = "© 2023 QAutoGame © 2025"', 'footer_text = "QAutoGame © 2025"')
            
            with open(filename, "w") as f:
                f.write(content)
            
            print(f"Updated footer in {filename}")

print("All footers have been updated!")