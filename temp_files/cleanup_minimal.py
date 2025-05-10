import os
import shutil

# List of essential files for the minimal game
essential_files = [
    # Core game files
    "button.py",
    "difficulty_manager.py",
    "difficulty_settings.py",
    "fixed_sound_manager.py",
    "game_hud.py",
    "game_objects.py",
    "high_scores.py",
    "improved_game.py",
    "instructions.py",
    "main.py",
    "main_menu.py",
    "settings.py",
    "settings_manager.py",
    "sound_manager.py",
    "requirements.txt",
    "run_consolidated.bat",
    
    # Documentation
    "README.md"
]

# Directories to keep
essential_dirs = [
    "assets"
]

def cleanup_directory():
    """Remove all non-essential files from the game directory"""
    print("Starting minimal cleanup process...")
    
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
        if file not in essential_files and not file == "cleanup_minimal.py":
            src = os.path.join(current_dir, file)
            dst = os.path.join(backup_dir, file)
            try:
                shutil.move(src, dst)
                print(f"Moved {file} to backup")
            except Exception as e:
                print(f"Error moving {file}: {e}")
    
    # Rename fixed_sound_manager.py to sound_manager.py
    try:
        fixed_sound_path = os.path.join(current_dir, "fixed_sound_manager.py")
        sound_manager_path = os.path.join(current_dir, "sound_manager.py")
        if os.path.exists(fixed_sound_path):
            # If sound_manager.py exists, back it up first
            if os.path.exists(sound_manager_path):
                backup_sound_path = os.path.join(backup_dir, "sound_manager.py")
                shutil.move(sound_manager_path, backup_sound_path)
                print(f"Backed up original sound_manager.py")
            
            # Copy fixed_sound_manager.py to sound_manager.py
            shutil.copy(fixed_sound_path, sound_manager_path)
            print(f"Copied fixed_sound_manager.py to sound_manager.py")
    except Exception as e:
        print(f"Error handling sound manager files: {e}")
    
    print("Minimal cleanup complete!")
    print("The game files are now organized with only essential files in the main directory.")
    print("All other files have been moved to the 'backup' directory.")

if __name__ == "__main__":
    cleanup_directory()