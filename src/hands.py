import pywinauto
from pywinauto import Desktop
import time

class Hands:
    def __init__(self):
        print(">> [HANDS] Initializing UI Injection Layer (UIA)...")
        # 'uia' (UI Automation) is required for modern apps like Chrome, WhatsApp, VS Code
        self.backend = "uia"
        print(">> [HANDS] Cybernetic Interface Online.")

    def get_active_window(self):
        """Connects to the currently focused window."""
        try:
            # Connect to the foreground application
            app = Desktop(backend=self.backend).window(active_only=True)
            if app:
                return app
            return None
        except Exception:
            return None

    def inspect_ui(self):
        """
        scans the active window and returns a list of clickable elements.
        The Brain uses this to know what 'names' to use for clicking.
        """
        window = self.get_active_window()
        if not window:
            return "No active window found."

        window_title = window.window_text()
        print(f">> [HANDS] Inspecting UI of: {window_title}")
        
        # We recursively search for buttons, edit fields, and links
        controls = []
        
        # This wrapper captures all "descendants" (children) of the window
        # limiting depth to 2 prevents getting stuck in huge trees
        for child in window.descendants(control_type="Button", depth=2):
            if child.window_text():
                controls.append(f"[Button] '{child.window_text()}'")
                
        for child in window.descendants(control_type="Edit", depth=2):
             controls.append(f"[Input] Edit Box")

        for child in window.descendants(control_type="Hyperlink", depth=2):
            if child.window_text():
                 controls.append(f"[Link] '{child.window_text()}'")
        
        if not controls:
            return f"Window '{window_title}' found, but no clear controls visible via UIA."
            
        return f"Visible Controls in '{window_title}':\n" + "\n".join(controls[:30]) # Limit to 30 to save tokens

    def click_element(self, element_name):
        """
        Directly triggers a button by its text name.
        """
        window = self.get_active_window()
        if not window:
            return {"error": "No active window."}

        try:
            # Magic: Find the button by its exact text name and click it
            # .click_input() moves mouse, .invoke() is pure code (ghost click)
            target = window.child_window(title=element_name, control_type="Button")
            
            if target.exists():
                print(f">> [HANDS] Ghost-Clicking '{element_name}'...")
                target.invoke() # Pure API call, no mouse movement!
                return {"status": "success", "action": f"Injected click into '{element_name}'"}
            else:
                return {"error": f"Element '{element_name}' not found in active window."}

        except Exception as e:
            return {"error": f"Injection Failed: {e}"}