import os
import shutil

def cleanup_directory():
    """Remove all files except QAutoGame.py and essential assets"""
    print("Starting final cleanup process...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Essential files to keep
    essential_files = [
        "QAutoGame.py",
        "run_qauto_game.bat",
        "README.md",
        "requirements.txt",
        "cleanup_final.py"
    ]
    
    # Create a backup directory if it doesn't exist
    backup_dir = os.path.join(current_dir, "backup")
    os.makedirs(backup_dir, exist_ok=True)
    
    # Move all non-essential files to backup
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        
        # Skip directories except for backup
        if os.path.isdir(item_path) and item != "backup" and item != "assets":
            try:
                shutil.move(item_path, os.path.join(backup_dir, item))
                print(f"Moved directory {item} to backup")
            except Exception as e:
                print(f"Error moving directory {item}: {e}")
        
        # Move files except essential ones
        elif os.path.isfile(item_path) and item not in essential_files:
            try:
                shutil.move(item_path, os.path.join(backup_dir, item))
                print(f"Moved file {item} to backup")
            except Exception as e:
                print(f"Error moving file {item}: {e}")
    
    print("Final cleanup complete!")
    print("Your game directory now contains only QAutoGame.py, run_qauto_game.bat, and essential assets.")

if __name__ == "__main__":
    # Ask for confirmation
    confirm = input("This will move all files except QAutoGame.py, run_qauto_game.bat, and assets to the backup folder. Continue? (y/n): ")
    if confirm.lower() == 'y':
        cleanup_directory()
    else:
        print("Cleanup cancelled.")