import pygame
import sys
import os

print("Adjusting button positions in high scores screen...")

with open("high_scores.py", "r") as f:
    content = f.read()

# Move buttons up by adjusting their Y positions
content = content.replace('SCREEN_HEIGHT - 80,', 'SCREEN_HEIGHT - 100,')
content = content.replace('SCREEN_HEIGHT - 150,', 'SCREEN_HEIGHT - 170,')

with open("high_scores.py", "w") as f:
    f.write(content)

print("High scores button positions have been adjusted!")