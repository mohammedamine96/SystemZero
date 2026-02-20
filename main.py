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
from src.gui import SystemZeroGUI  # <--- NEW IMPORT

class SystemZero:
    def __init__(self, command_queue):
        self.command_queue = command_queue # Connects to the GUI input
        print(">> System Zero: Initializing modules...")
        self.brain = Brain()
        self.ears = Ears()
        self.mouth = Mouth()
        print(">> System Zero: Online (Autonomy Enabled).")

    def wait_for_text_input(self, prompt=""):
        """Replaces standard input(). Waits for the GUI queue."""
        if prompt:
            print(prompt, end="")
        # This blocks the background thread until the user clicks "SEND" on the GUI
        return self.command_queue.get()

    def run(self):
        input_mode = "text"
        active_session = False 

        while True:
            try:
                user_input = None
                
                # --- INPUT HANDLING ---
                if input_mode == "text":
                    # Wait for text from the GUI instead of the terminal
                    user_input = self.wait_for_text_input()
                    
                    if user_input.lower().strip() == "voice":
                        input_mode = "voice"
                        print("\n>> [SYSTEM] Switched to VOICE MODE.")
                        continue

                elif input_mode == "voice":
                    # STATE 1: ASLEEP (Waiting for "Start")
                    if not active_session:
                        if self.ears.wait_for_wake_word("zero"): # Using 'zero' based on your latest log
                            active_session = True
                            self.mouth.speak("I am listening.", wait=True)
                        else:
                            continue 

                    # STATE 2: AWAKE (Continuous Listening)
                    if active_session:
                        # Listen for command
                        user_input = self.ears.listen()
                        
                        if not user_input:
                            continue

                        # Commands to sleep/exit voice mode
                        if "sleep" in user_input.lower() or "stop listening" in user_input.lower():
                            active_session = False
                            self.mouth.speak("Going to sleep.", wait=True)
                            continue

                        if "switch to text" in user_input.lower():
                            input_mode = "text"
                            active_session = False
                            self.mouth.speak("Switching to text mode.", wait=True)
                            continue

                if not user_input:
                    continue
                
                if user_input.lower() in ["exit", "quit", "shutdown"]:
                    print(">> [SYSTEM] Shutting down...")
                    break

                # --- EXECUTION ---
                self.process_task(user_input, input_mode)

            except Exception as e:
                print(f"\n[CRITICAL ERROR] {e}")
                break

    def process_task(self, initial_input, input_mode="text"):
        current_input = initial_input
        error_count = 0
        is_first_thought = True  # <--- Tracks if this is the first action
        
        while True:
            # (Standard image logic)
            image_attachment = None
            match = re.search(r"@([\w\-\.]+)", current_input)
            if match:
                image_attachment = match.group(1)
                current_input = current_input.replace(f"@{image_attachment}", "").strip()

            print(">> Thinking...")
            raw_response = self.brain.think(current_input, image_path=image_attachment)
            command = Parser.extract_command(raw_response)
            
            # Default Trust
            trust_session = True
            
            # --- 🛡️ THE SECURITY FILTER 🛡️ ---
            thought_text = command.get('thought', '')
            action_name = command.get('action', '')
            params_str = str(command.get('params', {}))
            
            # Define words that trigger the safety lockdown
            dangerous_keywords = ["delete", "remove", "format", "erase", "uninstall", "rmdir", "drop"]
            combined_context = (str(thought_text) + " " + action_name + " " + params_str).lower()
            
            is_dangerous = any(word in combined_context for word in dangerous_keywords)
            
            if is_dangerous:
                # REVOKE TRUST! Force the user to confirm.
                trust_session = False
                print("\n>> [SECURITY ALERT] Destructive intent detected!")
                self.mouth.speak("Warning. Destructive action detected. I need your explicit permission to proceed.", wait=True)
            
            # --- 🗣️ THE MOUTH LOGIC (QUIET MODE) ---
            if thought_text:
                print(f"[PLAN] Reason: {thought_text}")
                
                if is_dangerous:
                    # Always speak the plan if it's dangerous so you know what you are approving
                    self.mouth.speak(f"The plan is: {thought_text}", wait=True)
                elif is_first_thought:
                    # Speak ONLY the first thought
                    self.mouth.speak(thought_text, wait=True)
                    is_first_thought = False  # Turn off the mouth for the next loops
                else:
                    # Stay silent for intermediate steps
                    pass 

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
                if input_mode == "text":
                    confirm = self.wait_for_text_input(">> Execute? (y / n / stop): ")
                    if confirm.lower() == 'y' or confirm.lower() == 'y!':
                        trust_session = True
                    elif confirm.lower() in ['stop', 'n']:
                        print(">> [SYSTEM] Action aborted by Operator.")
                        break
                
                elif input_mode == "voice":
                    print(">> [WAITING FOR OVERRIDE] Say 'Yes', 'Go', or 'Stop'...")
                    time.sleep(0.5) 
                    
                    attempts = 0
                    authorized = False
                    
                    while attempts < 3:
                        approval = self.ears.listen()
                        if approval:
                            print(f">> [HEARD]: '{approval}'")
                            approval = approval.lower()
                            if any(word in approval for word in ["yes", "yeah", "go", "proceed", "ok", "do it", "confirm"]):
                                authorized = True
                                trust_session = True
                                self.mouth.speak("Override accepted. Executing.", wait=True)
                                break
                            elif any(word in approval for word in ["stop", "no", "wait", "cancel", "abort"]):
                                self.mouth.speak("Action aborted.", wait=True)
                                return 
                            else:
                                print(">> [SYSTEM] Invalid confirmation. Say 'Yes' or 'No'.")
                                attempts += 1
                        else:
                            print(">> [SILENCE] I didn't hear you. Listening again...")
                            attempts += 1
                    
                    if not authorized:
                        print(">> [TIMEOUT] Authorization failed.")
                        self.mouth.speak("Authorization timeout. Aborting.", wait=True)
                        break

            # (Execution)
            if trust_session:
                time.sleep(0.2) 
            
            result = Dispatcher.execute(command)
            print(f"\n[RESULT]:\n{json.dumps(result, indent=2)}")
            
            # --- 🏁 TASK COMPLETE LOGIC (FIXED) ---
            if result.get("status") == "task_complete":
                # Extract the final message from the Dispatcher's output
                summary = result.get("message", "Task completed.")
                # The agent speaks its final summary here!
                self.mouth.speak(summary, wait=True)
                break

            current_input = f"SYSTEM FEEDBACK: Last action resulted in: {json.dumps(result)}. Proceed."

# --- BOOT SEQUENCE ---
if __name__ == "__main__":
    # 1. Create the communication queue
    cmd_queue = queue.Queue()
    
    # 2. Initialize the GUI (Main Thread)
    app = SystemZeroGUI(cmd_queue)
    
    # 3. Initialize the Agent (Pass the queue to it)
    agent = SystemZero(cmd_queue)
    
    # 4. Start the Agent in a Background Thread
    # daemon=True means the thread will die when you close the GUI window
    agent_thread = threading.Thread(target=agent.run, daemon=True)
    agent_thread.start()
    
    # 5. Start the UI Loop (Blocks the main thread, keeping window open)
    app.mainloop()