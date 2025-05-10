import math

class DifficultyManager:
    """
    Manages game difficulty progression over time.
    Controls enemy spawn rate, speed, and other difficulty parameters.
    """
    def __init__(self):
        # Base settings (medium difficulty by default)
        self.initial_enemy_speed = 3.0
        self.initial_scroll_speed = 5.0
        self.initial_enemy_spawn_rate = 0.03
        self.initial_orb_spawn_rate = 0.02
        
        # Current settings
        self.enemy_speed = self.initial_enemy_speed
        self.scroll_speed = self.initial_scroll_speed
        self.enemy_spawn_rate = self.initial_enemy_spawn_rate
        self.orb_spawn_rate = self.initial_orb_spawn_rate
        
        # Progression rates
        self.speed_increase_rate = 0.0001
        self.spawn_rate_increase = 0.00005
        
        # Difficulty caps
        self.max_enemy_speed = 12.0
        self.max_scroll_speed = 15.0
        self.max_enemy_spawn_rate = 0.08
        self.max_orb_spawn_rate = 0.04
        
        # Game time tracking
        self.game_time = 0
        
        # Current difficulty level
        self.difficulty_level = "medium"
        
        # Try to load difficulty settings
        try:
            from difficulty_settings import DifficultySettings
            self.difficulty_settings = DifficultySettings()
            # Apply saved difficulty settings
            self.difficulty_settings.apply_to_difficulty_manager(self)
        except ImportError:
            print("Difficulty settings module not found, using default settings")
            self.difficulty_settings = None
        
    def update(self, dt):
        """Update difficulty based on elapsed time"""
        self.game_time += dt
        
        # Calculate difficulty factor (increases over time but with diminishing returns)
        difficulty_factor = 1.0 + math.log(1 + self.game_time / 60)
        
        # Update speeds with caps
        self.scroll_speed = min(
            self.max_scroll_speed,
            self.initial_scroll_speed + (self.speed_increase_rate * dt * 6000 * difficulty_factor)
        )
        
        self.enemy_speed = min(
            self.max_enemy_speed,
            self.initial_enemy_speed + (self.speed_increase_rate * dt * 6000 * difficulty_factor)
        )
        
        # Update spawn rates with caps
        self.enemy_spawn_rate = min(
            self.max_enemy_spawn_rate,
            self.initial_enemy_spawn_rate + (self.spawn_rate_increase * dt * 60 * difficulty_factor)
        )
        
        self.orb_spawn_rate = min(
            self.max_orb_spawn_rate,
            self.initial_orb_spawn_rate + (self.spawn_rate_increase * dt * 60 * 0.5 * difficulty_factor)
        )
    
    def reset(self):
        """Reset difficulty to initial values"""
        self.enemy_speed = self.initial_enemy_speed
        self.scroll_speed = self.initial_scroll_speed
        self.enemy_spawn_rate = self.initial_enemy_spawn_rate
        self.orb_spawn_rate = self.initial_orb_spawn_rate
        self.game_time = 0
    
    def get_difficulty_percentage(self):
        """Returns current difficulty as a percentage (0-100)"""
        # Base it on scroll speed as a representative value
        speed_percent = (self.scroll_speed - self.initial_scroll_speed) / (self.max_scroll_speed - self.initial_scroll_speed)
        return min(100, int(speed_percent * 100))