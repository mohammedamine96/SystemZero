import sys
import json
import re
import time
from src.brain import Brain
from src.parser import Parser
from src.dispatcher import Dispatcher
from src.tools import Toolbox
from src.ears import Ears  # <--- NEW MODULE
from src.mouth import Mouth
class SystemZero:
    def __init__(self):
        print(">> System Zero: Initializing modules...")
        self.brain = Brain()
        # Initialize Ears immediately
        self.ears = Ears()
        print(">> System Zero: Online (Autonomy Enabled).")
        self.mouth = Mouth()

    def run(self):
        input_mode = "text" # Default to safety

        while True:
            try:
                user_input = None
                
                # --- INPUT HANDLING ---
                if input_mode == "text":
                    user_input = input("\n[USER]: ")
                    
                    # Command to switch modes
                    if user_input.lower().strip() == "voice":
                        input_mode = "voice"
                        print(">> [SYSTEM] Switched to VOICE MODE. Say 'Switch to text' to exit.")
                        continue

                elif input_mode == "voice":
                    # Listen for audio
                    user_input = self.ears.listen()
                    
                    # If silence or error, loop back
                    if not user_input:
                        continue
                        
                    # Voice command to switch back
                    if "switch to text" in user_input.lower():
                        input_mode = "text"
                        print(">> [SYSTEM] Switched to TEXT MODE.")
                        continue

                if not user_input:
                    continue
                
                # Exit check
                if user_input.lower() in ["exit", "quit", "shutdown"]:
                    break

                # --- VISION TRIGGER (Look) ---
                if user_input.lower().strip() == "look":
                    print(">> [EYES] Capturing visual context...", end="\r")
                    try:
                        cap_result = Toolbox.capture_screen("vision_context.png")
                        if "error" in cap_result:
                            print(f"\n[ERROR] {cap_result['error']}")
                            continue
                        print(">> [EYES] Context captured. Processing...")
                        user_input = "Analyze the screen state in @vision_context.png."
                    except Exception as e:
                        print(f"\n[ERROR] Vision Failed: {e}")
                        continue
                
                # --- EXECUTION ---
                self.process_task(user_input)

            except KeyboardInterrupt:
                break

    def process_task(self, initial_input):
        current_input = initial_input
        trust_session = False
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
            # SYSTEM ZERO SPEAKS THE THOUGHT
            thought_text = command.get('thought')
            if thought_text:
                self.mouth.speak(thought_text)
            # (Standard Error Loop Protection)
            if "error" in command and "Complete" not in command.get('thought', ''):
                error_count += 1
                if error_count > 2:
                    print(f"\n[CRITICAL]: System stuck in error loop. Terminating task.")
                    break
            else:
                error_count = 0 

            # (Standard Stop/Task Complete Logic)
            if command.get("status") == "task_complete":
                print(f"\n>> [MISSION ACCOMPLISHED]: {command.get('summary')}")
                break

            if "error" in command and "Complete" in command.get('thought', ''):
                print(f"\n>> System Zero: {command.get('thought')}")
                break

            print(f"\n[PLAN] Action: {command.get('action')}")
            print(f"[PLAN] Reason: {command.get('thought')}")
            
            # (Execution Gate)
            if not trust_session:
                confirm = input(">> Execute? (y / y! / n / stop): ")
                if confirm.lower() == 'y!':
                    trust_session = True
                elif confirm.lower() == 'stop':
                    break
                elif confirm.lower() != 'y':
                    break
            else:
                time.sleep(1)
                print(">> [TRUST MODE] Executing automatically...")

            result = Dispatcher.execute(command)
            print(f"\n[RESULT]:\n{json.dumps(result, indent=2)}")
            
            # (Stop if task complete action returned success)
            if result.get("status") == "task_complete":
                break

            current_input = f"SYSTEM FEEDBACK: Last action resulted in: {json.dumps(result)}. Proceed."

if __name__ == "__main__":
    agent = SystemZero()
    agent.run()