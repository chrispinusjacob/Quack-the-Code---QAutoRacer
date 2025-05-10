import os
import re

print("Searching for and removing ALL references to 'Retro' and 'RETRO'...")

# List of files to check
files_to_check = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py') or file.endswith('.bat'):
            files_to_check.append(os.path.join(root, file))

# Patterns to search for
patterns = [
    r'QAutoGame INC\.', 
    r'QAutoGame Inc\.', 
    r'QAutoGame © 2025',
    r'QAutoGame © 2025',
    r'QAutoGame',
    r'QAutoGame',
    r'QAutoGame',
    r'QAutoGame',
    r'QAutoGame',
    r'QAutoGame',
    r'QAutoGame Experience',
    r'QAutoGame Experience'
]

# Count of replacements made
total_replacements = 0

# Process each file
for filename in files_to_check:
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        # Check for each pattern
        for pattern in patterns:
            if re.search(pattern, content):
                if 'QAutoGame INC' in pattern or 'QAutoGame Inc' in pattern:
                    content = re.sub(pattern, 'QAutoGame © 2025', content)
                elif 'QAutoGame' in pattern or 'QAutoGame' in pattern:
                    content = re.sub(pattern, 'QAutoGame', content)
                elif 'QAutoGame Experience' in pattern or 'QAutoGame Experience' in pattern:
                    content = re.sub(pattern, 'QAutoGame Experience', content)
                elif 'QAutoGame' in pattern or 'QAutoGame' in pattern:
                    content = re.sub(pattern, 'QAutoGame', content)
                elif 'QAutoGame' in pattern or 'QAutoGame' in pattern:
                    content = re.sub(pattern, 'QAutoGame', content)
                else:
                    content = re.sub(pattern, 'QAutoGame © 2025', content)
        
        # Check if content was modified
        if content != original_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            replacements = len(original_content) - len(content)
            total_replacements += replacements
            print(f"Updated {filename}")
    
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print(f"Completed! Made changes to remove all 'Retro' references.")

# Specifically check main_menu.py for the footer text
if os.path.exists('main_menu.py'):
    with open('main_menu.py', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Look for the footer text drawing code
    if 'footer_text =' in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'footer_text =' in line:
                lines[i] = '        footer_text = "QAutoGame © 2025"'
                print("Fixed footer text in main_menu.py")
        
        with open('main_menu.py', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

print("All references to 'Retro' should now be removed!")