import os
import re

def search_for_text(directory, search_text):
    """Search for text in all .py files in the directory"""
    found_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if search_text.lower() in content.lower():
                            found_files.append(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return found_files

# Search for any remaining references to "retro"
print("Searching for any remaining references to 'retro'...")
retro_files = search_for_text('.', 'retro')

if retro_files:
    print(f"Found {len(retro_files)} files with 'retro' references:")
    for file in retro_files:
        print(f"  - {file}")
else:
    print("No files found with 'retro' references!")

# Search for any remaining references to "RETRO"
print("\nSearching for any remaining references to 'RETRO'...")
RETRO_files = search_for_text('.', 'RETRO')

if RETRO_files:
    print(f"Found {len(RETRO_files)} files with 'RETRO' references:")
    for file in RETRO_files:
        print(f"  - {file}")
else:
    print("No files found with 'RETRO' references!")

# Check if the footer text is correctly set in main_menu.py
if os.path.exists('main_menu.py'):
    with open('main_menu.py', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if 'footer_text = "QAutoGame © 2025"' in content:
        print("\nFooter text in main_menu.py is correctly set to 'QAutoGame © 2025'")
    else:
        print("\nWARNING: Footer text in main_menu.py might not be correctly set!")
        
        # Find the footer text line
        match = re.search(r'footer_text = "(.*?)"', content)
        if match:
            print(f"Current footer text: {match.group(1)}")
        else:
            print("Could not find footer_text line in main_menu.py")

print("\nCheck complete!")