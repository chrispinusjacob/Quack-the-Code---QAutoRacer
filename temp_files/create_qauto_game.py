import os
import shutil

def combine_files():
    """Combine all necessary files into QAutoGame.py"""
    output_file = "QAutoGame.py"
    
    # List of files to combine in order
    files_to_combine = [
        "fixed_sound_manager.py",
        "button.py",
        "settings_manager.py",
        "difficulty_settings.py",
        "difficulty_manager.py",
        "game_objects.py",
        "game_hud.py",
        "main_menu.py",
        "high_scores.py",
        "instructions.py",
        "settings.py",
        "improved_game.py"
    ]
    
    # Start with the header
    header = """import pygame
import sys
import os
import math
import random
import json
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "QAutoGame '90"

# Neon 80s color palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (0, 191, 255)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (138, 43, 226)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)
NEON_CYAN = (0, 255, 255)

# Game settings
ROAD_WIDTH = 400
LANE_COUNT = 3
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")
FONT_DIR = os.path.join(ASSET_DIR, "fonts")
SPRITE_DIR = os.path.join(ASSET_DIR, "sprites")

# Create directories if they don't exist
os.makedirs(SOUND_DIR, exist_ok=True)
os.makedirs(FONT_DIR, exist_ok=True)
os.makedirs(SPRITE_DIR, exist_ok=True)

# Create pixel fonts
def get_font(size):
    try:
        return pygame.font.Font(os.path.join(FONT_DIR, "pixel.ttf"), size)
    except:
        return pygame.font.SysFont("Arial", size)
"""
    
    # Main function to run the game
    footer = """
#-------------------------------------------------------
# MAIN GAME MANAGER
#-------------------------------------------------------
class GameManager:
    def __init__(self):
        # Set up display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Initialize settings manager and apply settings
        self.settings_manager = SettingsManager()
        self.settings_manager.apply_settings_to_sound_manager(self.sound_manager)
        
        # Initialize difficulty settings
        self.difficulty_settings = DifficultySettings()
        
        # Game state
        self.running = True
        self.current_state = "menu"
        self.high_scores = self.load_high_scores()
    
    def load_high_scores(self):
        try:
            with open("high_scores.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default high scores if file doesn't exist or is invalid
            return {"scores": []}
    
    def save_high_scores(self):
        with open("high_scores.json", "w") as f:
            json.dump(self.high_scores, f)
    
    def add_high_score(self, score):
        self.high_scores["scores"].append(score)
        self.high_scores["scores"].sort(reverse=True)
        self.high_scores["scores"] = self.high_scores["scores"][:10]  # Keep only top 10
        self.save_high_scores()
    
    def run_menu(self):
        menu = MainMenu(self.screen, self.clock, self.sound_manager)
        selection = menu.run()
        
        if selection == "start":
            self.current_state = "game"
        elif selection == "scores":
            self.current_state = "high_scores"
        elif selection == "instructions":
            self.current_state = "instructions"
        elif selection == "settings":
            self.current_state = "settings"
        elif selection == "exit":
            self.running = False
    
    def run_game(self):
        # Stop menu music before starting game
        self.sound_manager.stop_music()
        
        # Create game instance
        game = Game(self.screen, self.clock, self.sound_manager)
        
        # Apply difficulty settings
        self.difficulty_settings.apply_to_difficulty_manager(game.difficulty)
        
        # Run the game
        result = game.run()
        
        # Process game result
        if result["action"] == "quit":
            self.running = False
        elif result["action"] == "menu":
            self.current_state = "menu"
            # Add score to high scores if game was completed
            if "score" in result:
                self.add_high_score(result["score"])
        
        # Restart menu music when returning to menu
        if self.current_state == "menu":
            # Make sure engine sound is stopped
            self.sound_manager.stop("engine")
            self.sound_manager.play_music("menu_music.mp3")
    
    def run_high_scores(self):
        high_scores_screen = HighScores(self.screen, self.clock, self.sound_manager, self.high_scores)
        result = high_scores_screen.run()
        
        if result == "exit":
            self.running = False
        else:
            self.current_state = "menu"
    
    def run_instructions(self):
        instructions_screen = Instructions(self.screen, self.clock, self.sound_manager)
        result = instructions_screen.run()
        
        if result == "exit":
            self.running = False
        else:
            self.current_state = "menu"
    
    def run_settings(self):
        settings_screen = Settings(self.screen, self.clock, self.sound_manager)
        result = settings_screen.run()
        
        # Save settings when returning from settings screen
        self.settings_manager.update_from_sound_manager(self.sound_manager)
        
        if result == "exit":
            self.running = False
        else:
            self.current_state = "menu"
    
    def run(self):
        while self.running:
            if self.current_state == "menu":
                self.run_menu()
            elif self.current_state == "game":
                self.run_game()
            elif self.current_state == "high_scores":
                self.run_high_scores()
            elif self.current_state == "instructions":
                self.run_instructions()
            elif self.current_state == "settings":
                self.run_settings()
        
        # Clean up
        pygame.quit()
        sys.exit()

# Start the game if run directly
if __name__ == "__main__":
    manager = GameManager()
    manager.run()
"""
    
    # Write header to output file
    with open(output_file, "w") as outfile:
        outfile.write(header)
    
    # Process each file
    for file_name in files_to_combine:
        if os.path.exists(file_name):
            print(f"Processing {file_name}...")
            
            # Read file content
            with open(file_name, "r") as infile:
                content = infile.read()
            
            # Extract class definitions and functions
            lines = content.split("\n")
            processed_lines = []
            
            # Skip imports and other non-essential parts
            in_class_or_function = False
            class_indent = 0
            
            for line in lines:
                # Skip import lines
                if line.startswith("import ") or line.startswith("from "):
                    continue
                
                # Detect start of class or function
                if line.startswith("class ") or line.startswith("def "):
                    in_class_or_function = True
                    class_indent = len(line) - len(line.lstrip())
                    processed_lines.append("\n#-------------------------------------------------------")
                    processed_lines.append(f"# {line.strip()}")
                    processed_lines.append("#-------------------------------------------------------")
                
                # Add line if in class or function
                if in_class_or_function:
                    processed_lines.append(line)
                
                # Detect end of class or function (empty line with same indent as start)
                if in_class_or_function and line.strip() == "" and len(processed_lines) > 0:
                    next_non_empty = next((l for l in lines[lines.index(line)+1:] if l.strip()), "")
                    if next_non_empty and len(next_non_empty) - len(next_non_empty.lstrip()) <= class_indent:
                        in_class_or_function = False
            
            # Write processed content to output file
            with open(output_file, "a") as outfile:
                outfile.write("\n".join(processed_lines))
                outfile.write("\n\n")
        else:
            print(f"Warning: {file_name} not found, skipping...")
    
    # Write footer to output file
    with open(output_file, "a") as outfile:
        outfile.write(footer)
    
    print(f"Successfully created {output_file}")

if __name__ == "__main__":
    combine_files()