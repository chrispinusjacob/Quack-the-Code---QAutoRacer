import pygame
import sys
import os
from game_class import Game

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("QAutoGame '90")
clock = pygame.time.Clock()

# Create and run the game
game = Game(screen, clock)
game.run()