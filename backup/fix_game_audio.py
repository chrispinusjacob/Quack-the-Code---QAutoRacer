import pygame
import os
import sys

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Define the sound manager class
class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music = None
        
    def load_sounds(self, sound_dir):
        try:
            # Load game sounds
            self.sounds["engine"] = self._load_sound(sound_dir, "engine.mp3")
            self.sounds["crash"] = self._load_sound(sound_dir, "crash.mp3")
            self.sounds["pickup"] = self._load_sound(sound_dir, "score.mp3")
            self.sounds["click"] = self._load_sound(sound_dir, "click.wav")
            self.sounds["hover"] = self._load_sound(sound_dir, "hover.wav")
            
            # Load menu music
            self.music = self._load_sound(sound_dir, "menu_music.wav")
            
            # Set volumes
            if self.music:
                self.music.set_volume(0.5)
            
            if "engine" in self.sounds:
                self.sounds["engine"].set_volume(0.4)
            if "crash" in self.sounds:
                self.sounds["crash"].set_volume(0.7)
            if "pickup" in self.sounds:
                self.sounds["pickup"].set_volume(0.5)
                
            return True
        except Exception as e:
            print(f"Error loading sounds: {e}")
            return False
    
    def _load_sound(self, sound_dir, filename):
        try:
            path = os.path.join(sound_dir, filename)
            if os.path.exists(path):
                return pygame.mixer.Sound(path)
        except Exception as e:
            print(f"Could not load {filename}: {e}")
        
        # Create empty sound if loading fails
        return pygame.mixer.Sound(buffer=bytes([0]*44))
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_music(self):
        if self.music:
            self.music.play(-1)
    
    def stop_all(self):
        pygame.mixer.stop()

# Function to modify the game_class.py file
def update_game_class():
    filename = "c:\\Users\\ADMIN\\Desktop\\QAutoGame\\game_class.py"
    
    with open(filename, 'r') as file:
        content = file.read()
    
    # Add import for sound manager
    if "from sound_manager import sound_manager" not in content:
        content = content.replace(
            "from stop_all_sounds import stop_all_sounds",
            "from sound_manager import sound_manager"
        )
    
    # Replace all stop_all_sounds() calls with sound_manager.stop_all_sounds()
    content = content.replace("stop_all_sounds()", "sound_manager.stop_all_sounds()")
    
    # Replace engine sound play calls
    content = content.replace(
        "self.engine_sound.play(-1)",
        "sound_manager.play_engine_sound()"
    )
    
    # Replace engine sound stop calls
    content = content.replace(
        "self.engine_sound.stop()",
        "sound_manager.stop_engine_sound()"
    )
    
    # Write the modified content back to the file
    with open(filename, 'w') as file:
        file.write(content)
    
    print("Successfully updated game_class.py")

# Create the sound_manager.py file
def create_sound_manager():
    filename = "c:\\Users\\ADMIN\\Desktop\\QAutoGame\\sound_manager.py"
    
    content = """import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music = None
        self.sound_enabled = True
        self.music_enabled = True
    
    def load_sounds(self, sound_dir):
        try:
            # Load game sounds
            self.sounds["engine"] = self._load_sound(sound_dir, "engine.mp3")
            self.sounds["crash"] = self._load_sound(sound_dir, "crash.mp3")
            self.sounds["pickup"] = self._load_sound(sound_dir, "score.mp3")
            
            # Load menu music
            try:
                self.music = self._load_sound(sound_dir, "menu_music.mp3")
            except:
                try:
                    self.music = self._load_sound(sound_dir, "menu_music.wav")
                except:
                    print("Could not load menu music")
            
            # Set volumes
            if self.music:
                self.music.set_volume(0.5)
            
            if "engine" in self.sounds:
                self.sounds["engine"].set_volume(0.4)
            if "crash" in self.sounds:
                self.sounds["crash"].set_volume(0.7)
            if "pickup" in self.sounds:
                self.sounds["pickup"].set_volume(0.5)
                
            print("Sound manager: All sounds loaded")
            return True
        except Exception as e:
            print(f"Sound manager: Error loading sounds: {e}")
            return False
    
    def _load_sound(self, sound_dir, filename):
        try:
            path = os.path.join(sound_dir, filename)
            if os.path.exists(path):
                return pygame.mixer.Sound(path)
        except Exception as e:
            print(f"Sound manager: Could not load {filename}: {e}")
        
        # Create empty sound if loading fails
        return pygame.mixer.Sound(buffer=bytes([0]*44))
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds and self.sound_enabled:
            self.sounds[sound_name].play()
    
    def play_engine_sound(self):
        if "engine" in self.sounds and self.sound_enabled:
            self.sounds["engine"].play(-1)
    
    def stop_engine_sound(self):
        if "engine" in self.sounds:
            self.sounds["engine"].stop()
    
    def play_menu_music(self):
        if self.music and self.music_enabled:
            self.music.play(-1)
    
    def stop_all_sounds(self):
        pygame.mixer.stop()
        print("Sound manager: Stopped all sounds")
    
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        if not self.sound_enabled:
            # Stop all sound effects
            for name, sound in self.sounds.items():
                sound.stop()
        return self.sound_enabled
    
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if not self.music_enabled and self.music:
            self.music.stop()
        elif self.music_enabled and self.music:
            self.music.play(-1)
        return self.music_enabled

# Create a global instance
sound_manager = SoundManager()
"""
    
    with open(filename, 'w') as file:
        file.write(content)
    
    print("Successfully created sound_manager.py")

# Main function
def main():
    create_sound_manager()
    update_game_class()
    print("Audio fix completed. Please run the game to test.")

if __name__ == "__main__":
    main()