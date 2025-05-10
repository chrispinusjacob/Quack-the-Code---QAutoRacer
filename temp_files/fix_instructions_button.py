import pygame
import sys
import os

print("Adjusting button position in instructions screen...")

with open("instructions.py", "r") as f:
    content = f.read()

# Move button up by adjusting its Y position
content = content.replace('SCREEN_HEIGHT - 80,', 'SCREEN_HEIGHT - 100,')

with open("instructions.py", "w") as f:
    f.write(content)

print("Instructions button position has been adjusted!")