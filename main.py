import os
from dotenv import load_dotenv

load_dotenv()

import sys
import json
import re
import time
import threading
import queue

from src.brain import Brain
from src.parser import Parser
from src.dispatcher import Dispatcher
from src.tools import Toolbox
from src.ears import Ears
from src.mouth import Mouth
from src.gui import SystemZeroGUI  
from src.uplink import RemoteTether

class SystemZero:
    def __init__(self, command_queue):
        self.command_queue = command_queue 
        print(">> System Zero: Initializing modules...")
        self.brain = Brain()
        self.ears = Ears(self.command_queue)
        self.mouth = Mouth()
        print(">> System Zero: Online (Autonomy Enabled).")

    def wait_for_input(self, prompt=""):
        """Waits for input from the GUI, Telegram, or Voice."""
        if prompt:
            print(prompt, end="")
        return self.command_queue.get()

    def run(self):
        while True:
            try:
                user_input = self.wait_for_input()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ["exit", "quit", "shutdown"]:
                    print(">> [SYSTEM] Shutting down...")
                    break

                # --- EXECUTION ---
                self.ears.is_busy = True   # <--- TURN ON MUTE SWITCH
                
                self.process_task(user_input)
                
                self.ears.is_busy = False  # <--- TURN OFF MUTE SWITCH (Listen for follow-up!)

            except Exception as e:
                print(f"\n[CRITICAL ERROR] {e}")
                break

    def process_task(self, initial_input):
        current_input = initial_input
        error_count = 0
        is_first_thought = True  
        
        while True:
            # (Standard image logic)
            image_attachment = None
            match = re.search(r"@([\w\-\.\/\\]+)", current_input)
            if match:
                image_attachment = match.group(1)
                current_input = current_input.replace(f"@{image_attachment}", "").strip()

            print(">> Thinking...")
            raw_response = self.brain.think(current_input, image_path=image_attachment)
            command = Parser.extract_command(raw_response)
            
            trust_session = True
            
            # --- 🛡️ THE SECURITY FILTER 🛡️ ---
            thought_text = command.get('thought', '')
            action_name = command.get('action', '')
            params_str = str(command.get('params', {}))
            
            combined_context = (str(thought_text) + " " + action_name + " " + params_str).lower()
            
            dangerous_pattern = r"\b(delete|remove|format|erase|uninstall|rmdir|drop)\b"
            is_dangerous = bool(re.search(dangerous_pattern, combined_context))

            if is_dangerous:
                trust_session = False
                print("\n>> [SECURITY ALERT] Destructive intent detected!")
                self.mouth.speak("Warning. Destructive action detected. I need your explicit permission to proceed.", wait=True)
            
            # --- 🗣️ THE MOUTH LOGIC (QUIET MODE) ---
            if thought_text:
                print(f"[PLAN] Reason: {thought_text}")
                
                if is_dangerous:
                    self.mouth.speak(f"The plan is: {thought_text}", wait=True)
                elif is_first_thought:
                    self.mouth.speak(thought_text, wait=True)
                    is_first_thought = False  
            
            # (Error Loop Protection)
            if "error" in command and "Complete" not in command.get('thought', ''):
                error_count += 1
                if error_count > 2:
                    print(f"\n[CRITICAL]: System stuck in loop. Terminating.")
                    self.mouth.speak("I am stuck. Aborting task.", wait=True)
                    break
            else:
                error_count = 0 

            print(f"\n[PLAN] Action: {command.get('action')}")
            
            # --- 🛑 AUTHORIZATION GATE ---
            if not trust_session:
                # You can now authorize by typing "yes" OR saying "Zero, yes"!
                confirm = self.wait_for_input("\n>> Execute? (Type 'y' or say 'Zero, yes'): ").lower()
                
                if any(word in confirm for word in ['y', 'yes', 'go', 'do it', 'confirm']):
                    trust_session = True
                    self.mouth.speak("Override accepted. Executing.", wait=True)
                else:
                    print(">> [SYSTEM] Action aborted by Operator.")
                    self.mouth.speak("Action aborted.", wait=True)
                    break
            
            # (Execution)
            if trust_session:
                time.sleep(0.2) 
            
            result = Dispatcher.execute(command)
            print(f"\n[RESULT]:\n{json.dumps(result, indent=2)}")
            
            # --- 🏁 TASK COMPLETE LOGIC ---
            if result.get("status") == "task_complete":
                summary = result.get("message", "Task completed.")
                self.mouth.speak(summary, wait=True)
                break

            current_input = f"ORIGINAL GOAL: {initial_input}\nSYSTEM FEEDBACK: Last action resulted in: {json.dumps(result)}. What is the next step?"
            
# --- BOOT SEQUENCE ---
if __name__ == "__main__":
    cmd_queue = queue.Queue()
    tether = RemoteTether(cmd_queue)  
    app = SystemZeroGUI(cmd_queue)
    agent = SystemZero(cmd_queue)
    
    agent_thread = threading.Thread(target=agent.run, daemon=True)
    agent_thread.start()
    
    app.mainloop()