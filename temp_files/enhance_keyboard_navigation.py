import os

print("Enhancing keyboard navigation visibility...")

# First, update the button.py file to make the hover effect more visible
print("\nUpdating button.py to enhance hover effect...")
with open("button.py", "r") as f:
    button_content = f.read()

# Enhance the hover effect in the draw method
if "def draw(self, surface):" in button_content:
    # Find the draw method
    draw_start = button_content.find("def draw(self, surface):")
    draw_end = button_content.find("def is_clicked(self, event):", draw_start)
    
    # Extract the draw method
    draw_method = button_content[draw_start:draw_end]
    
    # Enhance the hover effect
    if "if self.is_hovered:" in draw_method:
        # Make the hover effect more visible
        enhanced_hover = """        if self.is_hovered:
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
            ])"""
        
        # Replace the existing hover effect with the enhanced one
        draw_method = draw_method.replace(
            """        if self.is_hovered:
            # Pulsating effect when hovered
            pulse = math.sin(self.animation_time * 5) * 0.2 + 0.8
            hover_color = [min(255, c * pulse) for c in self.hover_color]
            
            # Draw background with hover color
            pygame.draw.rect(button_surface, (*hover_color, 150), 
                           (0, 0, self.width, self.height), 0, 10)
            
            # Draw border with glow effect
            for i in range(3, 0, -1):
                alpha = 100 if i == 1 else 50
                pygame.draw.rect(button_surface, (*self.border_color, alpha),
                               (0-i, 0-i, self.width+i*2, self.height+i*2), 
                               self.border_width, 10+i)""",
            enhanced_hover
        )
        
        # Update the button_content with the modified draw method
        button_content = button_content.replace(
            button_content[draw_start:draw_end],
            draw_method
        )
        
        print("Enhanced button hover effect with selection indicator (arrow)")

# Write the updated content back to the file
with open("button.py", "w") as f:
    f.write(button_content)

# Now update the main_menu.py file to add keyboard navigation instructions
print("\nUpdating main_menu.py to add keyboard navigation instructions...")
with open("main_menu.py", "r") as f:
    main_menu_content = f.read()

# Add keyboard navigation instructions to the draw method
if "def draw(self):" in main_menu_content:
    # Find the draw method
    draw_start = main_menu_content.find("def draw(self):")
    draw_end = main_menu_content.find("def run(self):", draw_start)
    
    # Extract the draw method
    draw_method = main_menu_content[draw_start:draw_end]
    
    # Add keyboard navigation instructions
    if "# Draw footer text" in draw_method:
        # Add keyboard navigation instructions before the footer text
        nav_instructions = """        # Draw keyboard navigation instructions
        nav_text = "Use Arrow Keys to Navigate, Enter to Select"
        nav_surface = self.small_font.render(nav_text, True, (200, 200, 200))
        nav_rect = nav_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 140))
        self.screen.blit(nav_surface, nav_rect)
        """
        
        # Insert the navigation instructions before the footer text
        draw_method = draw_method.replace(
            "        # Draw footer text",
            nav_instructions + "        # Draw footer text"
        )
        
        # Update the main_menu_content with the modified draw method
        main_menu_content = main_menu_content.replace(
            main_menu_content[draw_start:draw_end],
            draw_method
        )
        
        print("Added keyboard navigation instructions to main menu")

# Write the updated content back to the file
with open("main_menu.py", "w") as f:
    f.write(main_menu_content)

# Update the settings.py file to add keyboard navigation instructions
print("\nUpdating settings.py to add keyboard navigation instructions...")
with open("settings.py", "r") as f:
    settings_content = f.read()

