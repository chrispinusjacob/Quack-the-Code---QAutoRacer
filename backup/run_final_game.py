import pygame
import sys
import os
import shutil

# Check if the final_game.py file exists
if not os.path.exists('final_game.py'):
    # Combine all parts into final_game.py
    with open('final_game.py', 'w') as outfile:
        for i in range(1, 8):
            part_file = f'final_game_part{i}.py'
            if os.path.exists(part_file):
                with open(part_file, 'r') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n\n')

# Import and run the game
from final_game import Game

# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()