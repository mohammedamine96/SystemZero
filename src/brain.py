import os
import json
from groq import Groq
from dotenv import load_dotenv
from src.prompts import SYSTEM_INSTRUCTION

# FORCE LOAD .ENV
load_dotenv()

class Brain:
    def __init__(self):
        print(">> [BRAIN] Connecting to Groq Cloud (Llama 3.3)...")
        try:
            self.api_key = os.getenv("GROQ_API_KEY")
            
            if not self.api_key:
                # If .env fails, check if the user pasted it directly
                # (Safety fallback)
                print(">> [WARNING] GROQ_API_KEY not found in .env")
                self.api_key = input("Enter Groq API Key: ").strip()

            self.client = Groq(api_key=self.api_key)
            
            # --- THE FIX IS HERE ---
            # We switched from the dead 'llama3-70b-8192' to 'llama-3.3-70b-versatile'
            self.model = "llama-3.3-70b-versatile" 
            # -----------------------
            
            self.history = []
            
            # Connection Test
            print(f">> [BRAIN] Pinging {self.model}...")
            self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "hi"}]
            )
            print(f">> [BRAIN] Online. Running on {self.model}.")
            
        except Exception as e:
            print(f"\n[CRITICAL] Connection Failed: {e}")
            raise e

    def think(self, user_input, image_path=None):
        # 1. Vision Warning
        if image_path:
             user_input += f" [System Note: User attached image '{image_path}' but you are text-only.]"

        # 2. History Management
        self.history.append({'role': 'user', 'content': user_input})
        if len(self.history) > 10:
            self.history = self.history[-10:]

        # 3. Inference
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': SYSTEM_INSTRUCTION},
                    *self.history
                ],
                temperature=0.1,
                # We enable JSON mode for Llama 3.3 as it supports it perfectly
                response_format={"type": "json_object"} 
            )

            response_text = completion.choices[0].message.content
            
            # 4. Save
            self.history.append({'role': 'assistant', 'content': response_text})
            return response_text

        except Exception as e:
            # --- DEBUG BLOCK ---
            print(f"\n[BRAIN ERROR DETAILS]: {e}") 
            # -------------------
            return json.dumps({
                "action": "error",
                "thought": "Groq Brain Failure",
                "params": {"details": str(e)}
            })