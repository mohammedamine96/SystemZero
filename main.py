import sys
import json
import re
from src.brain import Brain
from src.parser import Parser
from src.dispatcher import Dispatcher

class SystemZero:
    def __init__(self):
        print(">> System Zero: Initializing modules...")
        self.brain = Brain()
        print(">> System Zero: Online (Autonomy Enabled).")

    def run(self):
        while True:
            try:
                user_input = input("\n[USER]: ")
                if user_input.lower() in ["exit", "quit", "shutdown"]:
                    break

                self.process_task(user_input)

            except KeyboardInterrupt:
                break

    def process_task(self, initial_input):
        current_input = initial_input
        trust_session = False
        error_count = 0 # Safety counter
        
        while True:
            # (Standard image/attachment logic)
            image_attachment = None
            match = re.search(r"@([\w\-\.]+)", current_input)
            if match:
                image_attachment = match.group(1)
                current_input = current_input.replace(f"@{image_attachment}", "").strip()

            print(">> Thinking...", end="\r")
            raw_response = self.brain.think(current_input, image_path=image_attachment)
            command = Parser.extract_command(raw_response)
            
            # --- SAFETY PATCH: ERROR BREAK ---
            if "error" in command and "Complete" not in command.get('thought', ''):
                error_count += 1
                if error_count > 2:
                    print(f"\n[CRITICAL]: System stuck in error loop. Terminating task.")
                    break
            else:
                error_count = 0 # Reset if we get a valid command
            # ---------------------------------

            if "error" in command and "Complete" in command.get('thought', ''):
                print(f"\n>> System Zero: {command.get('thought')}")
                break

            print(f"\n[PLAN] Action: {command.get('action')}")
            print(f"[PLAN] Reason: {command.get('thought')}")
            
            if not trust_session:
                confirm = input(">> Execute? (y / y! / n / stop): ")
                if confirm.lower() == 'y!':
                    trust_session = True
                elif confirm.lower() == 'stop':
                    break
                elif confirm.lower() != 'y':
                    break
            else:
                import time
                time.sleep(1) # Slow down trust mode to respect API limits
                print(">> [TRUST MODE] Executing automatically...")

            result = Dispatcher.execute(command)
            print(f"\n[RESULT]:\n{json.dumps(result, indent=2)}")

            current_input = f"SYSTEM FEEDBACK: Last action resulted in: {json.dumps(result)}. Proceed."

if __name__ == "__main__":
    agent = SystemZero()
    agent.run()