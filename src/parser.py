import json
import re

class Parser:
    @staticmethod
    def extract_command(llm_response: str):
        """
        Strips markdown and parses JSON.
        Returns a dictionary or raises an error.
        """
        try:
            # 1. Clean the input
            # LLMs often wrap code in ```json ... ```. We need to strip that.
            clean_text = llm_response.strip()
            
            # Regex to find the JSON block if it's buried in text
            json_match = re.search(r"\{.*\}", clean_text, re.DOTALL)
            
            if json_match:
                clean_text = json_match.group(0)
            
            # 2. Parse
            command_data = json.loads(clean_text)
            
            # 3. Validate Structure (The Security Gate)
            required_keys = ["thought", "action", "params"]
            for key in required_keys:
                if key not in command_data:
                    raise ValueError(f"Missing protocol key: {key}")
            
            return command_data

        except json.JSONDecodeError:
            print(f"[PARSER ERROR] Raw Output: {llm_response}")
            return {"error": "Invalid JSON format received from Brain."}
        except Exception as e:
            return {"error": str(e)}

# Self-Diagnostic
if __name__ == "__main__":
    print("Testing Parser...")
    
    # Test 1: Perfect JSON
    raw_1 = '{"thought": "Testing system.", "action": "ping", "params": {}}'
    print(f"Test 1 (Clean): {Parser.extract_command(raw_1)}")
    
    # Test 2: Markdown wrapped (Common LLM behavior)
    raw_2 = """
    Here is the command:
    ```json
    {
      "thought": "I need to list files.",
      "action": "ls",
      "params": {"path": "."}
    }
    ```
    """
    print(f"Test 2 (Markdown): {Parser.extract_command(raw_2)}")