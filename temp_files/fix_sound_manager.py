import pygame
import os

def fix_sound_paths():
    """
    Ensures sound files exist and are properly formatted.
    Creates placeholder files if needed.
    """
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Define asset directories
    ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
    SOUND_DIR = os.path.join(ASSET_DIR, "sounds")
    
    # Ensure directories exist
    os.makedirs(SOUND_DIR, exist_ok=True)
    
    # Define required sound files
    required_sounds = {
        "engine.mp3": "Engine sound",
        "crash.mp3": "Crash sound",
        "score.mp3": "Score/pickup sound"
    }
    
    missing_files = []
    
    # Check for missing files
    for filename, description in required_sounds.items():
        filepath = os.path.join(SOUND_DIR, filename)
        if not os.path.exists(filepath):
            missing_files.append((filename, description))
    
    if missing_files:
        print("The following sound files are missing:")
        for filename, description in missing_files:
            print(f"- {filename}: {description}")
        
        # Create simple placeholder sounds
        print("Creating placeholder sound files...")
        
        # Create a simple sound array
        duration = 0.5  # seconds
        sample_rate = 44100
        num_samples = int(duration * sample_rate)
        
        # Create a simple beep sound for engine
        if ("engine.mp3", "Engine sound") in missing_files:
            try:
                import numpy as np
                # Create a simple engine sound (low frequency)
                t = np.linspace(0, duration, num_samples, False)
                engine_tone = np.sin(2 * np.pi * 220 * t) * 0.3
                engine_sound = pygame.sndarray.make_sound((engine_tone * 32767).astype(np.int16))
                pygame.mixer.Sound.save(engine_sound, os.path.join(SOUND_DIR, "engine.mp3"))
                print("Created engine.mp3")
            except ImportError:
                print("Could not create engine.mp3 - numpy not available")
        
        # Create a simple crash sound
        if ("crash.mp3", "Crash sound") in missing_files:
            try:
                import numpy as np
                # Create a simple crash sound (noise)
                crash_tone = np.random.rand(num_samples) * 2 - 1
                crash_sound = pygame.sndarray.make_sound((crash_tone * 32767).astype(np.int16))
                pygame.mixer.Sound.save(crash_sound, os.path.join(SOUND_DIR, "crash.mp3"))
                print("Created crash.mp3")
            except ImportError:
                print("Could not create crash.mp3 - numpy not available")
        
        # Create a simple pickup sound
        if ("score.mp3", "Score/pickup sound") in missing_files:
            try:
                import numpy as np
                # Create a simple pickup sound (high frequency)
                t = np.linspace(0, duration, num_samples, False)
                pickup_tone = np.sin(2 * np.pi * 880 * t) * 0.3
                pickup_sound = pygame.sndarray.make_sound((pickup_tone * 32767).astype(np.int16))
                pygame.mixer.Sound.save(pickup_sound, os.path.join(SOUND_DIR, "score.mp3"))
                print("Created score.mp3")
            except ImportError:
                print("Could not create score.mp3 - numpy not available")
    
    else:
        print("All sound files are present.")
    
    print("Sound system check complete.")

if __name__ == "__main__":
    pygame.init()
    fix_sound_paths()
    pygame.quit()