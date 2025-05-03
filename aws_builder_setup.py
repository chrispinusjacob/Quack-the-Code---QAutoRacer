import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class BuilderIDSetupWindow:
    """
    GUI window for setting up AWS Builder ID
    """
    def __init__(self, root=None):
        self.standalone = root is None
        
        if self.standalone:
            self.root = tk.Tk()
            self.root.title("QAutoRacer - AWS Builder ID Setup")
            self.root.geometry("600x450")
            self.root.resizable(False, False)
        else:
            self.root = root
            self.setup_frame = tk.Frame(self.root)
            self.setup_frame.pack(fill=tk.BOTH, expand=True)
            
        self.config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "amazon_q_config.json")
        self.credentials = self._load_credentials()
        
        self._create_widgets()
        
    def _load_credentials(self):
        """Load AWS Builder ID from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return {
                "builder_id": ""
            }
        except Exception as e:
            print(f"Error loading AWS Builder ID: {e}")
            return {
                "builder_id": ""
            }
            
    def _create_widgets(self):
        """Create the GUI widgets"""
        # Main container
        if self.standalone:
            container = self.root
        else:
            container = self.setup_frame
            
        # Title
        title_frame = tk.Frame(container)
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, text="AWS Builder ID Setup", font=("Arial", 18, "bold"))
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Configure your AWS Builder ID for AI features")
        subtitle_label.pack()
        
        # Form
        form_frame = tk.Frame(container)
        form_frame.pack(pady=10, padx=30, fill=tk.X)
        
        # Builder ID
        builder_id_label = tk.Label(form_frame, text="AWS Builder ID:", anchor="w")
        builder_id_label.pack(fill=tk.X)
        
        self.builder_id_entry = tk.Entry(form_frame, width=50)
        self.builder_id_entry.pack(fill=tk.X, pady=(0, 10))
        if self.credentials and "builder_id" in self.credentials:
            self.builder_id_entry.insert(0, self.credentials["builder_id"])
        
        # Buttons
        button_frame = tk.Frame(container)
        button_frame.pack(pady=10)
        
        self.save_button = tk.Button(button_frame, text="Save Builder ID", command=self._save_credentials)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        if self.standalone:
            self.close_button = tk.Button(button_frame, text="Close", command=self.root.destroy)
            self.close_button.pack(side=tk.LEFT, padx=5)
        
        # Instructions
        instructions_frame = tk.Frame(container)
        instructions_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)
        
        instructions_label = tk.Label(instructions_frame, text="Setup Instructions:", anchor="w", font=("Arial", 10, "bold"))
        instructions_label.pack(fill=tk.X)
        
        instructions_text = tk.Text(instructions_frame, height=10, wrap=tk.WORD)
        instructions_text.pack(fill=tk.BOTH, expand=True)
        
        instructions = """
1. Create an AWS Builder ID at https://profile.aws.amazon.com/
2. Enter your Builder ID email address above
3. Click "Save Builder ID"

That's it! No AWS account or credit card required.

The Amazon Q Developer free tier includes:
- 2 million tokens per month
- Access to all AI features in the game
- No credit card required
        """
        
        instructions_text.insert(tk.END, instructions)
        instructions_text.config(state=tk.DISABLED)
        
    def _save_credentials(self):
        """Save the credentials to the config file"""
        builder_id = self.builder_id_entry.get()
        
        if not builder_id or "@" not in builder_id:
            messagebox.showerror("Error", "Please enter a valid email address for your AWS Builder ID")
            return False
            
        credentials = {
            "builder_id": builder_id
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(credentials, f)
            messagebox.showinfo("Success", "AWS Builder ID saved successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save Builder ID: {e}")
            return False
            
    def run(self):
        """Run the application"""
        if self.standalone:
            self.root.mainloop()
            
    def destroy(self):
        """Destroy the window"""
        if self.standalone:
            self.root.destroy()
        else:
            self.setup_frame.destroy()


if __name__ == "__main__":
    # Run as standalone application
    app = BuilderIDSetupWindow()
    app.run()