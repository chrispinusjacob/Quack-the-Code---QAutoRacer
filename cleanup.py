import os
import shutil

# List of files to remove
files_to_remove = [
    'ai_integration.py',
    'amazon_q_integration.py',
    'aws_setup.py',
    'local_ai.py',
    'aws_builder_setup.py',
    'README_AWS_SETUP.md',
    'README_BUILDER_ID.md'
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

print("Cleanup complete!")