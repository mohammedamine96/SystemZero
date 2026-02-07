import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    _api_key = os.getenv("GEMINI_API_KEY")

    @classmethod
    def get_api_key(cls):
        if not cls._api_key:
            print("CRITICAL ERROR: GEMINI_API_KEY not found in .env")
            print("System halted to prevent unauthorized null-authentication attempts.")
            sys.exit(1)
        return cls._api_key

# Sanity Check when running this file directly
if __name__ == "__main__":
    print(f"Environment Check: API Key loaded successfully. Length: {len(Config.get_api_key())}")