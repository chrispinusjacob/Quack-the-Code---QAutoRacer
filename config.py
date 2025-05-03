import pygame
import os

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
ROAD_WIDTH = 2000
SEGMENT_LENGTH = 200
RUMBLE_LENGTH = 3
LANES = 3

# Advanced configuration
CONFIG = {
    "difficulty_scaling": 0.0001,  # How quickly the game gets harder
    "max_obstacles": 30,           # Maximum obstacles on screen
    "draw_distance": 300,          # How far ahead to render (segments)
    "fog_density": 5,              # Fog effect intensity
    "camera_height": 1000,         # Camera height above road
    "camera_depth": 0.84,          # Camera depth (field of view)
    "centrifugal_factor": 0.3,     # How much curves pull the car
    "offroad_deceleration": 0.95,  # Speed multiplier when off road
    "night_mode": False,           # Night mode toggle
    "debug_mode": False            # Debug information toggle
}

# Colors
SKY = (10, 10, 40)
NIGHT_SKY = (5, 5, 20)
GROUND = (16, 16, 16)
RUMBLE_LIGHT = (255, 255, 255)
RUMBLE_DARK = (0, 0, 0)
ROAD = (100, 100, 100)
ROAD_NIGHT = (70, 70, 70)
GRASS_LIGHT = (16, 200, 16)
GRASS_DARK = (0, 154, 0)
GRASS_NIGHT_LIGHT = (8, 100, 8)
GRASS_NIGHT_DARK = (0, 77, 0)
LANE_MARKER = (255, 255, 255)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (0, 191, 255)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (138, 43, 226)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)
NEON_RED = (255, 0, 0)  # Added for completeness

# Color schemes
COLOR_SCHEMES = {
    "synthwave": {
        "sky": SKY,
        "ground": GROUND,
        "road": ROAD,
        "rumble_light": RUMBLE_LIGHT,
        "rumble_dark": RUMBLE_DARK,
        "grass_light": GRASS_LIGHT,
        "grass_dark": GRASS_DARK,
        "lane": LANE_MARKER,
        "car": NEON_PINK,
        "obstacles": [NEON_BLUE, NEON_GREEN, NEON_PURPLE, NEON_YELLOW]
    },
    "night": {
        "sky": NIGHT_SKY,
        "ground": GROUND,
        "road": ROAD_NIGHT,
        "rumble_light": RUMBLE_LIGHT,
        "rumble_dark": RUMBLE_DARK,
        "grass_light": GRASS_NIGHT_LIGHT,
        "grass_dark": GRASS_NIGHT_DARK,
        "lane": LANE_MARKER,
        "car": NEON_BLUE,
        "obstacles": [NEON_PINK, NEON_ORANGE, NEON_PURPLE, NEON_GREEN]
    }
}

# Game states
STATE_TITLE = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")

# Create directories if they don't exist
os.makedirs(SOUND_DIR, exist_ok=True)

# Initialize pygame
pygame.mixer.pre_init(44100, -16, 2, 2048)  # Setup for less sound lag
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Set up the display with more options
flags = pygame.HWSURFACE | pygame.DOUBLEBUF
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
pygame.display.set_caption("QAutoRacer - Synthwave Edition")
icon = pygame.Surface((32, 32))
icon.fill(NEON_PINK)
pygame.draw.rect(icon, NEON_BLUE, (8, 8, 16, 16))
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Global variables
high_score = 0
current_color_scheme = "synthwave"

def get_color_scheme():
    """Get current color scheme based on settings"""
    if CONFIG["night_mode"]:
        return COLOR_SCHEMES["night"]
    return COLOR_SCHEMES["synthwave"]