import os
import json

class SettingsManager:
    """
    Manages game settings persistence between sessions.
    Saves and loads settings to/from a JSON file.
    """
    def __init__(self):
        self.settings_file = "game_settings.json"
        self.default_settings = {
            "sound_enabled": True,
            "music_enabled": True,
            "sound_volume": 0.7,
            "music_volume": 0.5
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file or use defaults if file doesn't exist"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as f:
                    settings = json.load(f)
                return settings
            else:
                return self.default_settings.copy()
        except (json.JSONDecodeError, IOError):
            print("Warning: Could not load settings file. Using defaults.")
            return self.default_settings.copy()
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f)
        except IOError:
            print("Warning: Could not save settings file.")
    
    def get_setting(self, key):
        """Get a specific setting value"""
        return self.settings.get(key, self.default_settings.get(key))
    
    def set_setting(self, key, value):
        """Set a specific setting value and save to file"""
        if key in self.default_settings:
            self.settings[key] = value
            self.save_settings()
    
    def apply_settings_to_sound_manager(self, sound_manager):
        """Apply loaded settings to the sound manager"""
        # First set volumes, then enable/disable sound
        sound_manager.set_volume(self.get_setting("sound_volume"))
        sound_manager.set_music_volume(self.get_setting("music_volume"))
        
        # Now set enabled states
        # Use direct property access if available
        if hasattr(sound_manager, "_sound_enabled"):
            sound_manager._sound_enabled = self.get_setting("sound_enabled")
        else:
            sound_manager.sound_enabled = self.get_setting("sound_enabled")
            
        if hasattr(sound_manager, "_music_enabled"):
            sound_manager._music_enabled = self.get_setting("music_enabled")
        else:
            sound_manager.music_enabled = self.get_setting("music_enabled")
            
        # Print debug info
        print(f"Applied settings: sound={sound_manager.sound_enabled}, music={sound_manager.music_enabled}, " +
              f"sound_vol={sound_manager.volume}, music_vol={sound_manager.music_volume}")
    
    def update_from_sound_manager(self, sound_manager):
        """Update settings from current sound manager state"""
        self.set_setting("sound_enabled", sound_manager.sound_enabled)
        self.set_setting("music_enabled", sound_manager.music_enabled)
        self.set_setting("sound_volume", sound_manager.volume)
        self.set_setting("music_volume", sound_manager.music_volume)
        self.save_settings()