import customtkinter as ctk
import sys
import queue

class TextRedirector:
    """Hijacks terminal output and routes it safely to the GUI text box from any thread."""
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        # Schedule the UI update safely on the main thread
        self.widget.after(0, self._insert_text, text)
        
    def _insert_text(self, text):
        # Insert text at the end and auto-scroll to the bottom
        self.widget.insert(ctk.END, text)
        self.widget.see(ctk.END)
        
    def flush(self):
        pass

class SystemZeroGUI(ctk.CTk):
    def __init__(self, command_queue):
        super().__init__()
        self.command_queue = command_queue
        
        # --- WINDOW SETUP ---
        self.title("System Zero v4.0 - Command Node")
        self.geometry("900x650")
        
        # Force Dark Mode and a Matrix-Green color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green") 
        
        # --- HEADER ---
        self.header = ctk.CTkLabel(
            self, text="SYSTEM ZERO // NEURAL LINK ESTABLISHED", 
            font=("Consolas", 18, "bold"), text_color="#00FF41"
        )
        self.header.pack(pady=(15, 5))

        # --- MATRIX CONSOLE (Event Log) ---
        # A sleek, borderless text box for the agent's output
        self.console = ctk.CTkTextbox(
            self, width=860, height=500, 
            font=("Consolas", 14), text_color="#00FF41", fg_color="#0D0D0D", 
            border_width=1, border_color="#008F11"
        )
        self.console.pack(pady=10, padx=20)
        
        # Route all terminal print() statements directly to this console!
        sys.stdout = TextRedirector(self.console)
        
        # --- INPUT ROW ---
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill=ctk.X, padx=20, pady=5)
        
        self.entry = ctk.CTkEntry(
            self.input_frame, width=700, height=40, 
            font=("Consolas", 14), placeholder_text="Enter command or type 'voice' to activate audio sensors..."
        )
        self.entry.pack(side=ctk.LEFT, padx=(0, 10))
        self.entry.bind("<Return>", self.send_command) # Pressing Enter sends command
        
        self.send_btn = ctk.CTkButton(
            self.input_frame, text="EXECUTE", width=140, height=40,
            font=("Consolas", 14, "bold"), fg_color="#008F11", hover_color="#00FF41",
            command=self.send_command
        )
        self.send_btn.pack(side=ctk.LEFT)

        # Handle window close gracefully
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def send_command(self, event=None):
        cmd = self.entry.get()
        if cmd.strip():
            print(f"\n[OPERATOR]: {cmd}")
            self.command_queue.put(cmd)
            self.entry.delete(0, ctk.END)

    def on_close(self):
        print(">> [SYSTEM] Shutting down Neural Node...")
        self.destroy()
        sys.exit(0)