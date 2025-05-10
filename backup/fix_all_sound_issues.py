import os
import re

def fix_game_class():
    with open('game_class.py', 'r') as f:
        content = f.read()
    
    # Fix sound manager references
    content = content.replace('sound_manager.sound_manager.stop_all_sounds()', 'sound_manager.stop_all_sounds()')
    
    # Fix direct sound references
    content = content.replace('self.engine_sound.play(-1)', 'sound_manager.play_engine_sound()')
    content = content.replace('self.engine_sound.stop()', 'sound_manager.stop_engine_sound()')
    content = content.replace('self.crash_sound.play()', 'sound_manager.play_sound("crash")')
    content = content.replace('self.pickup_sound.play()', 'sound_manager.play_sound("pickup")')
    
    # Fix menu music references
    content = content.replace('self.main_menu.menu_music.play(-1)', 'sound_manager.play_menu_music()')
    
    with open('game_class.py', 'w') as f:
        f.write(content)
    
    print('Fixed all sound references in game_class.py')

def main():
    fix_game_class()
    print('All sound issues fixed. Please run the game to test.')

if __name__ == "__main__":
    main()