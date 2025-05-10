import pygame

def stop_all_sounds():
    """Stop all currently playing sounds in pygame mixer"""
    pygame.mixer.stop()  # This stops all channels
    
    # Alternative approach to stop individual sounds
    # for i in range(pygame.mixer.get_num_channels()):
    #     pygame.mixer.Channel(i).stop()