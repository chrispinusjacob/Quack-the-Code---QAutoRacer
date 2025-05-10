import pygame
import sys
import os

print("Adjusting title size and position in main menu...")

with open("main_menu.py", "r") as f:
    content = f.read()

# Adjust title font size
content = content.replace('self.title_font = self.get_font(72)', 'self.title_font = self.get_font(60)')

# Adjust title position in draw method
lines = content.split("\n")
for i, line in enumerate(lines):
    if "title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))" in line:
        lines[i] = "        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))"
        break

content = "\n".join(lines)

with open("main_menu.py", "w") as f:
    f.write(content)

print("Title size and position have been adjusted!")

# Also adjust the title in other screens
for filename in ["settings.py", "high_scores.py", "instructions.py"]:
    print(f"Adjusting title position in {filename}...")
    
    with open(filename, "r") as f:
        content = f.read()
    
    # Adjust title position in draw method
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 60))" in line:
            lines[i] = "        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 40))"
        elif "title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 70))" in line:
            lines[i] = "        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 40))"
    
    content = "\n".join(lines)
    
    with open(filename, "w") as f:
        f.write(content)
    
    print(f"{filename} title position has been adjusted!")

print("All title positions have been adjusted!")