# Add keyboard navigation instructions to the draw method
if "def draw(self):" in settings_content:
    # Find the draw method
    draw_start = settings_content.find("def draw(self):")
    draw_end = settings_content.find("def run(self):", draw_start)
    
    # Extract the draw method
    draw_method = settings_content[draw_start:draw_end]
    
    # Add keyboard navigation instructions
    if "# Draw help text" in draw_method:
        # Replace the help text with keyboard navigation instructions
        draw_method = draw_method.replace(
            """        # Draw help text
        help_text = "CLICK ON AN OPTION TO CHANGE IT"
        help_surface = self.text_font.render(help_text, True, (150, 150, 150))
        help_rect = help_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(help_surface, help_rect)""",
            """        # Draw help text
        help_text = "PRESS ENTER TO CHANGE SELECTED OPTION"
        help_surface = self.text_font.render(help_text, True, (150, 150, 150))
        help_rect = help_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(help_surface, help_rect)
        
        # Draw keyboard navigation instructions
        nav_text = "Use Arrow Keys to Navigate, ESC to Return"
        nav_surface = self.small_font.render(nav_text, True, (200, 200, 200))
        nav_rect = nav_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.screen.blit(nav_surface, nav_rect)"""
        )
        
        # Update the settings_content with the modified draw method
        settings_content = settings_content.replace(
            settings_content[draw_start:draw_end],
            draw_method
        )
        
        print("Added keyboard navigation instructions to settings menu")

# Write the updated content back to the file
with open("settings.py", "w") as f:
    f.write(settings_content)

# Update the high_scores.py file to add keyboard navigation instructions
print("\nUpdating high_scores.py to add keyboard navigation instructions...")
with open("high_scores.py", "r") as f:
    high_scores_content = f.read()

# Add keyboard navigation instructions to the draw method
if "def draw(self):" in high_scores_content:
    # Find the draw method
    draw_start = high_scores_content.find("def draw(self):")
    draw_end = high_scores_content.find("def run(self):", draw_start)
    
    # Extract the draw method
    draw_method = high_scores_content[draw_start:draw_end]
    
    # Add keyboard navigation instructions
    if "# Draw buttons" in draw_method:
        # Add keyboard navigation instructions before drawing buttons
        nav_instructions = """        # Draw keyboard navigation instructions
        nav_text = "Use UP/DOWN to Switch Buttons, ENTER to Select"
        nav_surface = self.small_font.render(nav_text, True, (200, 200, 200))
        nav_rect = nav_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200))
        self.screen.blit(nav_surface, nav_rect)
        
        """
        
        # Insert the navigation instructions before drawing buttons
        draw_method = draw_method.replace(
            "        # Draw buttons",
            nav_instructions + "        # Draw buttons"
        )
        
        # Update the high_scores_content with the modified draw method
        high_scores_content = high_scores_content.replace(
            high_scores_content[draw_start:draw_end],
            draw_method
        )
        
        print("Added keyboard navigation instructions to high scores screen")

# Write the updated content back to the file
with open("high_scores.py", "w") as f:
    f.write(high_scores_content)

# Update the instructions.py file to add keyboard navigation instructions
print("\nUpdating instructions.py to add keyboard navigation instructions...")
with open("instructions.py", "r") as f:
    instructions_content = f.read()

# Add keyboard navigation instructions to the draw method
if "def draw(self):" in instructions_content:
    # Find the draw method
    draw_start = instructions_content.find("def draw(self):")
    draw_end = instructions_content.find("def run(self):", draw_start)
    
    # Extract the draw method
    draw_method = instructions_content[draw_start:draw_end]
    
    # Add keyboard navigation instructions
    if "# Draw back button" in draw_method:
        # Add keyboard navigation instructions before drawing the back button
        nav_instructions = """        # Draw keyboard navigation instructions
        nav_text = "Press ESC or ENTER to Return to Menu"
        nav_surface = self.small_font.render(nav_text, True, (200, 200, 200))
        nav_rect = nav_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
        self.screen.blit(nav_surface, nav_rect)
        
        """
        
        # Insert the navigation instructions before drawing the back button
        draw_method = draw_method.replace(
            "        # Draw back button",
            nav_instructions + "        # Draw back button"
        )
        
        # Update the instructions_content with the modified draw method
        instructions_content = instructions_content.replace(
            instructions_content[draw_start:draw_end],
            draw_method
        )
        
        print("Added keyboard navigation instructions to instructions screen")

# Write the updated content back to the file
with open("instructions.py", "w") as f:
    f.write(instructions_content)

print("\nKeyboard navigation visibility has been enhanced!")
print("1. Added selection indicator (arrow) to highlight selected buttons")
print("2. Added keyboard navigation instructions to all menu screens")
print("3. Enhanced button hover effect for better visibility")
print("\nThe game now provides clear visual feedback for keyboard navigation!")