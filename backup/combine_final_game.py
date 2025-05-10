import os

# Combine all parts into the final game file
with open('retro_racer_complete.py', 'w') as outfile:
    # Add the first part (already has the imports and initialization)
    with open('retro_racer_complete.py', 'r') as infile:
        outfile.write(infile.read())
    
    # Add the menu drawing functions
    with open('retro_racer_complete_part2.py', 'r') as infile:
        outfile.write('\n\n')
        outfile.write(infile.read())
    
    # Add the Game class
    with open('retro_racer_complete_part3.py', 'r') as infile:
        outfile.write('\n\n')
        outfile.write(infile.read())
    
    # Add the rest of the Game class methods
    with open('retro_racer_complete_part4.py', 'r') as infile:
        outfile.write('\n\n')
        outfile.write(infile.read())

print("All game parts have been combined into retro_racer_complete.py")
print("Run the game using: python retro_racer_complete.py")