import pygame
import sys
import os

print("Fixing QAutoGame.py...")

with open("QAutoGame.py", "r") as f:
    content = f.read()

# Fix the title and copyright
content = content.replace('TITLE = "QAutoGame"\n# Copyright 2025 by Chrispinus Jacob\n# Powered by Amazon Q  # Changed from "QAutoGame \'90"', 
                         'TITLE = "QAutoGame"\n# Copyright 2025 by Chrispinus Jacob\n# Powered by Amazon Q')

# Add missing constants if needed
if "PLAYER_SPEED" not in content:
    print("Adding missing constants...")
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "Neon 80s color palette" in line:
            lines.insert(i-1, "# Game speeds")
            lines.insert(i, "PLAYER_SPEED = 5")
            lines.insert(i+1, "INITIAL_ENEMY_SPEED = 3")
            lines.insert(i+2, "INITIAL_SCROLL_SPEED = 5")
            lines.insert(i+3, "")
            break
    content = "\n".join(lines)

with open("QAutoGame.py", "w") as f:
    f.write(content)

print("QAutoGame.py has been updated!")