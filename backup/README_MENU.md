# Retro Racer '90 - Menu System

This menu system adds a complete menu interface to the Retro Racer game.

## Features

- Main Menu with:
  - Start Game
  - Settings
  - High Scores
  - Instructions
  - Exit

- Pause Menu with:
  - Resume
  - Restart
  - Main Menu
  - Quit Game

- Animated buttons with hover effects
- Sound effects for menu interactions
- Background music for menus
- Random tips on the main menu screen

## How to Run

1. Make sure you have all the required files:
   - `game_objects.py` - Car and Orb classes
   - `menu_drawing.py` - Menu drawing functions
   - `game_with_menu.py` - Main game implementation with menu integration
   - `run_game.py` - Simple runner script

2. Run the game with menu:
   ```
   python run_game.py
   ```

## Controls

- **Arrow Keys** or **A/D**: Move car left/right
- **ESC**: Pause game / Return to previous menu
- **Space**: Restart after game over
- **Mouse**: Navigate menus

## Sound Effects

For the best experience, add these sound files to your `assets/sounds` directory:
- `menu_music.mp3` - Background music for menus
- `click.mp3` - Button click sound
- `hover.mp3` - Button hover sound

## Troubleshooting

If you encounter issues:

1. Make sure all required files are in the correct locations
2. Check that your font loading function works correctly
3. Ensure that the menu system is imported correctly
4. If buttons don't work, try running the game in a window (not fullscreen)

## Credits

Created for Retro Racer '90 game