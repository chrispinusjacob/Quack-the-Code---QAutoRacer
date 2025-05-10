import pygame
import sys
import os

print("Adjusting button positions in settings screen...")

with open("settings.py", "r") as f:
    content = f.read()

# Move buttons up by adjusting their Y positions
content = content.replace('Button(button_x, 120, button_width, button_height,', 'Button(button_x, 100, button_width, button_height,')
content = content.replace('Button(button_x, 190, button_width, button_height,', 'Button(button_x, 170, button_width, button_height,')
content = content.replace('Button(button_x, 260, button_width, button_height,', 'Button(button_x, 240, button_width, button_height,')
content = content.replace('Button(button_x, 330, button_width, button_height,', 'Button(button_x, 310, button_width, button_height,')
content = content.replace('Button(button_x, 400, button_width, button_height,', 'Button(button_x, 380, button_width, button_height,')
content = content.replace('Button(button_x, 490, button_width, button_height,', 'Button(button_x, 450, button_width, button_height,')

with open("settings.py", "w") as f:
    f.write(content)

print("Settings button positions have been adjusted!")