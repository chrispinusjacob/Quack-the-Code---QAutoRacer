import pygame
import sys
import os

print("Fixing main menu title and removing overlapping text...")

with open("main_menu.py", "r") as f:
    content = f.read()

# Change the title from "QAutoGame '90" to "QAutoGame"
content = content.replace('title_text = "QAutoGame \'90"', 'title_text = "QAutoGame"')

# Remove the subtitle as it's overlapping with buttons
content = content.replace('subtitle_text = "THE ULTIMATE QAutoGame EXPERIENCE"', 'subtitle_text = ""')

# Remove the footer text as we already have copyright info
content = content.replace('footer_text = "© 2023 QAutoGame © 2025"', 'footer_text = ""')

# Adjust copyright position further up
content = content.replace('copyright_rect = copyright_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))', 
                         'copyright_rect = copyright_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))')
content = content.replace('powered_rect = powered_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))', 
                         'powered_rect = powered_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))')

with open("main_menu.py", "w") as f:
    f.write(content)

print("Main menu title has been fixed and overlapping text removed!")

# Also update the title in the game manager
with open("game_manager.py", "r") as f:
    content = f.read()

# Change the title from "QAutoGame '90" to "QAutoGame"
content = content.replace('TITLE = "QAutoGame \'90"', 'TITLE = "QAutoGame"')

with open("game_manager.py", "w") as f:
    f.write(content)

print("Game manager title has been updated!")