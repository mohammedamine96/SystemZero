import sys
import json
from src.brain import Brain
from src.parser import Parser
from src.dispatcher import Dispatcher

class SystemZero:
    def __init__(self):
        print(">> System Zero: Initializing modules...")
        self.brain = Brain()
        print(">> System Zero: Online. Waiting for command.")

    def run(self):
        while True:
            try:
                # 1. Input Interface
                user_input = input("\n[USER]: ")
                
                # Exit condition
                if user_input.lower() in ["exit", "quit", "shutdown"]:
                    print(">> System Zero: Shutting down.")
                    break

                # 2. Cognition (The Brain)
                print(">> Thinking...", end="\r")
                raw_response = self.brain.think(user_input)
                
                # 3. Parsing (The Filter)
                command = Parser.extract_command(raw_response)
                
                # Check for parsing errors
                if "error" in command:
                    print(f"\n[ERROR] Parser rejected response: {command['error']}")
                    continue

                # 4. Verification (Human-in-the-Loop)
                # CRITICAL SECURITY STEP: We show the user what we are about to do.
                print(f"\n[PLAN] Action: {command.get('action')}")
                print(f"[PLAN] Reason: {command.get('thought')}")
                
                confirm = input(">> Execute? (y/n): ")
                if confirm.lower() != 'y':
                    print(">> Action Aborted by User.")
                    continue

                # 5. Execution (The Body)
                result = Dispatcher.execute(command)
                
                # 6. Output
                print(f"\n[RESULT]:\n{json.dumps(result, indent=2)}")

            except KeyboardInterrupt:
                print("\n>> System Zero: Force Interrupt.")
                break
            except Exception as e:
                print(f"\n[CRITICAL FAILURE]: {e}")

if __name__ == "__main__":
    agent = SystemZero()
    agent.run()