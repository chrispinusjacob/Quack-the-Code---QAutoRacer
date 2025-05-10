# Retro Racer '90

A retro-style vertical scrolling racing game with neon 80s aesthetics, created with Python and Pygame.

## Description

Retro Racer '90 is a vertical scrolling racing game inspired by classic arcade games from the 90s. Control your pixel-art car, avoid enemy vehicles, and collect glowing orbs to increase your score. The game features a neon 80s color palette, retro fonts, and pixel graphics for an authentic arcade experience.

## Features

- Vertical scrolling gameplay with pixel-art graphics
- Player-controlled car that moves left and right
- Enemy cars that spawn at the top and scroll down
- Collectible glowing orbs that increase your score
- Gradually increasing difficulty as time progresses
- Neon 80s color palette with glowing effects
- Retro-style sound effects
- Score and high score tracking
- Game over screen with restart option

## Controls

- **A/Left Arrow**: Move left
- **D/Right Arrow**: Move right
- **Space**: Restart after game over
- **Escape**: Quit game

## Requirements

- Python 3.6+
- Pygame 2.5.2+

## Installation

1. Make sure you have Python installed
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the game:
   ```
   python retro_racer.py
   ```
   
   Or simply double-click the `run_retro_racer.bat` file (Windows)

## How to Play

Control your car (pink) to avoid enemy vehicles while collecting glowing cyan orbs. The game gets progressively more challenging as the speed increases over time. Your score increases based on time survived and orbs collected.

## Customization

You can customize the game by adding your own assets:

- **Fonts**: Place a pixel font named "pixel.ttf" in the `assets/fonts` directory
- **Sounds**: Add sound files to the `assets/sounds` directory:
  - engine.wav: Engine sound effect (looping)
  - crash.wav: Crash sound effect
  - pickup.wav: Orb pickup sound effect

## Code Structure

The game is organized with the following classes:

- **Game**: Main game logic and loop
- **Car**: Player and enemy car objects
- **Orb**: Collectible orbs that increase score

## Credits

Created as part of the "That's Entertainment!" challenge.

## License

MIT License