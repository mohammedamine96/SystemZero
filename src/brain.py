from google import genai
from google.genai import types
# FIXED IMPORTS: pointing to src.config and src.prompts
from src.config import Config
from src.prompts import SYSTEM_INSTRUCTION
import time

class Brain:
    def __init__(self):
        self.client = genai.Client(api_key=Config.get_api_key())
        self.model_id = "gemini-flash-latest"

    def think(self, user_input):
        try:
            time.sleep(1)
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.0,
                )
            )
            return response.text
        except Exception as e:
            return f'{{"thought": "Connection failure.", "action": "error", "params": {{"details": "{str(e)}"}} }}'

# NOTE: Because we changed imports, running this file directly now requires:
# python -m src.brain (from the root folder)
if __name__ == "__main__":
    print("Initializing System Zero (Mode: JSON Strict)...")
    core = Brain()
    print("\n[TEST] Command: 'Check files.'")
    print(core.think("Check files."))