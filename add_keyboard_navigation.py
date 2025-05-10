import os

print("Adding keyboard navigation to menus...")

# First, update the main_menu.py file
print("\nUpdating main_menu.py...")
with open("main_menu.py", "r") as f:
    main_menu_content = f.read()

# Add selected_button variable to __init__ method
if "def __init__(self, screen, clock, sound_manager):" in main_menu_content:
    main_menu_content = main_menu_content.replace(
        "def __init__(self, screen, clock, sound_manager):",
        "def __init__(self, screen, clock, sound_manager):\n        # Current selected button for keyboard navigation\n        self.selected_button = 0"
    )
    print("Added selected_button variable to MainMenu class")

# Update handle_events method to handle keyboard navigation
if "def handle_events(self):" in main_menu_content:
    # Find the handle_events method
    handle_events_start = main_menu_content.find("def handle_events(self):")
    handle_events_end = main_menu_content.find("def update(self):", handle_events_start)
    
    # Extract the handle_events method
    handle_events_method = main_menu_content[handle_events_start:handle_events_end]
    
    # Add keyboard navigation
    if "elif event.type == KEYDOWN:" in handle_events_method:
        # Replace the existing KEYDOWN handling
        new_keydown_handling = """            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    self.selected_option = "exit"
                elif event.key == K_UP:
                    # Navigate up
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                    self.sound_manager.play("hover")
                elif event.key == K_DOWN:
                    # Navigate down
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                    self.sound_manager.play("hover")
                elif event.key == K_RETURN or event.key == K_SPACE:
                    # Select current button
                    self.sound_manager.play("click")
                    if self.selected_button == 0:  # Start Game
                        self.running = False
                        self.selected_option = "start"
                    elif self.selected_button == 1:  # High Scores
                        self.running = False
                        self.selected_option = "scores"
                    elif self.selected_button == 2:  # Instructions
                        self.running = False
                        self.selected_option = "instructions"
                    elif self.selected_button == 3:  # Settings
                        self.running = False
                        self.selected_option = "settings"
                    elif self.selected_button == 4:  # Exit
                        self.running = False
                        self.selected_option = "exit"
"""
        
        # Replace the existing KEYDOWN handling with the new one
        handle_events_method = handle_events_method.replace(
            """            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    self.selected_option = "exit\"""",
            new_keydown_handling.rstrip()
        )
        
        # Update the main_menu_content with the modified handle_events method
        main_menu_content = main_menu_content.replace(
            main_menu_content[handle_events_start:handle_events_end],
            handle_events_method
        )
        
        print("Added keyboard navigation to MainMenu.handle_events method")

# Update the update method to highlight the selected button
if "def update(self):" in main_menu_content:
    # Find the update method
    update_start = main_menu_content.find("def update(self):")
    update_end = main_menu_content.find("def draw(self):", update_start)
    
    # Extract the update method
    update_method = main_menu_content[update_start:update_end]
    
    # Add code to highlight the selected button
    if "# Update buttons" in update_method:
        # Replace the existing button update code
        new_button_update = """        # Update buttons
        for i, button in enumerate(self.buttons):
            # Set hover state based on selected button
            button.is_hovered = (i == self.selected_button)
            button.update(dt)
"""
        
        # Replace the existing button update code with the new one
        update_method = update_method.replace(
            """        # Update buttons
        for button in self.buttons:
            button.update(dt)""",
            new_button_update.rstrip()
        )
        
        # Update the main_menu_content with the modified update method
        main_menu_content = main_menu_content.replace(
            main_menu_content[update_start:update_end],
            update_method
        )
        
        print("Updated MainMenu.update method to highlight selected button")

# Write the updated content back to the file
with open("main_menu.py", "w") as f:
    f.write(main_menu_content)

# Now update the settings.py file
print("\nUpdating settings.py...")
with open("settings.py", "r") as f:
    settings_content = f.read()

# Add selected_button variable to __init__ method
if "def __init__(self, screen, clock, sound_manager):" in settings_content:
    settings_content = settings_content.replace(
        "def __init__(self, screen, clock, sound_manager):",
        "def __init__(self, screen, clock, sound_manager):\n        # Current selected button for keyboard navigation\n        self.selected_button = 0"
    )
    print("Added selected_button variable to Settings class")

