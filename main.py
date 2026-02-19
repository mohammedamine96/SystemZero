import sys
import json
import re
import time
from src.brain import Brain
from src.parser import Parser
from src.dispatcher import Dispatcher
from src.tools import Toolbox
from src.ears import Ears
from src.mouth import Mouth

class SystemZero:
    def __init__(self):
        print(">> System Zero: Initializing modules...")
        self.brain = Brain()
        self.ears = Ears()
        print(">> System Zero: Online (Autonomy Enabled).")
        self.mouth = Mouth()

    def run(self):
        input_mode = "text"
        active_session = False 

        while True:
            try:
                user_input = None
                
                # --- INPUT HANDLING ---
                if input_mode == "text":
                    user_input = input("\n[USER]: ")
                    if user_input.lower().strip() == "voice":
                        input_mode = "voice"
                        print(">> [SYSTEM] Switched to VOICE MODE.")
                        continue

                elif input_mode == "voice":
                    # STATE 1: ASLEEP (Waiting for "Start")
                    if not active_session:
                        # Waits here for the keyword
                        if self.ears.wait_for_wake_word("zero"):
                            active_session = True
                            self.mouth.speak("I am listening, master amine", wait=True)
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
                    break

                # --- EXECUTION ---
                self.process_task(user_input, input_mode)

            except KeyboardInterrupt:
                break

    def process_task(self, initial_input, input_mode="text"):
        current_input = initial_input
        error_count = 0
        
        while True:
            # (Standard image logic)
            image_attachment = None
            match = re.search(r"@([\w\-\.]+)", current_input)
            if match:
                image_attachment = match.group(1)
                current_input = current_input.replace(f"@{image_attachment}", "").strip()

            print(">> Thinking...", end="\r")
            raw_response = self.brain.think(current_input, image_path=image_attachment)
            command = Parser.extract_command(raw_response)
            
            # --- 🚀 DEFAULT TO GOD MODE ---
            # We trust the agent completely by default now, for both Text and Voice
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
            
            # SYSTEM ZERO SPEAKS THE PLAN
            if thought_text:
                print(f"[PLAN] Reason: {thought_text}")
                if not is_dangerous:
                    self.mouth.speak(thought_text, wait=True)
                else:
                    self.mouth.speak(f"The plan is: {thought_text}", wait=True)

            # (Error Loop Protection)
            if "error" in command and "Complete" not in command.get('thought', ''):
                error_count += 1
                if error_count > 2:
                    print(f"\n[CRITICAL]: System stuck in loop. Terminating.")
                    self.mouth.speak("I am stuck. Aborting task.", wait=True)
                    break
            else:
                error_count = 0 

            if command.get("status") == "task_complete":
                print(f"\n>> [MISSION ACCOMPLISHED]: {command.get('summary')}")
                break

            print(f"\n[PLAN] Action: {command.get('action')}")
            
            # --- 🛑 AUTHORIZATION GATE (Triggers ONLY if trust_session is False) ---
            if not trust_session:
                if input_mode == "text":
                    confirm = input(">> Execute? (y / n / stop): ")
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
            
            if result.get("status") == "task_complete":
                break

            current_input = f"SYSTEM FEEDBACK: Last action resulted in: {json.dumps(result)}. Proceed."

if __name__ == "__main__":
    agent = SystemZero()
    agent.run()