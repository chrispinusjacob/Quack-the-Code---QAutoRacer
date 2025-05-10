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