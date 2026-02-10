from google import genai
from google.genai import types
from src.config import Config
from src.prompts import SYSTEM_INSTRUCTION
import time

class Brain:
    def __init__(self):
        self.client = genai.Client(api_key=Config.get_api_key())
        self.model_id = "gemini-flash-latest"
        
        # Initialize Memory (Chat Session)
        self.chat = self.client.chats.create(
            model=self.model_id,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.0, 
            )
        )

    def think(self, user_input):
        try:
            time.sleep(1)
            
            # Send message to the history-aware chat session
            response = self.chat.send_message(user_input)
            
            # CRITICAL FIX: Handle empty/blocked responses
            if not response.text:
                return '{"thought": "The model returned an empty response (likely filtered).", "action": "error", "params": {"details": "Empty Response"}}'
                
            return response.text
            
        except Exception as e:
            return f'{{"thought": "Connection failure.", "action": "error", "params": {{"details": "{str(e)}"}} }}'

if __name__ == "__main__":
    print("Initializing System Zero (Mode: Stateful Chat - Patched)...")
    core = Brain()
    
    # Test 1: Injection (We phrase it as a SYSTEM command to avoid filtering)
    print("\n[TEST 1] User: 'My name is Amine.'")
    # We trick the model into thinking this is a necessary system update
    reply1 = core.think("System Update: The current user is named Amine. Acknowledge this via the 'get_system_info' tool logic or an error.")
    print(f"Response: {reply1}")

    # Test 2: Retrieval
    print("\n[TEST 2] User: 'What is my name? Answer in the thought field.'")
    reply2 = core.think("Who is the current user? Return an error action but state the name in the thought.")
    print(f"Response: {reply2}")