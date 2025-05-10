import pygame
import sys
import math
import random
import os
from pygame.locals import *
from button import Button

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Neon 80s color palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (0, 191, 255)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (138, 43, 226)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)
NEON_CYAN = (0, 255, 255)

class Settings:
    """Settings screen for game configuration"""
    
    def __init__(self, screen, clock, sound_manager):
        # Current selected button for keyboard navigation
        self.selected_button = 0
        self.screen = screen
        self.clock = clock
        self.sound_manager = sound_manager
        self.running = True
        self.animation_time = 0
        self.stars = []
        
        # Create stars for background
        for i in range(100):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.uniform(1, 3),
                'speed': random.uniform(0.5, 2)
            })
        
        # Load or create fonts
        self.title_font = self.get_font(48)
        self.subtitle_font = self.get_font(36)
        self.text_font = self.get_font(24)
        self.small_font = self.get_font(18)  # Added missing small_font
        
        # Initialize difficulty settings
        try:
            from difficulty_settings import DifficultySettings
            self.difficulty_settings = DifficultySettings()
            current_difficulty = self.difficulty_settings.current_difficulty
        except ImportError:
            self.difficulty_settings = None
            current_difficulty = "medium"
        
        # Create buttons
        button_width = 300
        button_height = 60
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.buttons = [
            # Sound Effects toggle
            Button(button_x, 80, button_width, button_height, 
                  f"SOUND EFFECTS: {'ON' if self.sound_manager.sound_enabled else 'OFF'}", 
                  self.text_font, 
                  text_color=WHITE, hover_color=NEON_GREEN, 
                  border_color=NEON_GREEN, sound_manager=self.sound_manager),
            
            # Music toggle
            Button(button_x, 150, button_width, button_height, 
                  f"MUSIC: {'ON' if self.sound_manager.music_enabled else 'OFF'}", 
                  self.text_font, 
                  text_color=WHITE, hover_color=NEON_BLUE, 
                  border_color=NEON_BLUE, sound_manager=self.sound_manager),
            
            # Sound volume
            Button(button_x, 220, button_width, button_height, 
                  f"SOUND VOLUME: {int(self.sound_manager.volume * 100)}%", 
                  self.text_font, 
                  text_color=WHITE, hover_color=NEON_PURPLE, 
                  border_color=NEON_PURPLE, sound_manager=self.sound_manager),
            
            # Music volume
            Button(button_x, 290, button_width, button_height, 
                  f"MUSIC VOLUME: {int(self.sound_manager.music_volume * 100)}%", 
                  self.text_font, 
                  text_color=WHITE, hover_color=NEON_ORANGE, 
                  border_color=NEON_ORANGE, sound_manager=self.sound_manager),
            
            # Difficulty setting
            Button(button_x, 360, button_width, button_height, 
                  f"DIFFICULTY: {current_difficulty.upper()}", 
                  self.text_font, 
                  text_color=WHITE, hover_color=NEON_YELLOW, 
                  border_color=NEON_YELLOW, sound_manager=self.sound_manager),
            
            # Back button
            Button(button_x, 430, button_width, button_height, 
                  "BACK TO MENU", 
                  self.text_font, 
                  text_color=WHITE, hover_color=NEON_PINK, 
                  border_color=NEON_PINK, sound_manager=self.sound_manager)
        ]
    
    def get_font(self, size):
        """Get a font of specified size"""
        font_dir = os.path.join(os.path.dirname(__file__), "assets", "fonts")
        try:
            return pygame.font.Font(os.path.join(font_dir, "pixel.ttf"), size)
        except:
            return pygame.font.SysFont("Arial", size)
    
    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                return "exit"
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    return "menu"
                elif event.key == K_UP:
                    # Navigate up
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                    self.sound_manager.play("hover")
                elif event.key == K_DOWN:
                    # Navigate down
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                    self.sound_manager.play("hover")
                elif event.key == K_RETURN or event.key == K_SPACE:
                    # Select current button
                    self.sound_manager.play("click")
                    
                    # Get the selected button
                    button = self.buttons[self.selected_button]
                    
                    # Process button action based on index
                    i = self.selected_button
            
            # Check button clicks
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event):
                    if i == 0:  # Sound Effects toggle
                        # Toggle sound and update button text
                        sound_enabled = self.sound_manager.toggle_sound()
                        button.text = f"SOUND EFFECTS: {'ON' if sound_enabled else 'OFF'}"
                        button.text_surface = button.font.render(button.text, True, button.text_color)
                        button.text_rect = button.text_surface.get_rect(center=button.rect.center)
                        
                        # Debug output
                        print(f"Sound toggled in settings: {sound_enabled}")
                        
                        # Play a test sound if enabled
                        if sound_enabled:
                            print("Attempting to play test sound...")
                            # Force direct sound play for testing
                            if "click" in self.sound_manager.sounds:
                                try:
                                    self.sound_manager.sounds["click"].play()
                                    print("Test sound played directly")
                                except Exception as e:
                                    print(f"Error playing test sound: {e}")
                            else:
                                print("Click sound not found")
                        else:
                            # Make sure all sounds are stopped
                            pygame.mixer.stop()
                            print("Stopped all sounds")
                    
                    elif i == 1:  # Music toggle
                        # Toggle music and update button text
                        music_enabled = self.sound_manager.toggle_music()
                        button.text = f"MUSIC: {'ON' if music_enabled else 'OFF'}"
                        button.text_surface = button.font.render(button.text, True, button.text_color)
                        button.text_rect = button.text_surface.get_rect(center=button.rect.center)
                        
                        # Debug output
                        print(f"Music toggled in settings: {music_enabled}")
                        
                        # Play or stop music based on new state
                        if music_enabled:
                            # Try direct music control
                            try:
                                music_path = os.path.join(self.sound_manager.sound_dir, "menu_music.mp3")
                                if os.path.exists(music_path):
                                    pygame.mixer.music.load(music_path)
                                    pygame.mixer.music.set_volume(self.sound_manager.music_volume)
                                    pygame.mixer.music.play(-1)
                                    print("Music started directly")
                                else:
                                    print("Music file not found")
                            except Exception as e:
                                print(f"Error playing music: {e}")
                        else:
                            # Stop music directly
                            try:
                                pygame.mixer.music.stop()
                                print("Music stopped directly")
                            except Exception as e:
                                print(f"Error stopping music: {e}")
                    
                    elif i == 2:  # Sound volume
                        # Cycle through volume levels: 100% -> 75% -> 50% -> 25% -> 0% -> 100%
                        current_volume = self.sound_manager.volume
                        if current_volume >= 0.9:
                            new_volume = 0.75
                        elif current_volume >= 0.65:
                            new_volume = 0.5
                        elif current_volume >= 0.4:
                            new_volume = 0.25
                        elif current_volume >= 0.15:
                            new_volume = 0.0
                        else:
                            new_volume = 1.0
                        
                        # Set volume and update button text
                        self.sound_manager.set_volume(new_volume)
                        button.text = f"SOUND VOLUME: {int(self.sound_manager.volume * 100)}%"
                        button.text_surface = button.font.render(button.text, True, button.text_color)
                        button.text_rect = button.text_surface.get_rect(center=button.rect.center)
                        
                        # Note: set_volume now plays a test sound if sound is enabled
                    
                    elif i == 3:  # Music volume
                        # Cycle through volume levels: 100% -> 75% -> 50% -> 25% -> 0% -> 100%
                        current_volume = self.sound_manager.music_volume
                        if current_volume >= 0.9:
                            new_volume = 0.75
                        elif current_volume >= 0.65:
                            new_volume = 0.5
                        elif current_volume >= 0.4:
                            new_volume = 0.25
                        elif current_volume >= 0.15:
                            new_volume = 0.0
                        else:
                            new_volume = 1.0
                        
                        # Set music volume and update button text
                        self.sound_manager.set_music_volume(new_volume)
                        button.text = f"MUSIC VOLUME: {int(self.sound_manager.music_volume * 100)}%"
                        button.text_surface = button.font.render(button.text, True, button.text_color)
                        button.text_rect = button.text_surface.get_rect(center=button.rect.center)
                        
                        # If music is playing, restart it to apply the new volume immediately
                        if self.sound_manager.music_enabled and self.sound_manager.music_playing:
                            self.sound_manager.play_music("menu_music.mp3")
                    
                    elif i == 4:  # Difficulty setting
                        if self.difficulty_settings:
                            # Cycle through difficulty levels: easy -> medium -> hard -> easy
                            current = self.difficulty_settings.current_difficulty
                            if current == "easy":
                                new_difficulty = "medium"
                            elif current == "medium":
                                new_difficulty = "hard"
                            else:
                                new_difficulty = "easy"
                            
                            # Set new difficulty and update button text
                            self.difficulty_settings.set_difficulty(new_difficulty)
                            button.text = f"DIFFICULTY: {new_difficulty.upper()}"
                            button.text_surface = button.font.render(button.text, True, button.text_color)
                            button.text_rect = button.text_surface.get_rect(center=button.rect.center)
                            
                            # Play sound effect
                            self.sound_manager.play("click")
                            
                            print(f"Difficulty changed to: {new_difficulty}")
                    
                    elif i == 5:  # Back to menu
                        self.running = False
                        return "menu"
        
        return None
    
    def update(self):
        """Update screen elements"""
        dt = self.clock.get_time() / 1000.0  # Delta time in seconds
        self.animation_time += dt
        
        # Update stars
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
        
        # Update buttons
        for i, button in enumerate(self.buttons):
            # Set hover state based on selected button
            button.is_hovered = (i == self.selected_button)
            button.update(dt)
    
    def draw(self):
        """Draw the settings screen"""
        # Fill background
        self.screen.fill(BLACK)
        
        # Draw stars
        for star in self.stars:
            brightness = 100 + int(math.sin(self.animation_time * 2 + star['x']) * 50)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, 
                             (int(star['x']), int(star['y'])), 
                             int(star['size']))
        
        # Draw title
        title_text = "SETTINGS"
        title_surface = self.title_font.render(title_text, True, NEON_YELLOW)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 40))
        
        # Add glow effect to title
        for i in range(6, 0, -2):
            glow_surface = self.title_font.render(title_text, True, (*NEON_YELLOW[:3], 25 * i))
            glow_rect = glow_surface.get_rect(center=(
                title_rect.centerx + random.randint(-i, i),
                title_rect.centery + random.randint(-i, i)
            ))
            self.screen.blit(glow_surface, glow_rect)
        
        # Draw main title
        self.screen.blit(title_surface, title_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        # Draw help text
        help_text = "PRESS ENTER TO CHANGE SELECTED OPTION"
        help_surface = self.text_font.render(help_text, True, (150, 150, 150))
        help_rect = help_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(help_surface, help_rect)
        
        # Draw keyboard navigation instructions
        nav_text = "Use Arrow Keys to Navigate, ESC to Return"
        nav_surface = self.small_font.render(nav_text, True, (200, 200, 200))
        nav_rect = nav_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.screen.blit(nav_surface, nav_rect)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Run the settings screen"""
        while self.running:
            result = self.handle_events()
            if result:
                return result
                
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        return "menu"  # Default return to menu