import pygame
import sys
import os
import json
from pygame.locals import *

# Import game components
from improved_game import Game
from main_menu import MainMenu
from sound_manager import SoundManager
from difficulty_settings import DifficultySettings
from settings_manager import SettingsManager

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "QAutoGame '90"

class GameManager:
    """
    Main game manager that handles transitions between different game states:
    - Main menu
    - Game
    - High scores
    - Instructions
    - Settings
    """
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        
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
        """Load high scores from file"""
        try:
            with open("high_scores.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default high scores if file doesn't exist or is invalid
            return {"scores": []}
    
    def save_high_scores(self):
        """Save high scores to file"""
        with open("high_scores.json", "w") as f:
            json.dump(self.high_scores, f)
    
    def add_high_score(self, score):
        """Add a new high score"""
        self.high_scores["scores"].append(score)
        self.high_scores["scores"].sort(reverse=True)
        self.high_scores["scores"] = self.high_scores["scores"][:10]  # Keep only top 10
        self.save_high_scores()
    
    def run_menu(self):
        """Run the main menu"""
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
        """Run the game"""
        # Stop menu music before starting game
        self.sound_manager.stop_music()
        
        # Create game instance
        game = Game(self.screen, self.clock, self.sound_manager)
        
        # Apply difficulty settings
        self.difficulty_settings.apply_to_difficulty_manager(game.difficulty)
        print(f"Applied {self.difficulty_settings.current_difficulty} difficulty to game")
        
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
        """Show high scores screen"""
        from high_scores import HighScores
        high_scores_screen = HighScores(self.screen, self.clock, self.sound_manager, self.high_scores)
        result = high_scores_screen.run()
        
        if result == "exit":
            self.running = False
        else:
            self.current_state = "menu"
    
    def run_instructions(self):
        """Show instructions screen"""
        from instructions import Instructions
        instructions_screen = Instructions(self.screen, self.clock, self.sound_manager)
        result = instructions_screen.run()
        
        if result == "exit":
            self.running = False
        else:
            self.current_state = "menu"
    
    def run_settings(self):
        """Show settings screen"""
        from settings import Settings
        settings_screen = Settings(self.screen, self.clock, self.sound_manager)
        result = settings_screen.run()
        
        # Save settings when returning from settings screen
        self.settings_manager.update_from_sound_manager(self.sound_manager)
        
        if result == "exit":
            self.running = False
        else:
            self.current_state = "menu"
    
    def run(self):
        """Main game loop that manages different states"""
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