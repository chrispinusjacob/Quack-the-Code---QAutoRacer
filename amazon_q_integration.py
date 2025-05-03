import random
import math
import numpy as np
import time
import os
import json
from config import CONFIG, COLOR_SCHEMES

class AmazonQIntegration:
    """
    Integration with Amazon Q Developer using AWS Builder ID.
    
    This uses the free tier of Amazon Q Developer, which only requires an AWS Builder ID,
    not a full AWS account or credit card.
    """
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "amazon_q_config.json")
        self.credentials = self._load_credentials()
        self.is_configured = self.credentials is not None and "builder_id" in self.credentials
        
    def _load_credentials(self):
        """Load AWS Builder ID from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading AWS Builder ID: {e}")
            return None
            
    def save_credentials(self, builder_id):
        """Save AWS Builder ID to config file"""
        credentials = {
            "builder_id": builder_id
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(credentials, f)
            self.credentials = credentials
            self.is_configured = True
            return True
        except Exception as e:
            print(f"Error saving AWS Builder ID: {e}")
            return False
            
    def get_setup_instructions(self):
        """Return instructions for setting up AWS Builder ID"""
        return """
        To set up your AWS Builder ID for QAutoRacer:
        
        1. Create an AWS Builder ID at https://profile.aws.amazon.com/
        2. Enter your Builder ID in the game's setup screen
        
        That's it! No AWS account or credit card required.
        
        The Amazon Q Developer free tier includes:
        - 2 million tokens per month
        - Access to all AI features in the game
        """


class AITrackGenerator:
    """
    AI-powered track generator that creates interesting and balanced tracks
    based on player skill level and preferences.
    
    This simulates what would be done with Amazon Q Developer in a real implementation.
    """
    def __init__(self):
        self.complexity = CONFIG["track_complexity"]
        self.creativity = CONFIG["track_creativity"]
        self.theme = CONFIG["track_theme"]
        
    def generate_track(self, length=10000, player_skill=0.5):
        """
        Generate a track with the specified parameters
        
        Parameters:
        - length: Length of the track in segments
        - player_skill: 0.0 (beginner) to 1.0 (expert)
        
        Returns:
        - Dictionary with track_curvature, hills, and track_width arrays
        """
        print(f"AI Track Generator: Creating a {self.theme} track with complexity {self.complexity}")
        
        # Initialize arrays
        track_curvature = [0] * length
        hills = [0] * length
        track_width = [1.0] * length
        track_sprites = [None] * length
        
        # Use "AI" to determine track characteristics based on parameters
        # In a real implementation, this would call Amazon Q Developer
        
        # Calculate section parameters based on complexity and player skill
        section_count = int(20 + self.complexity * 30)  # More sections for higher complexity
        min_section_length = max(50, int(200 - player_skill * 100))  # Shorter sections for skilled players
        max_section_length = max(100, int(300 - player_skill * 100))
        
        # Track generation parameters
        max_curve = 0.3 + (self.complexity * 0.7)  # Higher complexity = sharper curves
        max_hill = 0.05 + (self.complexity * 0.1)  # Higher complexity = steeper hills
        
        # Creativity affects how much randomness and unusual features appear
        unusual_sections = int(self.creativity * 10)  # Number of unusual sections
        
        # Generate the track in sections
        pos = 0
        section_types = ["straight", "curves", "hills", "narrow", "wide", "mixed"]
        
        # Add unusual section types if creativity is high
        if self.creativity > 0.7:
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
                            ease = t * t * (3 - 2 * t)  # Ease in-out
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
                            ease = t * t * (3 - 2 * t)
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
                            ease = t * t * (3 - 2 * t)
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
                            ease = t * t * (3 - 2 * t)
                            hills[idx] = hill * math.sin(math.pi * ease)
                            
            elif section_type == "narrow":
                # Narrow track section
                min_width = max(0.5, 0.8 - player_skill * 0.3)  # Skilled players get narrower tracks
                
                for i in range(section_length):
                    idx = pos + i
                    if idx < length:
                        t = i / section_length
                        ease = t * t * (3 - 2 * t)
                        if i < section_length / 2:
                            track_width[idx] = 1.0 - (1.0 - min_width) * ease * 2
                        else:
                            track_width[idx] = min_width + (1.0 - min_width) * (ease - 0.5) * 2
                            
            elif section_type == "wide":
                # Wide track section
                max_width = 1.3 + self.creativity * 0.2  # More creative tracks can be wider
                
                for i in range(section_length):
                    idx = pos + i
                    if idx < length:
                        t = i / section_length
                        ease = t * t * (3 - 2 * t)
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
                        ease = t * t * (3 - 2 * t)
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
                            width_variation = 0.3 + self.creativity * 0.2
                            track_width[idx] = 1.0 + math.sin(phase) * width_variation
            
            # Add decorative sprites with theme-appropriate distribution
            sprite_chance = 0.2 + self.creativity * 0.2  # More creative tracks have more decorations
            
            for i in range(0, section_length, 20):  # Check every 20 segments
                if random.random() < sprite_chance:
                    sprite_pos = pos + i + random.randint(0, 19)
                    if sprite_pos < length:
                        side = random.choice([-1, 1])
                        
                        # Choose sprite types based on theme
                        if self.theme == "synthwave":
                            sprite_type = random.choice(["billboard", "building", "tree"])
                        elif self.theme == "cyberpunk":
                            sprite_type = random.choice(["building", "billboard", "building"])
                        elif self.theme == "retrowave":
                            sprite_type = random.choice(["tree", "billboard", "rock"])
                        else:
                            sprite_type = random.choice(["tree", "billboard", "rock", "building"])
                            
                        track_sprites[sprite_pos] = (sprite_type, side)
            
            # Move to next section
            pos += section_length
        
        # Apply final smoothing pass to avoid jarring transitions
        track_curvature = self._smooth_array(track_curvature)
        hills = self._smooth_array(hills)
        track_width = self._smooth_array(track_width)
        
        return {
            "track_curvature": track_curvature,
            "hills": hills,
            "track_width": track_width,
            "track_sprites": track_sprites
        }
    
    def _smooth_array(self, arr, window=5):
        """Apply a moving average smoothing to an array"""
        smoothed = arr.copy()
        half_window = window // 2
        
        for i in range(half_window, len(arr) - half_window):
            smoothed[i] = sum(arr[i-half_window:i+half_window+1]) / window
            
        return smoothed
    
    def suggest_color_scheme(self, time_of_day=None):
        """Suggest a color scheme based on track theme and time of day"""
        # In a real implementation, this would use Amazon Q to generate a custom color scheme
        
        if time_of_day == "night":
            return "night"
        elif time_of_day == "sunset":
            return "retrowave"
        elif self.theme == "cyberpunk":
            return "cyberpunk"
        elif self.theme == "retrowave":
            return "retrowave"
        else:
            return "synthwave"


class AdaptiveDifficulty:
    """
    AI-powered system that adjusts game difficulty based on player performance.
    
    This simulates what would be done with Amazon Q Developer in a real implementation.
    """
    def __init__(self):
        self.player_metrics = {
            "avg_speed": 0,
            "collisions": 0,
            "near_misses": 0,
            "time_offroad": 0,
            "reaction_time": 0,
            "segment_times": []
        }
        self.difficulty_level = 0.5  # Start at medium difficulty
        self.adaptation_rate = 0.05  # How quickly difficulty changes
        self.last_update_time = 0
        self.update_interval = 5000  # Update every 5 seconds
        
    def update_metrics(self, game_state, dt):
        """Update player performance metrics"""
        # Update average speed
        self.player_metrics["avg_speed"] = (self.player_metrics["avg_speed"] * 0.95 + 
                                           game_state.speed * 0.05)
        
        # Track time spent offroad
        if game_state.offroad:
            self.player_metrics["time_offroad"] += dt
        
        # Store segment completion time
        if len(self.player_metrics["segment_times"]) > 20:
            self.player_metrics["segment_times"].pop(0)
        
        # Add current segment time
        if game_state.speed > 0:
            segment_time = 1000 / game_state.speed  # Time to complete a segment
            self.player_metrics["segment_times"].append(segment_time)
    
    def record_collision(self):
        """Record a collision event"""
        self.player_metrics["collisions"] += 1
    
    def record_near_miss(self):
        """Record a near miss event"""
        self.player_metrics["near_misses"] += 1
    
    def adjust_difficulty(self, current_time):
        """
        Analyze player metrics and adjust difficulty
        Returns updated game parameters if difficulty should change
        """
        # Only update at certain intervals
        if current_time - self.last_update_time < self.update_interval:
            return None
            
        self.last_update_time = current_time
        
        # Calculate player skill based on metrics
        skill_score = self._calculate_skill_score()
        
        # Adjust difficulty to be slightly above player skill
        target_difficulty = min(1.0, skill_score + 0.1)
        
        # Gradually move toward target difficulty
        if abs(self.difficulty_level - target_difficulty) > 0.05:
            if self.difficulty_level < target_difficulty:
                self.difficulty_level += self.adaptation_rate
            else:
                self.difficulty_level -= self.adaptation_rate
                
            self.difficulty_level = max(0.1, min(1.0, self.difficulty_level))
            
            # Return updated game parameters
            return {
                "max_obstacles": int(20 + self.difficulty_level * 20),
                "obstacle_spacing": int(1000 - self.difficulty_level * 500),
                "track_complexity": self.difficulty_level,
                "track_width_multiplier": 1.0 - self.difficulty_level * 0.3
            }
        
        return None
    
    def _calculate_skill_score(self):
        """Calculate a skill score from 0.0 to 1.0 based on player metrics"""
        # Speed score (0.0 to 1.0)
        max_speed = 300  # Maximum possible speed
        speed_score = min(1.0, self.player_metrics["avg_speed"] / max_speed)
        
        # Collision penalty
        collision_penalty = min(0.5, self.player_metrics["collisions"] * 0.1)
        
        # Near miss bonus
        near_miss_bonus = min(0.2, self.player_metrics["near_misses"] * 0.02)
        
        # Offroad penalty
        offroad_penalty = min(0.3, self.player_metrics["time_offroad"] / 1000 * 0.05)
        
        # Reaction time score based on segment times consistency
        reaction_score = 0.5  # Default
        if len(self.player_metrics["segment_times"]) > 5:
            # Lower variance = better reaction time
            variance = np.var(self.player_metrics["segment_times"])
            reaction_score = max(0.0, min(1.0, 1.0 - variance / 1000))
        
        # Calculate final skill score
        skill_score = (speed_score * 0.4 + 
                      reaction_score * 0.3 + 
                      near_miss_bonus - 
                      collision_penalty - 
                      offroad_penalty)
        
        return max(0.1, min(1.0, skill_score))


class AICommentator:
    """
    AI-powered commentator that provides dynamic commentary based on player actions.
    
    This simulates what would be done with Amazon Q Developer in a real implementation.
    """
    def __init__(self):
        self.comment_cooldown = 0
        self.last_event = None
        self.event_history = []
        self.comment_templates = {
            "near_miss": [
                "Close call!",
                "That was close!",
                "Threading the needle!",
                "Precision driving!"
            ],
            "high_speed": [
                "You're flying!",
                "Speed demon!",
                "Burning rubber!",
                "Maximum velocity!"
            ],
            "drift": [
                "Nice drift!",
                "Smooth sliding!",
                "Perfect drift!",
                "Sliding with style!"
            ],
            "offroad": [
                "Off the beaten path!",
                "Taking a shortcut?",
                "Watch the grass!",
                "Back to the road!"
            ],
            "recovery": [
                "Great recovery!",
                "Back in control!",
                "Regaining control!",
                "Back on track!"
            ],
            "obstacle_streak": [
                "Obstacle master!",
                "Weaving through traffic!",
                "Slalom champion!",
                "Dodging like a pro!"
            ],
            "top_speed": [
                "Maximum overdrive!",
                "Breaking the sound barrier!",
                "Hyperspeed engaged!",
                "Ludicrous speed!"
            ],
            "track_feature": [
                "Sharp curve ahead!",
                "Narrow section coming up!",
                "Hill climb incoming!",
                "Watch for that dip!"
            ]
        }
        
    def detect_events(self, game_state, dt):
        """Detect noteworthy events based on game state"""
        events = []
        
        # High speed event
        if game_state.speed > game_state.max_speed * 0.9:
            events.append("high_speed")
            
        # Top speed event
        if game_state.speed > game_state.max_speed * 0.98:
            events.append("top_speed")
            
        # Drift event
        if abs(game_state.drift) > 0.7:
            events.append("drift")
            
        # Offroad event
        if game_state.offroad:
            events.append("offroad")
            
        # Recovery event (was offroad, now back on road)
        if len(self.event_history) > 0 and self.event_history[-1] == "offroad" and not game_state.offroad:
            events.append("recovery")
            
        # Track feature event
        segment = int(game_state.position / 200) % len(game_state.track_curvature)
        
        # Sharp curve
        if abs(game_state.track_curvature[segment]) > 0.6:
            events.append("track_feature")
            
        # Update event history
        if events:
            self.event_history.append(events[0])
            if len(self.event_history) > 10:
                self.event_history.pop(0)
                
        return events
        
    def generate_comment(self, event_type, game_state=None):
        """Generate a contextual comment based on the event type"""
        # In a real implementation, this would use Amazon Q to generate dynamic commentary
        
        if event_type in self.comment_templates:
            comments = self.comment_templates[event_type]
            
            # Choose a comment, avoiding the last one if possible
            if len(comments) > 1 and self.last_event == event_type:
                # Filter out the last comment used for this event type
                filtered_comments = [c for c in comments if c != self.last_event]
                comment = random.choice(filtered_comments)
            else:
                comment = random.choice(comments)
                
            self.last_event = event_type
            return comment
            
        return None
        
    def update(self, game_state, dt):
        """Update the commentator and potentially generate a new comment"""
        if self.comment_cooldown > 0:
            self.comment_cooldown -= dt
            return None
            
        # Detect events
        events = self.detect_events(game_state, dt)
        
        if events:
            # Choose the most interesting event
            event_priorities = {
                "top_speed": 5,
                "near_miss": 4,
                "recovery": 3,
                "drift": 2,
                "high_speed": 1,
                "offroad": 1,
                "track_feature": 1,
                "obstacle_streak": 2
            }
            
            # Sort events by priority
            events.sort(key=lambda e: event_priorities.get(e, 0), reverse=True)
            
            # Generate comment for highest priority event
            comment = self.generate_comment(events[0], game_state)
            
            if comment:
                # Set cooldown based on comment length
                self.comment_cooldown = 1000 + len(comment) * 50
                return comment
                
        return None