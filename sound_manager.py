import pygame
import os

class SoundManager:
    """
    Manages game sounds and music with proper error handling.
    """
    def __init__(self):
        # Initialize with explicit boolean values
        self.sounds = {}
        self.music_playing = False
        self.sound_enabled = True  # Explicitly True
        self.music_enabled = True  # Explicitly True
        self.volume = 0.7
        self.music_volume = 0.5
        
        # Debug output
        print("Sound Manager initialized:")
        print(f"Sound enabled: {self.sound_enabled}")
        print(f"Music enabled: {self.music_enabled}")
        print(f"Sound volume: {self.volume}")
        print(f"Music volume: {self.music_volume}")
        
        # Asset paths
        self.asset_dir = os.path.join(os.path.dirname(__file__), "assets")
        self.sound_dir = os.path.join(self.asset_dir, "sounds")
        
        # Ensure directories exist
        os.makedirs(self.sound_dir, exist_ok=True)
        
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except pygame.error:
                print("Warning: Sound system initialization failed")
                self.sound_enabled = False
                self.music_enabled = False
        
        # Load sounds
        self.load_sounds()
    
    def load_sounds(self):
        """Load all game sounds with error handling"""
        sound_files = {
            "engine": "engine.mp3",
            "crash": "crash.mp3",
            "pickup": "score.mp3",
            "click": "click.mp3",
            "hover": "hover.mp3"
        }
        
        for sound_name, filename in sound_files.items():
            self.load_sound(sound_name, filename)
    
    def load_sound(self, sound_name, filename):
        """Load a single sound file with error handling"""
        if not self.sound_enabled:
            return
            
        filepath = os.path.join(self.sound_dir, filename)
        try:
            if os.path.exists(filepath):
                self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                self.sounds[sound_name].set_volume(self.volume)
            else:
                print(f"Warning: Sound file not found: {filepath}")
        except pygame.error:
            print(f"Warning: Could not load sound: {filepath}")
    
    def play(self, sound_name, loops=0):
        """Play a sound effect"""
        # Check if sound is enabled - strict check
        if self.sound_enabled is False:  # Explicit check for False
            return
            
        if sound_name in self.sounds:
            try:
                # Make sure volume is set correctly before playing
                self.sounds[sound_name].set_volume(self.volume)
                self.sounds[sound_name].play(loops)
                
                # Debug output
                print(f"Playing sound: {sound_name}, Sound enabled: {self.sound_enabled}, Volume: {self.volume}")
            except pygame.error as e:
                print(f"Warning: Could not play sound: {sound_name}, Error: {e}")
    
    def stop(self, sound_name):
        """Stop a specific sound"""
        if not self.sound_enabled:
            return
            
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].stop()
            except pygame.error:
                print(f"Warning: Could not stop sound: {sound_name}")
    
    def stop_all(self):
        """Stop all sounds"""
        if not self.sound_enabled:
            return
            
        try:
            pygame.mixer.stop()
        except pygame.error:
            print("Warning: Could not stop sounds")
    
    def play_music(self, filename):
        """Play background music"""
        if not self.music_enabled:
            return
            
        filepath = os.path.join(self.sound_dir, filename)
        try:
            if os.path.exists(filepath):
                # Stop any currently playing music first
                self.stop_music()
                
                # Load and play the new music
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.music_playing = True
            else:
                print(f"Warning: Music file not found: {filepath}")
        except pygame.error:
            print(f"Warning: Could not play music: {filepath}")
    
    def stop_music(self):
        """Stop background music"""
        if not self.music_enabled:
            return
            
        try:
            pygame.mixer.music.stop()
            self.music_playing = False
        except pygame.error:
            print("Warning: Could not stop music")
    
    def set_volume(self, volume):
        """Set volume for all sound effects (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        
        # Always set volume on sound objects, even if sound is disabled
        # This ensures volume is correct when sound is re-enabled
        for sound in self.sounds.values():
            try:
                sound.set_volume(self.volume)
            except pygame.error:
                pass
                
        # Play a test sound to demonstrate the new volume if sound is enabled
        if self.sound_enabled and "click" in self.sounds:
            try:
                self.sounds["click"].play(0)
            except pygame.error:
                pass
    
    def set_music_volume(self, volume):
        """Set volume for music (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        
        # Always set music volume, even if music is disabled
        # This ensures volume is correct when music is re-enabled
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except pygame.error:
            pass
    
    def toggle_sound(self):
        """Toggle sound effects on/off"""
        self.sound_enabled = not self.sound_enabled
        
        # If sound is disabled, stop all sound effects
        if not self.sound_enabled:
            # Stop all currently playing sounds
            pygame.mixer.stop()
            
            # Make sure engine sound is stopped specifically
            if "engine" in self.sounds:
                try:
                    self.sounds["engine"].stop()
                except pygame.error:
                    pass
        
        return self.sound_enabled
    
    def toggle_music(self):
        """Toggle music on/off"""
        self.music_enabled = not self.music_enabled
        
        if not self.music_enabled and self.music_playing:
            self.stop_music()
        
        return self.music_enabled