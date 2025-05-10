import pygame
import sys
import os

print("Updating main menu title...")

with open("main_menu.py", "r") as f:
    content = f.read()

# Update the title in the main menu
content = content.replace('TITLE = "QAutoGame \'90"', 'TITLE = "QAutoGame"')
content = content.replace('pygame.display.set_caption("QAutoGame \'90")', 'pygame.display.set_caption("QAutoGame")')

# Add copyright to the draw method
if "Copyright 2025 by Chrispinus Jacob" not in content:
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "def draw(self):" in line:
            # Find where to insert the copyright text
            for j in range(i+1, len(lines)):
                if "self.screen.blit(title_surface, title_rect)" in lines[j]:
                    # Add copyright text after the title
                    lines.insert(j+1, "        # Draw copyright text")
                    lines.insert(j+2, "        copyright_font = self.get_font(16)")
                    lines.insert(j+3, "        copyright_text = \"Copyright 2025 by Chrispinus Jacob\"")
                    lines.insert(j+4, "        copyright_surface = copyright_font.render(copyright_text, True, (150, 150, 150))")
                    lines.insert(j+5, "        copyright_rect = copyright_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))")
                    lines.insert(j+6, "        self.screen.blit(copyright_surface, copyright_rect)")
                    lines.insert(j+7, "        # Draw powered by text")
                    lines.insert(j+8, "        powered_text = \"Powered by Amazon Q\"")
                    lines.insert(j+9, "        powered_surface = copyright_font.render(powered_text, True, (150, 150, 150))")
                    lines.insert(j+10, "        powered_rect = powered_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))")
                    lines.insert(j+11, "        self.screen.blit(powered_surface, powered_rect)")
                    break
            break
    content = "\n".join(lines)

with open("main_menu.py", "w") as f:
    f.write(content)

print("Main menu has been updated!")