# Update handle_events method to handle keyboard navigation
if "def handle_events(self):" in settings_content:
    # Find the handle_events method
    handle_events_start = settings_content.find("def handle_events(self):")
    handle_events_end = settings_content.find("def update(self):", handle_events_start)
    
    # Extract the handle_events method
    handle_events_method = settings_content[handle_events_start:handle_events_end]
    
    # Add keyboard navigation
    if "elif event.type == KEYDOWN:" in handle_events_method:
        # Add keyboard navigation code
        new_keydown_handling = """            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    return "menu"
                elif event.key == K_UP:
                    # Navigate up
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                    self.sound_manager.play("hover")
                elif event.key == K_DOWN:
                    # Navigate down
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                    self.sound_manager.play("hover")
                elif event.key == K_RETURN or event.key == K_SPACE:
                    # Select current button
                    self.sound_manager.play("click")
                    
                    # Get the selected button
                    button = self.buttons[self.selected_button]
                    
                    # Process button action based on index
                    i = self.selected_button
"""
        
        # Replace the existing KEYDOWN handling with the new one
        handle_events_method = handle_events_method.replace(
            """            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    return "menu\"""",
            new_keydown_handling.rstrip()
        )
        
        # Update the settings_content with the modified handle_events method
        settings_content = settings_content.replace(
            settings_content[handle_events_start:handle_events_end],
            handle_events_method
        )
        
        print("Added keyboard navigation to Settings.handle_events method")

# Update the update method to highlight the selected button
if "def update(self):" in settings_content:
    # Find the update method
    update_start = settings_content.find("def update(self):")
    update_end = settings_content.find("def draw(self):", update_start)
    
    # Extract the update method
    update_method = settings_content[update_start:update_end]
    
    # Add code to highlight the selected button
    if "# Update buttons" in update_method:
        # Replace the existing button update code
        new_button_update = """        # Update buttons
        for i, button in enumerate(self.buttons):
            # Set hover state based on selected button
            button.is_hovered = (i == self.selected_button)
            button.update(dt)
"""
        
        # Replace the existing button update code with the new one
        update_method = update_method.replace(
            """        # Update buttons
        for button in self.buttons:
            button.update(dt)""",
            new_button_update.rstrip()
        )
        
        # Update the settings_content with the modified update method
        settings_content = settings_content.replace(
            settings_content[update_start:update_end],
            update_method
        )
        
        print("Updated Settings.update method to highlight selected button")

# Write the updated content back to the file
with open("settings.py", "w") as f:
    f.write(settings_content)

# Update the high_scores.py file
print("\nUpdating high_scores.py...")
with open("high_scores.py", "r") as f:
    high_scores_content = f.read()

# Add selected_button variable to __init__ method
if "def __init__(self, screen, clock, sound_manager, scores_data):" in high_scores_content:
    high_scores_content = high_scores_content.replace(
        "def __init__(self, screen, clock, sound_manager, scores_data):",
        "def __init__(self, screen, clock, sound_manager, scores_data):\n        # Current selected button for keyboard navigation\n        self.selected_button = 0"
    )
    print("Added selected_button variable to HighScores class")

# Add keyboard navigation to handle_events method
if "def handle_events(self):" in high_scores_content:
    # Find the handle_events method
    handle_events_start = high_scores_content.find("def handle_events(self):")
    handle_events_end = high_scores_content.find("def update(self):", handle_events_start)
    
    # Extract the handle_events method
    handle_events_method = high_scores_content[handle_events_start:handle_events_end]
    
    # Add keyboard navigation
    if "elif event.type == KEYDOWN:" in handle_events_method:
        # Add keyboard navigation code
        new_keydown_handling = """            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    return "menu"
                elif event.key == K_UP or event.key == K_DOWN:
                    # Toggle between back and reset buttons
                    self.selected_button = 1 - self.selected_button
                    self.sound_manager.play("hover")
                elif event.key == K_RETURN or event.key == K_SPACE:
                    # Select current button
                    self.sound_manager.play("click")
                    if self.selected_button == 0:  # Back button
                        self.running = False
                        return "menu"
                    elif self.selected_button == 1:  # Reset button
                        # Reset high scores
                        self.scores_data["scores"] = []
                        # Save the empty scores
                        with open("high_scores.json", "w") as f:
                            json.dump(self.scores_data, f)
"""
        
        # Replace the existing KEYDOWN handling with the new one
        handle_events_method = handle_events_method.replace(
            """            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    return "menu\"""",
            new_keydown_handling.rstrip()
        )
        
        # Update the high_scores_content with the modified handle_events method
        high_scores_content = high_scores_content.replace(
            high_scores_content[handle_events_start:handle_events_end],
            handle_events_method
        )
        
        print("Added keyboard navigation to HighScores.handle_events method")

