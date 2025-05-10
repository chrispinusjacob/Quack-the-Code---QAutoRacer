import pygame
import sys
import os

print("Updating game manager title...")

with open("game_manager.py", "r") as f:
    content = f.read()

# Update the title in the game manager
content = content.replace('TITLE = "QAutoGame \'90"', 'TITLE = "QAutoGame"')
content = content.replace('pygame.display.set_caption(TITLE)', 'pygame.display.set_caption("QAutoGame")')

# Add missing constants if needed
if "PLAYER_SPEED" not in content:
    print("Adding missing constants...")
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "FPS = 60" in line:
            lines.insert(i+1, "PLAYER_SPEED = 5")
            lines.insert(i+2, "INITIAL_ENEMY_SPEED = 3")
            lines.insert(i+3, "INITIAL_SCROLL_SPEED = 5")
            break
    content = "\n".join(lines)

with open("game_manager.py", "w") as f:
    f.write(content)

print("Game manager has been updated!")