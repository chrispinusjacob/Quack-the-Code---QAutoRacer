import pygame
import sys
import os

# Check if the game file exists
if not os.path.exists('retro_racer_complete.py'):
    print("Error: Game file not found. Please make sure retro_racer_complete.py exists.")
    sys.exit(1)

# Import and run the game
try:
    from retro_racer_complete import Game
    
    # Start the game
    if __name__ == "__main__":
        print("Starting QAutoGame '90...")
        game = Game()
        game.run()
except Exception as e:
    print(f"Error starting the game: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)