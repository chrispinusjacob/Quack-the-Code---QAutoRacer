import pygame
import os

class SoundManager:
    """
    Fixed sound manager with proper sound control.
    """
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self._sound_enabled = True  # Use private variables with properties
        self._music_enabled = True
        self._volume = 0.7
        self._music_volume = 0.5
        
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
                self._sound_enabled = False
                self._music_enabled = False
        
        # Load sounds
        self.load_sounds()
        
        # Debug output
        print("Sound Manager initialized:")
        print(f"Sound enabled: {self._sound_enabled}")
        print(f"Music enabled: {self._music_enabled}")
        print(f"Sound volume: {self._volume}")
        print(f"Music volume: {self._music_volume}")
    
    # Properties with getters and setters
    @property
    def sound_enabled(self):
        return self._sound_enabled
    
    @sound_enabled.setter
    def sound_enabled(self, value):
        self._sound_enabled = bool(value)
        if not self._sound_enabled:
            pygame.mixer.stop()
    
    @property
    def music_enabled(self):
        return self._music_enabled
    
    @music_enabled.setter
    def music_enabled(self, value):
        self._music_enabled = bool(value)
        if not self._music_enabled and self.music_playing:
            self.stop_music()
    
    @property
    def volume(self):
        return self._volume
    
    @volume.setter
    def volume(self, value):
        self._volume = max(0.0, min(1.0, value))
        self.apply_volume()
    
    @property
    def music_volume(self):
        return self._music_volume
    
    @music_volume.setter
    def music_volume(self, value):
        self._music_volume = max(0.0, min(1.0, value))
        self.apply_music_volume()
    
    def apply_volume(self):
        """Apply current volume to all sounds"""
        for sound in self.sounds.values():
            try:
                sound.set_volume(self._volume)
            except pygame.error:
                pass
    
    def apply_music_volume(self):
        """Apply current music volume"""
        try:
            pygame.mixer.music.set_volume(self._music_volume)
        except pygame.error:
            pass
    
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
        filepath = os.path.join(self.sound_dir, filename)
        try:
            if os.path.exists(filepath):
                self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                self.sounds[sound_name].set_volume(self._volume)
                print(f"Loaded sound: {sound_name}")
            else:
                print(f"Warning: Sound file not found: {filepath}")
        except pygame.error as e:
            print(f"Warning: Could not load sound: {filepath}, Error: {e}")
    
    def play(self, sound_name, loops=0):
        """Play a sound effect"""
        if not self._sound_enabled:
            print(f"Sound disabled, not playing {sound_name}")
            return
            
        if sound_name in self.sounds:
            try:
                # Make sure volume is set correctly before playing
                self.sounds[sound_name].set_volume(self._volume)
                self.sounds[sound_name].play(loops)
                print(f"Playing sound: {sound_name}, Volume: {self._volume}")
            except pygame.error as e:
                print(f"Warning: Could not play sound: {sound_name}, Error: {e}")
        else:
            print(f"Sound not found: {sound_name}")
    
    def stop(self, sound_name):
        """Stop a specific sound"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].stop()
                print(f"Stopped sound: {sound_name}")
            except pygame.error as e:
                print(f"Warning: Could not stop sound: {sound_name}, Error: {e}")
    
    def stop_all(self):
        """Stop all sounds"""
        try:
            pygame.mixer.stop()
            print("Stopped all sounds")
        except pygame.error as e:
            print(f"Warning: Could not stop sounds, Error: {e}")
    
    def play_music(self, filename):
        """Play background music"""
        if not self._music_enabled:
            print("Music disabled, not playing")
            return
            
        filepath = os.path.join(self.sound_dir, filename)
        try:
            if os.path.exists(filepath):
                # Stop any currently playing music first
                self.stop_music()
                
                # Load and play the new music
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(self._music_volume)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.music_playing = True
                print(f"Playing music: {filename}, Volume: {self._music_volume}")
            else:
                print(f"Warning: Music file not found: {filepath}")
        except pygame.error as e:
            print(f"Warning: Could not play music: {filepath}, Error: {e}")
    
    def stop_music(self):
        """Stop background music"""
        try:
            pygame.mixer.music.stop()
            self.music_playing = False
            print("Stopped music")
        except pygame.error as e:
            print(f"Warning: Could not stop music, Error: {e}")
    
    def set_volume(self, volume):
        """Set volume for all sound effects (0.0 to 1.0)"""
        self.volume = volume
        print(f"Set sound volume to {self._volume}")
        
        # Play a test sound to demonstrate the new volume if sound is enabled
        if self._sound_enabled and "click" in self.sounds:
            try:
                self.sounds["click"].play(0)
            except pygame.error:
                pass
    
    def set_music_volume(self, volume):
        """Set volume for music (0.0 to 1.0)"""
        self.music_volume = volume
        print(f"Set music volume to {self._music_volume}")
    
    def toggle_sound(self):
        """Toggle sound effects on/off"""
        self.sound_enabled = not self._sound_enabled
        print(f"Sound toggled: {self._sound_enabled}")
        
        # If sound is disabled, stop all sound effects
        if not self._sound_enabled:
            self.stop_all()
        
        return self._sound_enabled
    
    def toggle_music(self):
        """Toggle music on/off"""
        self.music_enabled = not self._music_enabled
        print(f"Music toggled: {self._music_enabled}")
        
        if not self._music_enabled and self.music_playing:
            self.stop_music()
        
        return self._music_enabled