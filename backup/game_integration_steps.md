# Game Menu Integration Steps

Great news! The simple menu system is working correctly. Here's how to integrate it with your main game:

## Step 1: Use the SimpleButton class

The SimpleButton class from `simple_game_menu.py` works reliably. Use this instead of the more complex Button class.

## Step 2: Add Game States to Your Main Game

Add these state constants to your main game:
```python
# Game states
STATE_MAIN_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_PAUSED = 3
STATE_SETTINGS = 4
STATE_HIGH_SCORES = 5
STATE_INSTRUCTIONS = 6
```

## Step 3: Modify Your Game Class

Update your Game class to start in the main menu state:
```python
def __init__(self):
    self.running = True
    self.game_over = False
    self.state = STATE_MAIN_MENU  # Start at main menu
    # ... rest of your initialization
    
    # Create menu buttons
    self.main_menu_buttons = create_main_menu_buttons()
    self.pause_menu_buttons = create_pause_menu_buttons()
```

## Step 4: Update Your handle_events Method

Modify your handle_events method to handle menu navigation:
```python
def handle_events(self):
    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False
    
    for event in events:
        if event.type == QUIT:
            self.running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicked = True
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
        # Update main menu buttons
        for button in self.main_menu_buttons.values():
            button.update(mouse_pos)
        
        # Check for button clicks
        if mouse_clicked:
            if self.main_menu_buttons["start"].is_clicked(mouse_pos, mouse_clicked):
                self.state = STATE_PLAYING
                if has_sound:
                    engine_sound.play(-1)
            elif self.main_menu_buttons["settings"].is_clicked(mouse_pos, mouse_clicked):
                self.state = STATE_SETTINGS
            elif self.main_menu_buttons["high_scores"].is_clicked(mouse_pos, mouse_clicked):
                self.state = STATE_HIGH_SCORES
            elif self.main_menu_buttons["instructions"].is_clicked(mouse_pos, mouse_clicked):
                self.state = STATE_INSTRUCTIONS
            elif self.main_menu_buttons["exit"].is_clicked(mouse_pos, mouse_clicked):
                self.running = False
    
    elif self.state == STATE_PAUSED:
        # Update pause menu buttons
        for button in self.pause_menu_buttons.values():
            button.update(mouse_pos)
        
        # Check for button clicks
        if mouse_clicked:
            if self.pause_menu_buttons["resume"].is_clicked(mouse_pos, mouse_clicked):
                self.state = STATE_PLAYING
                if has_sound and not self.game_over:
                    engine_sound.play(-1)
            elif self.pause_menu_buttons["restart"].is_clicked(mouse_pos, mouse_clicked):
                self.reset()
                self.state = STATE_PLAYING
            elif self.pause_menu_buttons["main_menu"].is_clicked(mouse_pos, mouse_clicked):
                self.state = STATE_MAIN_MENU
            elif self.pause_menu_buttons["quit"].is_clicked(mouse_pos, mouse_clicked):
                self.running = False
    
    # Only process game controls if in playing state
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

## Step 5: Update Your update Method

Modify your update method to respect game state:
```python
def update(self):
    dt = clock.get_time() / 1000.0  # Delta time in seconds
    
    # Only update game if in playing state
    if self.state != STATE_PLAYING or self.game_over:
        return
    
    self.game_time += dt
    
    # Rest of your update code...
```

## Step 6: Update Your draw Method

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
        draw_main_menu(self.main_menu_buttons, self.game_time)
    elif self.state == STATE_SETTINGS:
        draw_settings_screen()
    elif self.state == STATE_HIGH_SCORES:
        draw_high_scores_screen()
    elif self.state == STATE_INSTRUCTIONS:
        draw_instructions_screen()
    else:
        # Draw game elements (only if playing or paused)
        # Draw road
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        
        # Draw road segments
        for segment in self.road_segments:
            screen.blit(segment['sprite'], (road_left, segment['y']))
        
        # Draw stripes
        for stripe in self.stripes:
            # Left stripe
            screen.blit(stripe['sprite'], (road_left - 15, stripe['y']))
            # Right stripe
            screen.blit(stripe['sprite'], (road_left + ROAD_WIDTH + 5, stripe['y']))
        
        # Draw orbs
        for orb in self.orbs:
            orb.draw(screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # Draw player
        self.player.draw(screen)
        
        # Draw HUD
        self.draw_hud()
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
        
        # Draw pause menu if paused
        if self.state == STATE_PAUSED:
            draw_pause_menu(self.pause_menu_buttons)
    
    pygame.display.flip()
```

## Step 7: Copy the Menu Drawing Functions

Copy these functions from `simple_game_menu.py`:
- `create_main_menu_buttons()`
- `create_pause_menu_buttons()`
- `draw_main_menu()`
- `draw_pause_menu()`
- `draw_settings_screen()`
- `draw_high_scores_screen()`
- `draw_instructions_screen()`

## Step 8: Test Your Integration

Run your game and make sure:
1. The game starts at the main menu
2. All buttons work correctly
3. The pause menu appears when ESC is pressed during gameplay
4. You can navigate between all screens

## Need More Help?

If you need more detailed implementation, I can provide specific code for each part of the integration.