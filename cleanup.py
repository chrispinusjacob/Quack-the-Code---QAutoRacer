import os
import shutil

# List of files to remove
files_to_remove = [
    'car.py',
    'fix_config.py',
    'game_features.py',
    'main.py',  # We'll use simple_main.py instead
    'sprites.py',
    'test.py',
    'test_imports.py',
    'track.py',
    'track_generator.py',
    'utils.py'
]

# Remove files
for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
        print(f"Removed {file}")

# Remove __pycache__ directory
if os.path.exists('__pycache__'):
    shutil.rmtree('__pycache__')
    print("Removed __pycache__ directory")

# Rename simple_main.py to main.py
if os.path.exists('simple_main.py'):
    if os.path.exists('main.py'):
        os.remove('main.py')
    os.rename('simple_main.py', 'main.py')
    print("Renamed simple_main.py to main.py")

print("Cleanup complete!")