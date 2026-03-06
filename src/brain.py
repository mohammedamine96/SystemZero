import os
from groq import Groq
from google import genai  # <-- The brand new SDK!
from PIL import Image
from src.prompts import SYSTEM_INSTRUCTION
from dotenv import load_dotenv

load_dotenv()

class Brain:
    def __init__(self, model="llama-3.1-8b-instant"):
        print(f">> [BRAIN] Connecting Left Hemisphere to Groq ({model})...")
        try:
            # 1. Initialize Left Brain (Groq)
            self.groq_api_key = os.getenv("GROQ_API_KEY")
            if not self.groq_api_key:
                raise ValueError("GROQ_API_KEY is literally blank! Check your .env file.")
                
            self.client = Groq(api_key=self.groq_api_key)
            self.model = model 
            
            # 2. Initialize Right Brain (Gemini 2.5 Optical Nerve)
            self.gemini_api_key = os.getenv("GEMINI_API_KEY")
            if self.gemini_api_key:
                self.gemini_client = genai.Client(api_key=self.gemini_api_key)
                print(">> [BRAIN] Connecting Right Hemisphere to Gemini 2.5 Vision Engine...")
            else:
                print(">> [WARNING] GEMINI_API_KEY missing. Optical routing offline.")

            print(f">> [BRAIN] Neural Pathways Online.")
            
        except Exception as e:
            print(f"\n[CRITICAL] Connection Failed: {e}")
            raise e

    def think(self, prompt, image_path=None):
        """Processes logic. Routes to Gemini if visual data is present, otherwise uses Groq."""
        
        # --- RIGHT BRAIN: OPTICAL PROCESSING (GEMINI) ---
        if image_path and os.path.exists(image_path):
            print(f">> [OPTICAL NERVE] Routing image data to Gemini Vision Engine...")
            try:
                img = Image.open(image_path)
                full_prompt = f"{SYSTEM_INSTRUCTION}\n\nUSER PROMPT: {prompt}"
                
                # Use the new syntax for generating content
                response = self.gemini_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[img, full_prompt]
                )
                return response.text
                
            except Exception as e:
                print(f">> [OPTICAL ERROR] Gemini vision failed: {e}")
                return '{"thought": "I failed to process the image.", "action": "task_complete", "params": {"summary": "Optical cortex failure."}}'

        # --- LEFT BRAIN: TEXT LOGIC (GROQ) ---
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_INSTRUCTION},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f'{{"thought": "Groq API error: {e}", "action": "task_complete", "params": {{"summary": "API Limit reached."}}}}'