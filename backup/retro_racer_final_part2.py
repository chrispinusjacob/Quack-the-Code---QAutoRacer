# Simple Button class
class SimpleButton:
    def __init__(self, x, y, width, height, text, color=NEON_BLUE, hover_color=NEON_PINK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface, font):
        # Draw button with hover effect
        color = self.hover_color if self.is_hovered else self.color
        
        # Main button
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=5)  # Border
        
        # Button text
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos):
        # Check if hover state changed
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        # Check if button was clicked
        return self.rect.collidepoint(mouse_pos) and mouse_click

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