import pygame
import sys
import os

print("Fixing instruction section layout to prevent overlapping...")

with open("instructions.py", "r") as f:
    content = f.read()

# Adjust the starting y_offset for instructions to be higher up
content = content.replace('y_offset = 130', 'y_offset = 100')

# Reduce the vertical spacing between instruction sections
content = content.replace('y_offset += 20', 'y_offset += 10')

# Reduce the vertical spacing between instruction lines
content = content.replace('y_offset += 30', 'y_offset += 25')

# Reduce the vertical spacing after section titles
content = content.replace('y_offset += 50', 'y_offset += 40')

# Move the controls diagram up and make it smaller
content = content.replace('car_width = 60', 'car_width = 50')
content = content.replace('car_height = 40', 'car_height = 30')

# Remove the controls diagram if it's causing overlap
if "def draw_controls_diagram" in content:
    lines = content.split("\n")
    new_lines = []
    skip_diagram = False
    for line in lines:
        if "self.draw_controls_diagram" in line:
            # Comment out the call to draw the diagram
            new_lines.append("        # Controls diagram removed to prevent overlap")
            new_lines.append("        # self.draw_controls_diagram(SCREEN_WIDTH // 2 - 150, y_offset)")
            continue
        elif "def draw_controls_diagram" in line:
            skip_diagram = True
            continue
        elif skip_diagram and "def run" in line:
            skip_diagram = False
        
        if not skip_diagram:
            new_lines.append(line)
    
    content = "\n".join(new_lines)

# Make the instructions content more compact
content = content.replace("""        self.instructions = [
            {
                "title": "CONTROLS",
                "content": [
                    "LEFT ARROW / A: Move car left",
                    "RIGHT ARROW / D: Move car right",
                    "P or ESC: Pause game",
                    "SPACE: Restart (when game over)"
                ]
            },
            {
                "title": "GAMEPLAY",
                "content": [
                    "Avoid crashing into other cars",
                    "Collect orbs to increase your score",
                    "Each orb is worth 1 point",
                    "Game speed increases over time"
                ]
            },
            {
                "title": "TIPS",
                "content": [
                    "Stay in open lanes to avoid traffic",
                    "Plan your movements ahead of time",
                    "Don't get greedy for orbs in dangerous spots",
                    "Watch for patterns in the traffic"
                ]
            }
        ]""", """        self.instructions = [
            {
                "title": "CONTROLS",
                "content": [
                    "LEFT/A: Move left | RIGHT/D: Move right",
                    "P or ESC: Pause | SPACE: Restart"
                ]
            },
            {
                "title": "GAMEPLAY",
                "content": [
                    "Avoid cars | Collect orbs for points",
                    "Speed increases over time"
                ]
            },
            {
                "title": "TIPS",
                "content": [
                    "Stay in open lanes | Plan ahead",
                    "Be careful with orbs in traffic"
                ]
            }
        ]""")

with open("instructions.py", "w") as f:
    f.write(content)

print("Instructions layout has been fixed to prevent overlapping!")