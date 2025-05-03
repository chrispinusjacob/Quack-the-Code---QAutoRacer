import random
import math
import numpy as np
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, NEON_GREEN

class AdaptiveDifficulty:
    """
    System that adjusts game difficulty based on player performance.
    """
    def __init__(self):
        self.player_metrics = {
            "avg_speed": 0,
            "collisions": 0,
            "near_misses": 0,
            "time_offroad": 0,
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


class DynamicCommentator:
    """
    Dynamic commentator that provides commentary based on player actions.
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
        if hasattr(game_state, 'drift') and abs(game_state.drift) > 0.7:
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


def draw_comment(screen, comment):
    """Draw a comment on the screen"""
    if not comment:
        return
        
    comment_font = pygame.font.SysFont("Arial", 24, bold=True)
    comment_surface = comment_font.render(comment, True, NEON_GREEN)
    comment_x = SCREEN_WIDTH // 2 - comment_surface.get_width() // 2
    comment_y = SCREEN_HEIGHT // 4
    
    # Add a background for better readability
    comment_bg = pygame.Surface((comment_surface.get_width() + 20, comment_surface.get_height() + 10), pygame.SRCALPHA)
    comment_bg.fill((0, 0, 0, 128))
    screen.blit(comment_bg, (comment_x - 10, comment_y - 5))
    screen.blit(comment_surface, (comment_x, comment_y))


def draw_hud(screen, speed, score, boost=0, damage=0, game_over=False):
    """Draw the heads-up display with game information"""
    from config import NEON_PINK, NEON_BLUE, NEON_GREEN, NEON_YELLOW, NEON_RED
    
    # Get a high-quality font
    font = pygame.font.SysFont("Arial", 24, bold=True)
    small_font = pygame.font.SysFont("Arial", 18)
    
    # Create a semi-transparent HUD background
    hud_surface = pygame.Surface((SCREEN_WIDTH, 80), pygame.SRCALPHA)
    hud_surface.fill((0, 0, 0, 128))
    screen.blit(hud_surface, (0, 0))
    
    # Speed display with animation
    speed_kmh = int(speed * 3.6)  # Convert to km/h
    speed_text = f"SPEED: {speed_kmh} KM/H"
    
    # Animate speed text color based on speed
    speed_ratio = min(1.0, speed / 300)  # Assuming max_speed is 300
    if speed_ratio > 0.8:
        # Pulse red at high speeds
        pulse = (math.sin(pygame.time.get_ticks() / 100) + 1) / 2
        speed_color = (255, int(255 * (1 - pulse)), int(255 * (1 - pulse)))
    else:
        # Gradient from green to yellow to red
        if speed_ratio < 0.5:
            # Green to yellow
            green_to_yellow = speed_ratio * 2
            speed_color = (int(255 * green_to_yellow), 255, 0)
        else:
            # Yellow to red
            yellow_to_red = (speed_ratio - 0.5) * 2
            speed_color = (255, int(255 * (1 - yellow_to_red)), 0)
    
    speed_surface = font.render(speed_text, True, speed_color)
    screen.blit(speed_surface, (20, 20))
    
    # Score display with animation for milestones
    score_int = int(score)
    score_text = f"SCORE: {score_int}"
    
    # Check for score milestone
    milestone_animation = 0
    if score_int > 0 and score_int % 1000 == 0:
        milestone_animation = math.sin(pygame.time.get_ticks() / 100) * 10
    
    score_size = 24 + int(milestone_animation)
    score_font = pygame.font.SysFont("Arial", score_size, bold=True)
    score_surface = score_font.render(score_text, True, NEON_PINK)
    screen.blit(score_surface, (20, 50))
    
    # High score display
    from config import high_score
    if score_int > high_score:
        high_score = score_int
        
    high_score_text = f"HIGH: {high_score}"
    high_score_surface = small_font.render(high_score_text, True, NEON_BLUE)
    screen.blit(high_score_surface, (200, 55))
    
    # Boost meter
    boost_width = 150
    boost_height = 15
    boost_x = SCREEN_WIDTH - boost_width - 20
    boost_y = 20
    
    # Boost background
    pygame.draw.rect(screen, (50, 50, 50), (boost_x, boost_y, boost_width, boost_height), border_radius=3)
    
    # Boost fill
    if boost > 0:
        boost_fill_width = int(boost_width * (boost / 100))
        
        # Gradient color based on boost amount
        if boost < 30:
            boost_color = NEON_RED
        elif boost < 70:
            boost_color = NEON_YELLOW
        else:
            boost_color = NEON_GREEN
            
        pygame.draw.rect(screen, boost_color, 
                       (boost_x, boost_y, boost_fill_width, boost_height), 
                       border_radius=3)
    
    # Boost text
    boost_text = "BOOST"
    boost_text_surface = small_font.render(boost_text, True, (255, 255, 255))
    screen.blit(boost_text_surface, 
               (boost_x + boost_width//2 - boost_text_surface.get_width()//2, 
                boost_y + boost_height//2 - boost_text_surface.get_height()//2))
    
    # Damage meter
    damage_width = 150
    damage_height = 15
    damage_x = SCREEN_WIDTH - damage_width - 20
    damage_y = 45
    
    # Damage background
    pygame.draw.rect(screen, (50, 50, 50), (damage_x, damage_y, damage_width, damage_height), border_radius=3)
    
    # Damage fill
    if damage > 0:
        damage_fill_width = int(damage_width * (damage / 100))
        
        # Color based on damage amount
        if damage < 30:
            damage_color = NEON_GREEN
        elif damage < 70:
            damage_color = NEON_YELLOW
        else:
            # Flashing red for critical damage
            if pygame.time.get_ticks() % 500 < 250:
                damage_color = NEON_RED
            else:
                damage_color = (150, 0, 0)
                
        pygame.draw.rect(screen, damage_color, 
                       (damage_x, damage_y, damage_fill_width, damage_height), 
                       border_radius=3)
    
    # Damage text
    damage_text = "DAMAGE"
    damage_text_surface = small_font.render(damage_text, True, (255, 255, 255))
    screen.blit(damage_text_surface, 
               (damage_x + damage_width//2 - damage_text_surface.get_width()//2, 
                damage_y + damage_height//2 - damage_text_surface.get_height()//2))
    
    # Game over message with advanced styling
    if game_over:
        # Create overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Game over text with glow effect
        font_large = pygame.font.SysFont("Arial", 72, bold=True)
        game_over_text = "GAME OVER"
        
        # Pulse effect
        pulse = (math.sin(pygame.time.get_ticks() / 300) + 1) / 2
        glow_size = int(5 + pulse * 10)
        
        # Draw glow
        for i in range(glow_size, 0, -1):
            alpha = int(200 * (1 - i / glow_size))
            glow_color = (NEON_PINK[0], NEON_PINK[1], NEON_PINK[2], alpha)
            glow_text = font_large.render(game_over_text, True, glow_color)
            screen.blit(glow_text, 
                       (SCREEN_WIDTH // 2 - glow_text.get_width() // 2 + random.randint(-i//2, i//2), 
                        SCREEN_HEIGHT // 3 - glow_text.get_height() // 2 + random.randint(-i//2, i//2)))
        
        # Main text
        main_text = font_large.render(game_over_text, True, NEON_PINK)
        screen.blit(main_text, 
                   (SCREEN_WIDTH // 2 - main_text.get_width() // 2, 
                    SCREEN_HEIGHT // 3 - main_text.get_height() // 2))
        
        # Final score
        score_font = pygame.font.SysFont("Arial", 48)
        final_score_text = f"FINAL SCORE: {score_int}"
        final_score_surface = score_font.render(final_score_text, True, NEON_GREEN)
        screen.blit(final_score_surface, 
                   (SCREEN_WIDTH // 2 - final_score_surface.get_width() // 2, 
                    SCREEN_HEIGHT // 2 - final_score_surface.get_height() // 2))
        
        # High score
        if score_int >= high_score:
            high_score_text = "NEW HIGH SCORE!"
            high_score_color = NEON_YELLOW
            
            # Animated effect for new high score
            scale = 1.0 + math.sin(pygame.time.get_ticks() / 200) * 0.1
            high_score_font = pygame.font.SysFont("Arial", int(36 * scale), bold=True)
        else:
            high_score_text = f"HIGH SCORE: {high_score}"
            high_score_color = NEON_BLUE
            high_score_font = pygame.font.SysFont("Arial", 36)
            
        high_score_surface = high_score_font.render(high_score_text, True, high_score_color)
        screen.blit(high_score_surface, 
                   (SCREEN_WIDTH // 2 - high_score_surface.get_width() // 2, 
                    SCREEN_HEIGHT // 2 + 50))
        
        # Restart text with animation
        restart_text = "Press SPACE to restart"
        restart_font = pygame.font.SysFont("Arial", 30)
        
        # Pulse animation
        pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) / 2
        restart_color = (
            int(NEON_GREEN[0] * (0.7 + 0.3 * pulse)),
            int(NEON_GREEN[1] * (0.7 + 0.3 * pulse)),
            int(NEON_GREEN[2] * (0.7 + 0.3 * pulse))
        )
        
        restart_surface = restart_font.render(restart_text, True, restart_color)
        screen.blit(restart_surface, 
                   (SCREEN_WIDTH // 2 - restart_surface.get_width() // 2, 
                    SCREEN_HEIGHT - 100))