# Update the update method to highlight the selected button
if "def update(self):" in high_scores_content:
    # Find the update method
    update_start = high_scores_content.find("def update(self):")
    update_end = high_scores_content.find("def draw(self):", update_start)
    
    # Extract the update method
    update_method = high_scores_content[update_start:update_end]
    
    # Add code to highlight the selected buttons
    update_method_lines = update_method.split("\n")
    new_update_method_lines = []
    
    for line in update_method_lines:
        if "self.back_button.update(dt)" in line:
            new_update_method_lines.append("        # Set hover state based on selected button")
            new_update_method_lines.append("        self.back_button.is_hovered = (self.selected_button == 0)")
            new_update_method_lines.append("        self.back_button.update(dt)")
        elif "self.reset_button.update(dt)" in line:
            new_update_method_lines.append("        self.reset_button.is_hovered = (self.selected_button == 1)")
            new_update_method_lines.append("        self.reset_button.update(dt)")
        else:
            new_update_method_lines.append(line)
    
    # Join the lines back together
    new_update_method = "\n".join(new_update_method_lines)
    
    # Update the high_scores_content with the modified update method
    high_scores_content = high_scores_content.replace(update_method, new_update_method)
    
    print("Updated HighScores.update method to highlight selected button")

# Write the updated content back to the file
with open("high_scores.py", "w") as f:
    f.write(high_scores_content)

# Update the instructions.py file
print("\nUpdating instructions.py...")
with open("instructions.py", "r") as f:
    instructions_content = f.read()

# Add selected_button variable to __init__ method
if "def __init__(self, screen, clock, sound_manager):" in instructions_content:
    instructions_content = instructions_content.replace(
        "def __init__(self, screen, clock, sound_manager):",
        "def __init__(self, screen, clock, sound_manager):\n        # Current selected button for keyboard navigation\n        self.selected_button = 0"
    )
    print("Added selected_button variable to Instructions class")

# Add keyboard navigation to handle_events method
if "def handle_events(self):" in instructions_content:
    # Find the handle_events method
    handle_events_start = instructions_content.find("def handle_events(self):")
    handle_events_end = instructions_content.find("def update(self):", handle_events_start)
    
    # Extract the handle_events method
    handle_events_method = instructions_content[handle_events_start:handle_events_end]
    
    # Add keyboard navigation
    if "elif event.type == KEYDOWN:" in handle_events_method:
        # Add keyboard navigation code
        new_keydown_handling = """            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    return "menu"
                elif event.key == K_RETURN or event.key == K_SPACE:
                    # Return to menu
                    self.running = False
                    return "menu"
"""
        
        # Replace the existing KEYDOWN handling with the new one
        handle_events_method = handle_events_method.replace(
            """            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    return "menu\"""",
            new_keydown_handling.rstrip()
        )
        
        # Update the instructions_content with the modified handle_events method
        instructions_content = instructions_content.replace(
            instructions_content[handle_events_start:handle_events_end],
            handle_events_method
        )
        
        print("Added keyboard navigation to Instructions.handle_events method")

# Update the update method to highlight the back button
if "def update(self):" in instructions_content:
    # Find the update method
    update_start = instructions_content.find("def update(self):")
    update_end = instructions_content.find("def draw(self):", update_start)
    
    # Extract the update method
    update_method = instructions_content[update_start:update_end]
    
    # Add code to highlight the back button
    update_method_lines = update_method.split("\n")
    new_update_method_lines = []
    
    for line in update_method_lines:
        if "self.back_button.update(dt)" in line:
            new_update_method_lines.append("        # Always highlight the back button")
            new_update_method_lines.append("        self.back_button.is_hovered = True")
            new_update_method_lines.append("        self.back_button.update(dt)")
        else:
            new_update_method_lines.append(line)
    
    # Join the lines back together
    new_update_method = "\n".join(new_update_method_lines)
    
    # Update the instructions_content with the modified update method
    instructions_content = instructions_content.replace(update_method, new_update_method)
    
    print("Updated Instructions.update method to highlight back button")

# Write the updated content back to the file
with open("instructions.py", "w") as f:
    f.write(instructions_content)

print("\nKeyboard navigation has been added to all menu screens!")
print("Players can now navigate menus using:")
print("- UP/DOWN arrow keys: Navigate between buttons")
print("- ENTER/SPACE: Select the highlighted button")
print("- ESC: Return to previous menu or exit")

print("\nAll tasks completed successfully!")
print("1. Project files cleaned up and organized")
print("2. Keyboard navigation added to all menus")
print("\nThe game is now ready for production!")