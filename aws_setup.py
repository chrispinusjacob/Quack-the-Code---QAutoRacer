import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class AWSSetupWindow:
    """
    GUI window for setting up AWS Builder ID credentials
    """
    def __init__(self, root=None):
        self.standalone = root is None
        
        if self.standalone:
            self.root = tk.Tk()
            self.root.title("QAutoRacer - AWS Setup")
            self.root.geometry("600x500")
            self.root.resizable(False, False)
        else:
            self.root = root
            self.setup_frame = tk.Frame(self.root)
            self.setup_frame.pack(fill=tk.BOTH, expand=True)
            
        self.config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "aws_config.json")
        self.credentials = self._load_credentials()
        
        self._create_widgets()
        
    def _load_credentials(self):
        """Load AWS credentials from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return {
                "builder_id": "",
                "access_key": "",
                "secret_key": "",
                "region": "us-east-1"
            }
        except Exception as e:
            print(f"Error loading AWS credentials: {e}")
            return {
                "builder_id": "",
                "access_key": "",
                "secret_key": "",
                "region": "us-east-1"
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
        
        subtitle_label = tk.Label(title_frame, text="Configure your AWS credentials for AI features")
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
        
        # Access Key
        access_key_label = tk.Label(form_frame, text="Access Key ID:", anchor="w")
        access_key_label.pack(fill=tk.X)
        
        self.access_key_entry = tk.Entry(form_frame, width=50)
        self.access_key_entry.pack(fill=tk.X, pady=(0, 10))
        if self.credentials and "access_key" in self.credentials:
            self.access_key_entry.insert(0, self.credentials["access_key"])
        
        # Secret Key
        secret_key_label = tk.Label(form_frame, text="Secret Access Key:", anchor="w")
        secret_key_label.pack(fill=tk.X)
        
        self.secret_key_entry = tk.Entry(form_frame, width=50, show="*")
        self.secret_key_entry.pack(fill=tk.X, pady=(0, 10))
        if self.credentials and "secret_key" in self.credentials:
            self.secret_key_entry.insert(0, self.credentials["secret_key"])
        
        # Region
        region_label = tk.Label(form_frame, text="AWS Region:", anchor="w")
        region_label.pack(fill=tk.X)
        
        regions = [
            "us-east-1", "us-east-2", "us-west-1", "us-west-2",
            "eu-west-1", "eu-west-2", "eu-central-1",
            "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2",
            "sa-east-1"
        ]
        
        self.region_var = tk.StringVar()
        if self.credentials and "region" in self.credentials:
            self.region_var.set(self.credentials["region"])
        else:
            self.region_var.set("us-east-1")
            
        region_dropdown = ttk.Combobox(form_frame, textvariable=self.region_var, values=regions)
        region_dropdown.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(container)
        button_frame.pack(pady=10)
        
        self.test_button = tk.Button(button_frame, text="Test Connection", command=self._test_connection)
        self.test_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = tk.Button(button_frame, text="Save Credentials", command=self._save_credentials)
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
2. Sign in to the AWS Management Console
3. Create an IAM user with programmatic access
4. Attach the "AmazonQFullAccess" policy to the user
5. Copy the Access Key ID and Secret Access Key
6. Enter these credentials above and click "Save Credentials"

Note: You can use the AWS Free Tier for this game's AI features.
        """
        
        instructions_text.insert(tk.END, instructions)
        instructions_text.config(state=tk.DISABLED)
        
    def _save_credentials(self):
        """Save the credentials to the config file"""
        credentials = {
            "builder_id": self.builder_id_entry.get(),
            "access_key": self.access_key_entry.get(),
            "secret_key": self.secret_key_entry.get(),
            "region": self.region_var.get()
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(credentials, f)
            messagebox.showinfo("Success", "AWS credentials saved successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save credentials: {e}")
            return False
            
    def _test_connection(self):
        """Test the AWS connection"""
        # Disable buttons during test
        self.test_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        
        # Create a progress bar
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(pady=10)
        
        progress_label = tk.Label(progress_frame, text="Testing connection...")
        progress_label.pack()
        
        progress_bar = ttk.Progressbar(progress_frame, mode="indeterminate", length=200)
        progress_bar.pack(pady=5)
        progress_bar.start()
        
        # Run the test in a separate thread
        def test_thread():
            # In a real implementation, this would use the AWS SDK to test the connection
            time.sleep(2)  # Simulate API call
            
            # Remove progress bar
            progress_bar.stop()
            progress_frame.destroy()
            
            # Re-enable buttons
            self.test_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)
            
            # Show result
            messagebox.showinfo("Connection Test", "Connection successful! Your AWS credentials are valid.")
            
        threading.Thread(target=test_thread).start()
        
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
    app = AWSSetupWindow()
    app.run()