import os

# Combine all parts into final_game.py
with open('final_game.py', 'w') as outfile:
    # First part (initialization, classes, etc.)
    with open('final_game.py', 'r') as infile:
        outfile.write(infile.read())
    
    # Add all other parts
    for i in range(2, 8):
        part_file = f'final_game_part{i}.py'
        if os.path.exists(part_file):
            with open(part_file, 'r') as infile:
                outfile.write('\n\n')
                outfile.write(infile.read())

print("All game files have been combined into final_game.py")
print("Run the game using: python run_final_game.py")