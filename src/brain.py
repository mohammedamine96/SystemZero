from google import genai
from config import Config
import time

class Brain:
    def __init__(self):
        self.client = genai.Client(api_key=Config.get_api_key())
        # CHANGED: Using the generic alias. This is the safest bet for API stability.
        self.model_id = "gemini-flash-latest"

    def think(self, user_input):
        try:
            # We add a small safety buffer to prevent rapid-fire rate limits during testing
            time.sleep(1) 
            
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=user_input
            )
            return response.text
        except Exception as e:
            return f"ERROR_NEURAL_LINK: {e}"

if __name__ == "__main__":
    print(f"Initializing Neural Link (Model: gemini-flash-latest)...")
    core = Brain()
    print("Sending ping...")
    reply = core.think("You are SystemZero. Confirm operational status.")
    print(f"Response Received: {reply}")