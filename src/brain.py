from google import genai
from google.genai import types
from src.config import Config
from src.prompts import SYSTEM_INSTRUCTION
import time
import PIL.Image
import os

class Brain:
    def __init__(self):
        self.client = genai.Client(api_key=Config.get_api_key())
        self.model_id = "gemini-flash-latest"
        
        self.chat = self.client.chats.create(
            model=self.model_id,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.0, 
            )
        )

    def think(self, user_input, image_path=None):
        """
        Processes text and optional image input.
        """
        try:
            time.sleep(1)
            
            # 1. Prepare Content
            content = [user_input]
            
            # 2. Attach Image (if present)
            if image_path:
                try:
                    # Security: Ensure image is in workspace
                    full_path = os.path.join("workspace", image_path)
                    if not os.path.exists(full_path):
                        return f'{{"thought": "Image not found.", "action": "error", "params": {{"details": "File {image_path} missing from workspace"}} }}'
                    
                    img = PIL.Image.open(full_path)
                    content.append(img)
                    print(f">> [System] Attached Vision Data: {image_path}")
                except Exception as e:
                    return f'{{"thought": "Image load error.", "action": "error", "params": {{"details": "{str(e)}"}} }}'

            # 3. Send to Brain
            response = self.chat.send_message(content)
            
            if not response.text:
                return '{"thought": "The model returned an empty response.", "action": "error", "params": {"details": "Empty Response"}}'
                
            return response.text
            
        except Exception as e:
            return f'{{"thought": "Connection failure.", "action": "error", "params": {{"details": "{str(e)}"}} }}'