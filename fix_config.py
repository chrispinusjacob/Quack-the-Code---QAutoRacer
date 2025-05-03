import os

def fix_config():
    # Read the config.py file
    with open('config.py', 'r') as f:
        content = f.read()
    
    # Check if the key already exists
    if '"ai_track_generation"' in content and '"advanced_track_generation"' not in content:
        # Replace the key
        content = content.replace('"ai_track_generation"', '"advanced_track_generation"')
        
        # Write the updated content back to the file
        with open('config.py', 'w') as f:
            f.write(content)
        print("Fixed config.py: Replaced 'ai_track_generation' with 'advanced_track_generation'")
    elif '"advanced_track_generation"' in content:
        print("Config.py already has the correct key 'advanced_track_generation'")
    else:
        print("Could not find the key to replace in config.py")

def fix_main():
    # Read the main.py file
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Check if the key is referenced incorrectly
    if 'CONFIG["ai_track_generation"]' in content:
        # Replace the key
        content = content.replace('CONFIG["ai_track_generation"]', 'CONFIG["advanced_track_generation"]')
        
        # Write the updated content back to the file
        with open('main.py', 'w') as f:
            f.write(content)
        print("Fixed main.py: Replaced 'CONFIG[\"ai_track_generation\"]' with 'CONFIG[\"advanced_track_generation\"]'")
    else:
        print("Main.py already has the correct key reference 'CONFIG[\"advanced_track_generation\"]'")

if __name__ == "__main__":
    fix_config()
    fix_main()
    print("Fix complete. Try running the game now.")