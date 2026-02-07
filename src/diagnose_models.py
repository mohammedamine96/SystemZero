from google import genai
from config import Config

def list_raw_models():
    try:
        print("Authenticating...")
        client = genai.Client(api_key=Config.get_api_key())
        
        print("Querying Google AI for available models (Raw Mode)...")
        # We iterate and just print the name. No filtering.
        for model in client.models.list():
            print(f"FOUND: {model.name}")
            
    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")

if __name__ == "__main__":
    list_raw_models()