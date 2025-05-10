import pygame
import sys
import os

print("Fixing overlapping text in main menu...")

# Fix main menu buttons - move them up even more
with open("main_menu.py", "r") as f:
    content = f.read()

# Move buttons up by adjusting their Y positions
content = content.replace('Button(button_x, 180, button_width, button_height,', 'Button(button_x, 150, button_width, button_height,')
content = content.replace('Button(button_x, 250, button_width, button_height,', 'Button(button_x, 220, button_width, button_height,')
content = content.replace('Button(button_x, 320, button_width, button_height,', 'Button(button_x, 290, button_width, button_height,')
content = content.replace('Button(button_x, 390, button_width, button_height,', 'Button(button_x, 360, button_width, button_height,')
content = content.replace('Button(button_x, 460, button_width, button_height,', 'Button(button_x, 430, button_width, button_height,')

# Adjust copyright position
if "copyright_rect = copyright_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))" in content:
    content = content.replace(
        "copyright_rect = copyright_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))",
        "copyright_rect = copyright_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))"
    )
    
if "powered_rect = powered_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))" in content:
    content = content.replace(
        "powered_rect = powered_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))",
        "powered_rect = powered_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))"
    )

with open("main_menu.py", "w") as f:
    f.write(content)

print("Main menu button positions have been adjusted!")

# Fix settings screen buttons - move them up even more
with open("settings.py", "r") as f:
    content = f.read()

# Move buttons up by adjusting their Y positions
content = content.replace('Button(button_x, 100, button_width, button_height,', 'Button(button_x, 80, button_width, button_height,')
content = content.replace('Button(button_x, 170, button_width, button_height,', 'Button(button_x, 150, button_width, button_height,')
content = content.replace('Button(button_x, 240, button_width, button_height,', 'Button(button_x, 220, button_width, button_height,')
content = content.replace('Button(button_x, 310, button_width, button_height,', 'Button(button_x, 290, button_width, button_height,')
content = content.replace('Button(button_x, 380, button_width, button_height,', 'Button(button_x, 360, button_width, button_height,')
content = content.replace('Button(button_x, 450, button_width, button_height,', 'Button(button_x, 430, button_width, button_height,')

with open("settings.py", "w") as f:
    f.write(content)

print("Settings button positions have been adjusted!")

# Fix high scores screen buttons - move them up even more
with open("high_scores.py", "r") as f:
    content = f.read()

# Move buttons up by adjusting their Y positions
content = content.replace('SCREEN_HEIGHT - 100,', 'SCREEN_HEIGHT - 120,')
content = content.replace('SCREEN_HEIGHT - 170,', 'SCREEN_HEIGHT - 190,')

with open("high_scores.py", "w") as f:
    f.write(content)

print("High scores button positions have been adjusted!")

# Fix instructions screen button - move it up even more
with open("instructions.py", "r") as f:
    content = f.read()

# Move button up by adjusting its Y position
content = content.replace('SCREEN_HEIGHT - 100,', 'SCREEN_HEIGHT - 120,')

with open("instructions.py", "w") as f:
    f.write(content)

print("Instructions button position has been adjusted!")

print("All overlapping text issues have been fixed!")