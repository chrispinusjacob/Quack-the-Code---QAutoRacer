import os

# Combine all parts into the final game file
with open('retro_racer_complete.py', 'w') as outfile:
    # Add all parts in order
    for i in range(1, 9):
        part_file = f'retro_racer_part{i}.py' if i > 1 else 'retro_racer_complete.py'
        if os.path.exists(part_file):
            with open(part_file, 'r') as infile:
                content = infile.read()
                if i > 1:  # For parts after the first one
                    # Remove any imports or other duplicate code
                    if "import " in content or "from " in content:
                        lines = content.split('\n')
                        filtered_lines = [line for line in lines if not (line.startswith('import ') or line.startswith('from '))]
                        content = '\n'.join(filtered_lines)
                outfile.write(content)
                if i < 8:  # Don't add newline after the last part
                    outfile.write('\n\n')

print("All game parts have been combined into retro_racer_complete.py")
print("Run the game using: python retro_racer_complete.py")