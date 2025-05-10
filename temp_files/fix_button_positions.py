import pygame
import sys
import os

print("Adjusting button positions in main menu...")

with open("main_menu.py", "r") as f:
    content = f.read()

# Move buttons up by adjusting their Y positions
content = content.replace('Button(button_x, 250, button_width, button_height,', 'Button(button_x, 180, button_width, button_height,')
content = content.replace('Button(button_x, 330, button_width, button_height,', 'Button(button_x, 250, button_width, button_height,')
content = content.replace('Button(button_x, 410, button_width, button_height,', 'Button(button_x, 320, button_width, button_height,')
content = content.replace('Button(button_x, 490, button_width, button_height,', 'Button(button_x, 390, button_width, button_height,')
content = content.replace('Button(button_x, 570, button_width, button_height,', 'Button(button_x, 460, button_width, button_height,')

with open("main_menu.py", "w") as f:
    f.write(content)

print("Button positions have been adjusted!")

# Also update the copyright position to avoid overlap with buttons
if "Copyright 2025 by Chrispinus Jacob" in content:
    print("Adjusting copyright position...")
    
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "copyright_rect = copyright_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))" in line:
            lines[i] = "        copyright_rect = copyright_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))"
        if "powered_rect = powered_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))" in line:
            lines[i] = "        powered_rect = powered_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))"
    
    with open("main_menu.py", "w") as f:
        f.write("\n".join(lines))
    
    print("Copyright position has been adjusted!")