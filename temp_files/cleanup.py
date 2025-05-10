import os
import shutil

# List of essential files for the game
essential_files = [
    # Core game files
    "button.py",
    "difficulty_manager.py",
    "difficulty_settings.py",
    "fix_sound_manager.py",
    "fixed_sound_manager.py",
    "game_hud.py",
    "game_manager.py",
    "game_objects.py",
    "high_scores.py",
    "improved_game.py",
    "instructions.py",
    "main_menu.py",
    "settings.py",
    "settings_manager.py",
    "sound_manager.py",
    "requirements.txt",
    "run_fixed_game.bat",
    "run_with_fixed_sound.bat",
    
    # Documentation
    "README.md"
]

# Directories to keep
essential_dirs = [
    "assets"
]

# Files to clean up in assets/sounds directory
non_essential_sound_files = [
    "AWS CLOUD CLUB TUM.jpg",
    "Frame 24.jpg",
    "social media designs - instagram post.png",
    "social media designs - WhatsApp.png"
]

def cleanup_directory():
    """Remove all non-essential files from the game directory"""
    print("Starting cleanup process...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get all files in the current directory
    all_files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    
    # Create a backup directory
    backup_dir = os.path.join(current_dir, "backup")
    os.makedirs(backup_dir, exist_ok=True)
    print(f"Created backup directory: {backup_dir}")
    
    # Move non-essential files to backup
    for file in all_files:
        if file not in essential_files and not file == "cleanup.py":
            src = os.path.join(current_dir, file)
            dst = os.path.join(backup_dir, file)
            try:
                shutil.move(src, dst)
                print(f"Moved {file} to backup")
            except Exception as e:
                print(f"Error moving {file}: {e}")
    
    # Clean up non-essential files in assets/sounds
    sounds_dir = os.path.join(current_dir, "assets", "sounds")
    if os.path.exists(sounds_dir):
        for file in os.listdir(sounds_dir):
            if file in non_essential_sound_files:
                try:
                    os.remove(os.path.join(sounds_dir, file))
                    print(f"Removed {file} from assets/sounds")
                except Exception as e:
                    print(f"Error removing {file}: {e}")
    
    # Remove -p directory if it exists
    p_dir = os.path.join(current_dir, "-p")
    if os.path.exists(p_dir) and os.path.isdir(p_dir):
        try:
            shutil.rmtree(p_dir)
            print(f"Removed -p directory")
        except Exception as e:
            print(f"Error removing -p directory: {e}")
    
    print("Cleanup complete!")
    print("The game files are now organized. Only essential files remain in the main directory.")
    print("All other files have been moved to the 'backup' directory.")

if __name__ == "__main__":
    cleanup_directory()