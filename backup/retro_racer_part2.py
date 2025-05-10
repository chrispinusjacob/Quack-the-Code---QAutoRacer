# Helper functions for game objects
def create_car_sprite(color, width=40, height=60):
    """Create a simple pixel art car sprite"""
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Main body
    pygame.draw.rect(sprite, color, (5, 10, width-10, height-20))
    
    # Top part (cabin)
    pygame.draw.rect(sprite, color, (10, 5, width-20, 10))
    
    # Wheels
    wheel_color = (30, 30, 30)
    pygame.draw.rect(sprite, wheel_color, (2, 15, 6, 12))
    pygame.draw.rect(sprite, wheel_color, (width-8, 15, 6, 12))
    pygame.draw.rect(sprite, wheel_color, (2, height-27, 6, 12))
    pygame.draw.rect(sprite, wheel_color, (width-8, height-27, 6, 12))
    
    # Windshield
    pygame.draw.rect(sprite, (100, 200, 255), (12, 12, width-24, 8))
    
    # Headlights
    pygame.draw.rect(sprite, (255, 255, 200), (8, 5, 6, 4))
    pygame.draw.rect(sprite, (255, 255, 200), (width-14, 5, 6, 4))
    
    # Taillights
    pygame.draw.rect(sprite, (255, 0, 0), (8, height-9, 6, 4))
    pygame.draw.rect(sprite, (255, 0, 0), (width-14, height-9, 6, 4))
    
    return sprite

def create_orb_sprite(radius=15):
    """Create a glowing orb sprite"""
    size = radius * 2
    sprite = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Create glow effect with multiple circles
    for r in range(radius, 0, -2):
        alpha = 255 if r == radius else int(255 * (r / radius))
        color = (0, 255, 255, alpha)  # NEON_CYAN with alpha
        pygame.draw.circle(sprite, color, (radius, radius), r)
    
    return sprite

def create_road_segment(width, height):
    """Create a road segment with lane markings"""
    segment = pygame.Surface((width, height))
    segment.fill((50, 50, 50))  # Dark gray road
    
    # Add lane markings
    lane_width = width // LANE_COUNT
    for lane in range(1, LANE_COUNT):
        x = lane * lane_width
        pygame.draw.line(segment, (255, 255, 255), (x, 0), (x, height), 2)
    
    return segment

def create_stripe(width, height):
    """Create a road stripe for the sides"""
    stripe = pygame.Surface((width, height))
    stripe.fill((255, 255, 255))
    return stripe

# Game classes
class Car:
    def __init__(self, x, y, color=NEON_BLUE, is_player=False):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.color = color
        self.is_player = is_player
        self.speed = PLAYER_SPEED if is_player else INITIAL_ENEMY_SPEED
        self.sprite = create_car_sprite(color, self.width, self.height)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Animation variables
        self.frame = 0
        self.exhaust_particles = []
    
    def update(self, dt=1.0):
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Add exhaust particles for player
        if self.is_player and random.random() < 0.2:
            self.exhaust_particles.append({
                'x': self.x + self.width // 2,
                'y': self.y + self.height,
                'size': random.uniform(2, 5),
                'life': random.randint(10, 20),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(1, 2)
            })
        
        # Update exhaust particles
        new_particles = []
        for p in self.exhaust_particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1
            p['size'] *= 0.9
            
            if p['life'] > 0 and p['size'] > 0.5:
                new_particles.append(p)
        
        self.exhaust_particles = new_particles
        
        # Animation frame
        self.frame += 1
    
    def draw(self, surface):
        # Draw exhaust particles
        for p in self.exhaust_particles:
            alpha = min(255, int(p['life'] * 10))
            pygame.draw.circle(surface, (100, 100, 100, alpha), 
                             (int(p['x']), int(p['y'])), 
                             int(p['size']))
        
        # Draw car with slight animation
        y_offset = math.sin(self.frame * 0.2) * 2 if self.is_player else 0
        surface.blit(self.sprite, (self.x, self.y + y_offset))
        
        # Draw headlight glow for player
        if self.is_player:
            glow_size = 10 + math.sin(self.frame * 0.1) * 2
            glow_surf = pygame.Surface((int(glow_size*2), int(glow_size*2)), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 200, 50), (int(glow_size), int(glow_size)), int(glow_size))
            surface.blit(glow_surf, (self.x + 8 - glow_size, self.y + 5 - glow_size))
            surface.blit(glow_surf, (self.x + self.width - 8 - glow_size, self.y + 5 - glow_size))

class Orb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.sprite = create_orb_sprite(self.radius)
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius*2, self.radius*2)
        self.collected = False
        
        # Animation variables
        self.frame = random.randint(0, 100)
    
    def update(self, scroll_speed):
        self.y += scroll_speed
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius
        self.frame += 1
    
    def draw(self, surface):
        # Pulsating effect
        scale = 1.0 + math.sin(self.frame * 0.1) * 0.2
        scaled_sprite = pygame.transform.scale(
            self.sprite, 
            (int(self.radius*2*scale), int(self.radius*2*scale))
        )
        surface.blit(
            scaled_sprite, 
            (self.x - int(self.radius*scale), self.y - int(self.radius*scale))
        )