# Menu System Integration Guide

This guide explains how to integrate the menu system into your Retro Racer game.

## Files Created

1. **menu_system.py** - Contains all menu classes and functionality
2. **menu_demo.py** - A standalone demo to test the menu system
3. **integration_guide.md** - This guide

## How to Test the Menu System

Run `menu_demo.py` to see the menu system in action. This will demonstrate:
- Main menu with buttons
- Settings menu with theme selection
- Instructions screen
- High scores screen
- Pause menu
- Simple game screen (placeholder)

## Integration Steps

### Step 1: Import the Menu System

Add this import to your main.py file:

```python
from menu_system import (
    MainMenu, PauseMenu, SettingsMenu, InstructionsMenu, HighScoresMenu,
    STATE_MAIN_MENU, STATE_PLAYING, STATE_GAME_OVER, STATE_PAUSED, 
    STATE_SETTINGS, STATE_HIGH_SCORES, STATE_INSTRUCTIONS
)
```

### Step 2: Modify the Game Class

Update your Game class to include menu objects and state management:

```python
def __init__(self):
    self.running = True
    self.game_over = False
    self.state = STATE_MAIN_MENU  # Start at main menu
    self.score = 0
    self.high_score = 0
    self.scroll_speed = INITIAL_SCROLL_SPEED
    self.enemy_speed = INITIAL_ENEMY_SPEED
    self.player = Car(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100, NEON_PINK, True)
    self.enemies = []
    self.orbs = []
    self.road_segments = []
    self.stripes = []
    self.game_time = 0
    
    # Create menu objects
    self.main_menu = MainMenu(screen, get_font)
    self.pause_menu = PauseMenu(screen, get_font)
    self.settings_menu = SettingsMenu(screen, get_font)
    self.instructions_menu = InstructionsMenu(screen, get_font)
    self.high_scores_menu = HighScoresMenu(screen, get_font)
    
    # Create road segments
    # ... rest of your initialization code
```

### Step 3: Update the handle_events Method

Modify your handle_events method to handle menu navigation:

```python
def handle_events(self):
    events = pygame.event.get()
    
    for event in events:
        if event.type == QUIT:
            self.running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if self.state == STATE_PLAYING:
                    self.state = STATE_PAUSED
                    if has_sound:
                        engine_sound.stop()
                elif self.state == STATE_PAUSED:
                    self.state = STATE_PLAYING
                    if has_sound and not self.game_over:
                        engine_sound.play(-1)
                elif self.state in [STATE_SETTINGS, STATE_INSTRUCTIONS, STATE_HIGH_SCORES]:
                    self.state = STATE_MAIN_MENU
            elif event.key == K_SPACE and self.game_over:
                self.reset()
    
    # Handle menu states
    if self.state == STATE_MAIN_MENU:
        new_state = self.main_menu.handle_events(events)
        if new_state != self.state:
            self.state = new_state
            if new_state == STATE_PLAYING:
                # Start engine sound when starting game
                if has_sound:
                    engine_sound.play(-1)
    elif self.state == STATE_PAUSED:
        new_state = self.pause_menu.handle_events(events)
        if new_state == -1:  # Special code for restart
            self.reset()
            self.state = STATE_PLAYING
        elif new_state != self.state:
            self.state = new_state
    elif self.state == STATE_SETTINGS:
        new_state = self.settings_menu.handle_events(events)
        if new_state != self.state:
            self.state = new_state
    elif self.state == STATE_INSTRUCTIONS:
        new_state = self.instructions_menu.handle_events(events)
        if new_state != self.state:
            self.state = new_state
    elif self.state == STATE_HIGH_SCORES:
        new_state = self.high_scores_menu.handle_events(events)
        if new_state != self.state:
            self.state = new_state
    
    # Continuous movement (only when playing)
    if self.state == STATE_PLAYING and not self.game_over:
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.player.x -= self.player.speed
        if keys[K_RIGHT] or keys[K_d]:
            self.player.x += self.player.speed
        
        # Keep player within road boundaries
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH
        self.player.x = max(road_left + 5, min(road_right - self.player.width - 5, self.player.x))
```

### Step 4: Update the update Method

Modify your update method to respect game state:

```python
def update(self):
    dt = clock.get_time() / 1000.0  # Delta time in seconds
    
    if self.state == STATE_MAIN_MENU:
        self.main_menu.update(dt)
        return
    elif self.state == STATE_PAUSED or self.state == STATE_SETTINGS or self.state == STATE_INSTRUCTIONS or self.state == STATE_HIGH_SCORES:
        return
    elif self.game_over:
        return
    
    # Rest of your update code...
```

### Step 5: Update the draw Method

Modify your draw method to draw the appropriate screen based on state:

```python
def draw(self):
    # Fill background
    screen.fill(BLACK)
    
    # Draw starfield background
    for i in range(100):
        x = (i * 17) % SCREEN_WIDTH
        y = (i * 23) % SCREEN_HEIGHT
        size = random.randint(1, 3)
        brightness = 100 + int(math.sin(self.game_time + i) * 50)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(screen, color, (x, y), size)
    
    # Draw appropriate screen based on state
    if self.state == STATE_MAIN_MENU:
        self.main_menu.draw()
        pygame.display.flip()
        return
    elif self.state == STATE_SETTINGS:
        self.settings_menu.draw()
        pygame.display.flip()
        return
    elif self.state == STATE_INSTRUCTIONS:
        self.instructions_menu.draw()
        pygame.display.flip()
        return
    elif self.state == STATE_HIGH_SCORES:
        self.high_scores_menu.draw()
        pygame.display.flip()
        return
    
    # Draw game elements
    # ... rest of your game drawing code
    
    # Draw pause menu if paused
    if self.state == STATE_PAUSED:
        self.pause_menu.draw()
    
    pygame.display.flip()
```

### Step 6: Update the reset Method

Modify your reset method to reset game state:

```python
def reset(self):
    self.game_over = False
    self.score = 0
    self.scroll_speed = INITIAL_SCROLL_SPEED
    self.enemy_speed = INITIAL_ENEMY_SPEED
    self.player = Car(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100, NEON_PINK, True)
    self.enemies = []
    self.orbs = []
    self.game_time = 0
    
    # Restart engine sound
    if has_sound:
        engine_sound.play(-1)
```

## Additional Features

### High Score Saving

When the game ends, add this code to save the high score:

```python
if self.score > self.high_score:
    self.high_score = self.score
    
    # Add to high scores list
    from menu_system import save_high_scores, load_high_scores
    scores = load_high_scores()
    scores.append({"name": "YOU", "score": self.score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    save_high_scores(scores[:10])  # Keep only top 10
```

### Sound Effects

To add sound effects to menu buttons:

1. Create sound files:
   - `click.mp3` - Button click sound
   - `hover.mp3` - Button hover sound
   - `menu_music.mp3` - Background music for menus

2. Place them in your `assets/sounds` directory

The menu system will automatically detect and use these sounds if they exist.

## Customization

You can customize the menu system by:

1. Modifying the colors in `menu_system.py`
2. Adding more buttons or menu screens
3. Changing the text and layout
4. Adding animations or effects

## Troubleshooting

If you encounter issues:

1. Make sure all required files are in the correct locations
2. Check that your font loading function works correctly
3. Ensure your game state management is consistent
4. Verify that the menu system is imported correctly