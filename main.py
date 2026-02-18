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
                        if self.ears.wait_for_wake_word("start"):
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
                    break

                # --- EXECUTION ---
                self.process_task(user_input, input_mode)

            except KeyboardInterrupt:
                break

    def process_task(self, initial_input, input_mode="text"):
        current_input = initial_input
        
        # --- GOD MODE CONFIGURATION ---
        # If in Voice Mode, we ENABLE TRUST automatically.
        # No confirmations. No waiting. Pure execution.
        if input_mode == "voice":
            trust_session = True
        else:
            trust_session = False # Text mode still asks for safety
            
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
            
            # SYSTEM ZERO SPEAKS THE PLAN
            thought_text = command.get('thought')
            if thought_text:
                print(f"[PLAN] Reason: {thought_text}")
                # It speaks the plan, then immediately acts (because trust_session is True)
                self.mouth.speak(thought_text, wait=True)

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
            
            # --- AUTHORIZATION GATE ---
            # This entire block is SKIPPED if trust_session is True
            if not trust_session:
                confirm = input(">> Execute? (y / y! / n / stop): ")
                if confirm.lower() == 'y!':
                    trust_session = True
                elif confirm.lower() == 'stop' or confirm.lower() == 'n':
                    break

            # (Trust Mode Execution)
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