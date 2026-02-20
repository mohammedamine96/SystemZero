import customtkinter as ctk
import threading
import sys

# Set dark mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TextRedirector:
    """Magically catches all print() statements and sends them to the GUI."""
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, string):
        # Insert text at the end and auto-scroll down
        self.textbox.configure(state="normal")
        self.textbox.insert(ctk.END, string)
        self.textbox.see(ctk.END)
        self.textbox.configure(state="disabled")

    def flush(self):
        pass

class SystemZeroGUI(ctk.CTk):
    def __init__(self, command_queue):
        super().__init__()
        self.command_queue = command_queue

        # Window Setup
        self.title("System Zero - Operator Dashboard")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Main Terminal Output (The Telemetry Log)
        self.console = ctk.CTkTextbox(self, font=("Consolas", 14), fg_color="#1e1e1e", text_color="#00ff00")
        self.console.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        self.console.configure(state="disabled")

        # Redirect standard output (print) to this text box
        sys.stdout = TextRedirector(self.console)

        # 2. Bottom Input Area
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.input_box = ctk.CTkEntry(self.input_frame, placeholder_text="Type command or 'y' to confirm...", font=("Consolas", 14))
        self.input_box.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        # Allow hitting Enter to send
        self.input_box.bind("<Return>", self._on_send)

        self.send_btn = ctk.CTkButton(self.input_frame, text="SEND", font=("Consolas", 14, "bold"), command=self._on_send)
        self.send_btn.grid(row=0, column=1)

    def _on_send(self, event=None):
        """Triggers when you click SEND or press Enter."""
        text = self.input_box.get()
        if text.strip():
            # Send the text to the background agent thread
            self.command_queue.put(text)
            self.input_box.delete(0, ctk.END) # Clear the box
            print(f"\n[USER]: {text}")