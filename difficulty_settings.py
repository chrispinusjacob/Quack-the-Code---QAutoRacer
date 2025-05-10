import json
import os

class DifficultySettings:
    """
    Manages difficulty settings for the game.
    Provides easy, medium, and hard difficulty presets.
    """
    def __init__(self):
        self.settings_file = "difficulty_settings.json"
        
        # Default difficulty settings
        self.difficulty_presets = {
            "easy": {
                "name": "EASY",
                # Slower game speed
                "initial_enemy_speed": 1.5,
                "initial_scroll_speed": 2.5,
                # Fewer enemies
                "initial_enemy_spawn_rate": 0.015,
                # More orbs for points
                "initial_orb_spawn_rate": 0.035,
                # Very slow progression
                "speed_increase_rate": 0.001,
                "spawn_rate_increase": 0.000005,
                # Lower maximum speeds
                "max_enemy_speed": 6.0,
                "max_scroll_speed": 8.0,
                "max_enemy_spawn_rate": 0.04,
                "max_orb_spawn_rate": 0.07
            },
            "medium": {
                "name": "MEDIUM",
                # Balanced game speed
                "initial_enemy_speed": 3.0,
                "initial_scroll_speed": 5.0,
                # Moderate enemy count
                "initial_enemy_spawn_rate": 0.03,
                # Balanced orb spawning
                "initial_orb_spawn_rate": 0.02,
                # Standard progression
                "speed_increase_rate": 0.002,
                "spawn_rate_increase": 0.00002,
                # Moderate maximum speeds
                "max_enemy_speed": 10.0,
                "max_scroll_speed": 12.0,
                "max_enemy_spawn_rate": 0.08,
                "max_orb_spawn_rate": 0.04
            },
            "hard": {
                "name": "HARD",
                # Fast game speed from the start
                "initial_enemy_speed": 7.0,
                "initial_scroll_speed": 9.0,
                # Many enemies
                "initial_enemy_spawn_rate": 0.05,
                # Fewer orbs
                "initial_orb_spawn_rate": 0.01,
                # Rapid progression
                "speed_increase_rate": 0.004,
                "spawn_rate_increase": 0.0002,
                # High maximum speeds
                "max_enemy_speed": 15.0,
                "max_scroll_speed": 18.0,
                "max_enemy_spawn_rate": 0.15,
                "max_orb_spawn_rate": 0.025
            }
        }
        
        # Current difficulty level
        self.current_difficulty = "medium"
        
        # Load saved settings if available
        self.load_settings()
    
    def load_settings(self):
        """Load difficulty settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as f:
                    data = json.load(f)
                    if "difficulty" in data:
                        self.current_difficulty = data["difficulty"]
                        print(f"Loaded difficulty setting: {self.current_difficulty}")
        except Exception as e:
            print(f"Error loading difficulty settings: {e}")
    
    def save_settings(self):
        """Save current difficulty settings to file"""
        try:
            with open(self.settings_file, "w") as f:
                json.dump({"difficulty": self.current_difficulty}, f)
                print(f"Saved difficulty setting: {self.current_difficulty}")
        except Exception as e:
            print(f"Error saving difficulty settings: {e}")
    
    def get_current_settings(self):
        """Get the current difficulty settings"""
        return self.difficulty_presets[self.current_difficulty]
    
    def set_difficulty(self, difficulty):
        """Set the current difficulty level"""
        if difficulty in self.difficulty_presets:
            self.current_difficulty = difficulty
            self.save_settings()
            return True
        return False
    
    def get_difficulty_name(self):
        """Get the name of the current difficulty level"""
        return self.difficulty_presets[self.current_difficulty]["name"]
    
    def apply_to_difficulty_manager(self, difficulty_manager):
        """Apply current settings to a difficulty manager instance"""
        settings = self.get_current_settings()
        
        # Apply all settings
        difficulty_manager.initial_enemy_speed = settings["initial_enemy_speed"]
        difficulty_manager.initial_scroll_speed = settings["initial_scroll_speed"]
        difficulty_manager.initial_enemy_spawn_rate = settings["initial_enemy_spawn_rate"]
        difficulty_manager.initial_orb_spawn_rate = settings["initial_orb_spawn_rate"]
        difficulty_manager.speed_increase_rate = settings["speed_increase_rate"]
        difficulty_manager.spawn_rate_increase = settings["spawn_rate_increase"]
        difficulty_manager.max_enemy_speed = settings["max_enemy_speed"]
        difficulty_manager.max_scroll_speed = settings["max_scroll_speed"]
        difficulty_manager.max_enemy_spawn_rate = settings["max_enemy_spawn_rate"]
        difficulty_manager.max_orb_spawn_rate = settings["max_orb_spawn_rate"]
        
        # Set current values to initial values
        difficulty_manager.enemy_speed = settings["initial_enemy_speed"]
        difficulty_manager.scroll_speed = settings["initial_scroll_speed"]
        difficulty_manager.enemy_spawn_rate = settings["initial_enemy_spawn_rate"]
        difficulty_manager.orb_spawn_rate = settings["initial_orb_spawn_rate"]
        
        # Set difficulty level
        difficulty_manager.difficulty_level = self.current_difficulty
        
        # Reset the difficulty manager
        difficulty_manager.game_time = 0
        
        print(f"Applied {self.current_difficulty} difficulty settings to difficulty manager")
        return settings