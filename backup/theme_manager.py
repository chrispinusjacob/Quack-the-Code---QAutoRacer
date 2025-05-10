"""
Theme Manager for the game
Controls visual themes and color schemes
"""
import pygame

# Define theme colors
SYNTHWAVE_COLORS = {
    "background": (0, 0, 0),
    "road": (40, 40, 40),
    "stripe": (255, 255, 255),
    "player": (255, 20, 147),  # NEON_PINK
    "text": (0, 191, 255),     # NEON_BLUE
    "score": (57, 255, 20),    # NEON_GREEN
    "high_score": (0, 255, 255), # NEON_CYAN
    "enemy": [(57, 255, 20), (0, 191, 255), (138, 43, 226), (255, 255, 0), (255, 165, 0)]
}

CYBERPUNK_COLORS = {
    "background": (5, 0, 20),
    "road": (30, 30, 50),
    "stripe": (255, 215, 0),
    "player": (0, 255, 255),   # Cyan
    "text": (255, 50, 50),     # Red
    "score": (255, 215, 0),    # Gold
    "high_score": (0, 255, 127), # Spring Green
    "enemy": [(255, 50, 50), (255, 215, 0), (0, 255, 127), (148, 0, 211), (255, 105, 180)]
}

RETROWAVE_COLORS = {
    "background": (25, 0, 50),
    "road": (50, 0, 80),
    "stripe": (255, 255, 255),
    "player": (255, 105, 180), # Hot Pink
    "text": (255, 223, 0),     # Gold
    "score": (127, 255, 212),  # Aquamarine
    "high_score": (255, 165, 0), # Orange
    "enemy": [(127, 255, 212), (255, 223, 0), (255, 165, 0), (255, 105, 180), (148, 0, 211)]
}

NIGHT_COLORS = {
    "background": (5, 5, 30),
    "road": (20, 20, 40),
    "stripe": (200, 200, 200),
    "player": (220, 220, 220), # Silver
    "text": (180, 180, 255),   # Light Blue
    "score": (200, 255, 200),  # Light Green
    "high_score": (255, 255, 200), # Light Yellow
    "enemy": [(255, 200, 200), (200, 255, 200), (200, 200, 255), (255, 255, 200), (255, 200, 255)]
}

class ThemeManager:
    """Manages game visual themes"""
    
    def __init__(self):
        # Theme index: 0=Synthwave, 1=Cyberpunk, 2=Retrowave, 3=Night
        self.theme = 0  # Default to Synthwave
        
        # Theme names
        self.theme_names = ["SYNTHWAVE", "CYBERPUNK", "RETROWAVE", "NIGHT"]
        
        # Theme color schemes
        self.theme_colors = [
            SYNTHWAVE_COLORS,
            CYBERPUNK_COLORS,
            RETROWAVE_COLORS,
            NIGHT_COLORS
        ]
        
        # Star colors for each theme
        self.star_colors = [
            (255, 255, 255),  # White for Synthwave
            (0, 255, 255),    # Cyan for Cyberpunk
            (255, 223, 0),    # Gold for Retrowave
            (220, 220, 255)   # Light Blue for Night
        ]
    
    def set_theme(self, index):
        """Set the theme by index"""
        if 0 <= index < len(self.theme_names):
            self.theme = index
            return True
        return False
    
    def get_theme_name(self):
        """Get the current theme name"""
        return self.theme_names[self.theme]
    
    def get_colors(self):
        """Get the color scheme for the current theme"""
        return self.theme_colors[self.theme]
    
    def get_star_color(self):
        """Get the star color for the current theme"""
        return self.star_colors[self.theme]
    
    def next_theme(self):
        """Switch to the next theme"""
        self.theme = (self.theme + 1) % len(self.theme_names)
        return self.get_theme_name()
    
    def prev_theme(self):
        """Switch to the previous theme"""
        self.theme = (self.theme - 1) % len(self.theme_names)
        return self.get_theme_name()
    
    def create_road_segment(self, width, height):
        """Create a road segment with the current theme colors"""
        colors = self.get_colors()
        surface = pygame.Surface((width, height))
        surface.fill(colors["road"])
        return surface
    
    def create_stripe(self, width, height):
        """Create a road stripe with the current theme colors"""
        colors = self.get_colors()
        surface = pygame.Surface((width, height))
        surface.fill(colors["stripe"])
        return surface

# Create a global instance
theme_manager = ThemeManager()