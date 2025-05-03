import random
import math
from config import CONFIG

def ease_in_out(t):
    """Smooth easing function for transitions"""
    return t * t * (3 - 2 * t)

def smooth_array(arr, window=5):
    """Apply a moving average smoothing to an array"""
    smoothed = arr.copy()
    half_window = window // 2
    
    for i in range(half_window, len(arr) - half_window):
        smoothed[i] = sum(arr[i-half_window:i+half_window+1]) / window
        
    return smoothed

def generate_track(length=10000, player_skill=0.5):
    """
    Generate a track with varying characteristics
    
    Parameters:
    - length: Length of the track in segments
    - player_skill: 0.0 (beginner) to 1.0 (expert)
    
    Returns:
    - Dictionary with track_curvature, hills, and track_width arrays
    """
    complexity = CONFIG["track_complexity"]
    creativity = CONFIG["track_creativity"]
    theme = CONFIG["track_theme"]
    
    print(f"Track Generator: Creating a {theme} track with complexity {complexity}")
    
    # Initialize arrays
    track_curvature = [0] * length
    hills = [0] * length
    track_width = [1.0] * length
    track_sprites = [None] * length
    
    # Calculate section parameters based on complexity and player skill
    section_count = int(20 + complexity * 30)  # More sections for higher complexity
    min_section_length = max(50, int(200 - player_skill * 100))  # Shorter sections for skilled players
    max_section_length = max(100, int(300 - player_skill * 100))
    
    # Track generation parameters
    max_curve = 0.3 + (complexity * 0.7)  # Higher complexity = sharper curves
    max_hill = 0.05 + (complexity * 0.1)  # Higher complexity = steeper hills
    
    # Generate the track in sections
    pos = 0
    section_types = ["straight", "curves", "hills", "narrow", "wide", "mixed"]
    
    # Add unusual section types if creativity is high
    if creativity > 0.7:
        section_types.extend(["extreme_curves", "extreme_hills", "alternating"])
    
    while pos < length:
        # Choose a section type with weighted probability
        if random.random() < 0.2:  # 20% chance for straight sections
            section_type = "straight"
        else:
            section_type = random.choice(section_types)
        
        # Determine section length
        section_length = random.randint(min_section_length, max_section_length)
        section_length = min(section_length, length - pos)
        
        # Generate the section
        if section_type == "straight":
            # Simple straight section
            for i in range(section_length):
                if pos + i < length:
                    track_curvature[pos + i] = 0
                    hills[pos + i] = 0
                    
        elif section_type == "curves":
            # Generate a series of curves
            curve_count = random.randint(1, 3)
            sub_length = section_length // curve_count
            
            for c in range(curve_count):
                # Determine curve direction and magnitude
                curve = random.uniform(-max_curve, max_curve)
                
                for i in range(sub_length):
                    idx = pos + c * sub_length + i
                    if idx < length:
                        # Apply easing function for smooth curves
                        t = i / sub_length
                        ease = ease_in_out(t)
                        track_curvature[idx] = curve * math.sin(math.pi * ease)
                        
        elif section_type == "extreme_curves":
            # More extreme curves for high creativity
            curve_count = random.randint(2, 4)
            sub_length = section_length // curve_count
            
            for c in range(curve_count):
                # More extreme curves
                curve = random.uniform(-max_curve * 1.5, max_curve * 1.5)
                
                for i in range(sub_length):
                    idx = pos + c * sub_length + i
                    if idx < length:
                        t = i / sub_length
                        ease = ease_in_out(t)
                        # More pronounced curves
                        track_curvature[idx] = curve * math.sin(math.pi * ease)
                        
        elif section_type == "hills":
            # Generate hills
            hill_count = random.randint(1, 4)
            sub_length = section_length // hill_count
            
            for h in range(hill_count):
                hill = random.uniform(-max_hill, max_hill)
                
                for i in range(sub_length):
                    idx = pos + h * sub_length + i
                    if idx < length:
                        t = i / sub_length
                        ease = ease_in_out(t)
                        hills[idx] = hill * math.sin(math.pi * ease)
                        
        elif section_type == "extreme_hills":
            # More extreme hills
            hill_count = random.randint(2, 5)
            sub_length = section_length // hill_count
            
            for h in range(hill_count):
                hill = random.uniform(-max_hill * 1.5, max_hill * 1.5)
                
                for i in range(sub_length):
                    idx = pos + h * sub_length + i
                    if idx < length:
                        t = i / sub_length
                        ease = ease_in_out(t)
                        hills[idx] = hill * math.sin(math.pi * ease)
                        
        elif section_type == "narrow":
            # Narrow track section
            min_width = max(0.5, 0.8 - player_skill * 0.3)  # Skilled players get narrower tracks
            
            for i in range(section_length):
                idx = pos + i
                if idx < length:
                    t = i / section_length
                    ease = ease_in_out(t)
                    if i < section_length / 2:
                        track_width[idx] = 1.0 - (1.0 - min_width) * ease * 2
                    else:
                        track_width[idx] = min_width + (1.0 - min_width) * (ease - 0.5) * 2
                        
        elif section_type == "wide":
            # Wide track section
            max_width = 1.3 + creativity * 0.2  # More creative tracks can be wider
            
            for i in range(section_length):
                idx = pos + i
                if idx < length:
                    t = i / section_length
                    ease = ease_in_out(t)
                    if i < section_length / 2:
                        track_width[idx] = 1.0 + (max_width - 1.0) * ease * 2
                    else:
                        track_width[idx] = max_width - (max_width - 1.0) * (ease - 0.5) * 2
                        
        elif section_type == "mixed":
            # Combination of curves and hills
            curve = random.uniform(-max_curve * 0.8, max_curve * 0.8)
            hill = random.uniform(-max_hill * 0.8, max_hill * 0.8)
            
            for i in range(section_length):
                idx = pos + i
                if idx < length:
                    t = i / section_length
                    ease = ease_in_out(t)
                    track_curvature[idx] = curve * math.sin(math.pi * ease)
                    hills[idx] = hill * math.cos(math.pi * ease)
                    
        elif section_type == "alternating":
            # Alternating track width (challenging!)
            cycle_length = max(10, int(30 - player_skill * 15))  # Shorter cycles for skilled players
            cycles = section_length // cycle_length
            
            for c in range(cycles):
                for i in range(cycle_length):
                    idx = pos + c * cycle_length + i
                    if idx < length:
                        # Alternate between narrow and wide
                        phase = (i / cycle_length) * math.pi * 2
                        width_variation = 0.3 + creativity * 0.2
                        track_width[idx] = 1.0 + math.sin(phase) * width_variation
        
        # Add decorative sprites with theme-appropriate distribution
        sprite_chance = 0.2 + creativity * 0.2  # More creative tracks have more decorations
        
        for i in range(0, section_length, 20):  # Check every 20 segments
            if random.random() < sprite_chance:
                sprite_pos = pos + i + random.randint(0, 19)
                if sprite_pos < length:
                    side = random.choice([-1, 1])
                    
                    # Choose sprite types based on theme
                    if theme == "synthwave":
                        sprite_type = random.choice(["billboard", "building", "tree"])
                    elif theme == "cyberpunk":
                        sprite_type = random.choice(["building", "billboard", "building"])
                    elif theme == "retrowave":
                        sprite_type = random.choice(["tree", "billboard", "rock"])
                    else:
                        sprite_type = random.choice(["tree", "billboard", "rock", "building"])
                        
                    track_sprites[sprite_pos] = (sprite_type, side)
        
        # Move to next section
        pos += section_length
    
    # Apply final smoothing pass to avoid jarring transitions
    track_curvature = smooth_array(track_curvature)
    hills = smooth_array(hills)
    track_width = smooth_array(track_width)
    
    return {
        "track_curvature": track_curvature,
        "hills": hills,
        "track_width": track_width,
        "track_sprites": track_sprites
    }

def suggest_color_scheme(theme=None, time_of_day=None):
    """Suggest a color scheme based on track theme and time of day"""
    if time_of_day == "night":
        return "night"
    elif time_of_day == "sunset":
        return "retrowave"
    elif theme == "cyberpunk":
        return "cyberpunk"
    elif theme == "retrowave":
        return "retrowave"
    else:
        return "synthwave"