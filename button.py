import pygame
import math

class Button:
    """
    Interactive button class for game menus.
    """
    def __init__(self, x, y, width, height, text, font, 
                 text_color=(255, 255, 255),
                 bg_color=(0, 0, 0, 0),
                 hover_color=(100, 100, 255),
                 border_color=(255, 255, 255),
                 border_width=2,
                 sound_manager=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_width = border_width
        self.sound_manager = sound_manager
        
        self.rect = pygame.Rect(x, y, width, height)
        self.is_hovered = False
        self.was_hovered = False
        self.animation_time = 0
        
        # Pre-render text
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def update(self, dt):
        """Update button state and animation"""
        mouse_pos = pygame.mouse.get_pos()
        self.was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Play hover sound when first hovering
        if self.is_hovered and not self.was_hovered:
            if self.sound_manager:
                self.sound_manager.play("hover")
        
        # Update animation time
        self.animation_time += dt
    
    def draw(self, surface):
        """Draw the button with hover effects"""
        # Create button surface with transparency
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Determine colors based on hover state
        if self.is_hovered:
            # Pulsating effect when hovered
            pulse = math.sin(self.animation_time * 5) * 0.2 + 0.8
            hover_color = [min(255, c * pulse) for c in self.hover_color]
            
            # Draw background with hover color
            pygame.draw.rect(button_surface, (*hover_color, 200), 
                           (0, 0, self.width, self.height), 0, 10)
            
            # Draw border with stronger glow effect
            for i in range(5, 0, -1):
                alpha = 150 if i == 1 else 100
                pygame.draw.rect(button_surface, (*self.border_color, alpha),
                               (0-i, 0-i, self.width+i*2, self.height+i*2), 
                               self.border_width, 10+i)
                               
            # Draw selection indicator (arrow)
            arrow_size = 20
            pygame.draw.polygon(surface, self.hover_color, [
                (self.x - 30, self.y + self.height // 2),
                (self.x - 10, self.y + self.height // 2 - 10),
                (self.x - 10, self.y + self.height // 2 + 10)
            ])
        else:
            # Draw normal background
            pygame.draw.rect(button_surface, self.bg_color, 
                           (0, 0, self.width, self.height), 0, 10)
        
        # Always draw border
        pygame.draw.rect(button_surface, self.border_color, 
                       (0, 0, self.width, self.height), 
                       self.border_width, 10)
        
        # Blit button to surface
        surface.blit(button_surface, (self.x, self.y))
        
        # Draw text
        surface.blit(self.text_surface, self.text_rect)
    
    def is_clicked(self, event):
        """Check if button is clicked"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.sound_manager:
                    self.sound_manager.play("click")
                return True
        return False