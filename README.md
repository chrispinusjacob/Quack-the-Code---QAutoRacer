# QAutoRacer - Synthwave Edition

A retro-style racing game with synthwave aesthetics, created with Python and Pygame.

## Description

QAutoRacer is a racing game inspired by classic arcade racers with a modern synthwave twist. Race through procedurally generated tracks with neon colors and retro vibes! The game demonstrates pseudo-3D rendering techniques used in classic racing games from the 80s and 90s.

## Features

- Procedurally generated endless tracks with curves and hills
- Synthwave/retrowave visual aesthetics with neon colors
- Physics-based car handling with realistic acceleration and steering
- Obstacle avoidance gameplay with increasing difficulty
- Score tracking and speedometer
- Educational insights into classic game development techniques
- Advanced features:
  - Dynamic track generation with varying complexity
  - Adaptive difficulty that adjusts to player skill
  - Dynamic commentary based on gameplay events
  - Multiple visual themes (synthwave, retrowave, cyberpunk)

## Educational Value

This game demonstrates several important game development concepts:
- **Pseudo-3D Rendering**: The game uses a technique called "pseudo-3D" or "fake 3D" that was popular in early racing games before true 3D graphics were possible.
- **Procedural Generation**: The track is generated procedurally, creating an endless and unique racing experience.
- **Game Physics**: Simple but effective physics for car handling, including acceleration, deceleration, and centrifugal force on curves.
- **Collision Detection**: Basic collision detection between the player's car and obstacles.
- **Game State Management**: The game demonstrates proper state management (title screen, playing, game over).
- **Adaptive Difficulty**: The game analyzes player performance and adjusts difficulty accordingly.

## Controls

- **W/Up Arrow**: Accelerate
- **S/Down Arrow**: Brake
- **A/Left Arrow**: Steer left
- **D/Right Arrow**: Steer right
- **Space**: Start game / Restart after game over
- **Escape**: Quit game

## Requirements

- Python 3.6+
- Pygame 2.5.2+
- NumPy 1.26.0+

## Installation

1. Make sure you have Python installed
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the game:
   ```
   python main.py
   ```
   
   Or simply double-click the `run_game.bat` file (Windows)

## How to Play

Navigate your car through the procedurally generated track, avoiding obstacles along the way. The game gets progressively more challenging as you drive further. Your score increases based on the distance traveled.

## Sound Credits

The game uses the following sound effects:
- Engine sound
- Crash sound
- Score milestone sound

## Development Process

This game was created as part of the "That's Entertainment!" challenge. The development process included:

1. Setting up the basic game structure and pseudo-3D rendering
2. Implementing car physics and controls
3. Creating procedurally generated tracks with varying curves and hills
4. Adding obstacles and collision detection
5. Designing the synthwave visual aesthetic
6. Implementing game states (title, playing, game over)
7. Adding advanced features like adaptive difficulty and dynamic commentary
8. Adding sound effects and educational elements

## Credits

Created as part of the "That's Entertainment!" challenge.

## License

MIT License