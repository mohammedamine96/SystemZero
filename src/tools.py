import os
import platform
import sys          
import subprocess
import requests
from bs4 import BeautifulSoup
import pyautogui 
from src.vision import Vision
from src.hands import Hands
import json
import webbrowser

GLOBAL_HANDS = Hands()
# Global instance so we don't reload the model every time
GLOBAL_EYES = Vision()

class Toolbox:
    @staticmethod
    def get_system_info():
        try:
            return {
                "system": platform.system(),
                "node": platform.node(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor()
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def list_directory(path="."):
        try:
            if not os.path.exists(path):
                return {"error": "Path does not exist."}
            return {"path": path, "files": os.listdir(path)}
        except Exception as e:
            return {"error": f"Access Denied: {e}"}

    @staticmethod
    def read_file(path):
        """Reads a text file."""
        try:
            if not path.startswith("workspace"):
                target_path = os.path.join("workspace", path)
            else:
                target_path = path

            if not os.path.exists(target_path):
                return {"error": f"File not found. (Looked at: {target_path})"}
            
            file_size = os.path.getsize(target_path)
            if file_size > 1024 * 1024:
                return {"error": f"File too large ({file_size} bytes). Limit is 1MB."}

            with open(target_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {"content": content[:2000] + "... (truncated)" if len(content) > 2000 else content}

        except Exception as e:
            return {"error": f"Read Failure: {e}"}
    
    @staticmethod
    def write_file(filename, content):
        try:
            if ".." in filename or "/" in filename or "\\" in filename:
                return {"error": "Security Violation: Write only to workspace root."}
            
            target_path = os.path.join("workspace", filename)
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return {"status": "success", "path": target_path, "bytes_written": len(content)}

        except Exception as e:
            return {"error": f"Write Failure: {e}"}

    @staticmethod
    def run_python_script(filename):
        try:
            if ".." in filename or "/" in filename or "\\" in filename:
                return {"error": "Security Violation."}
            
            target_path = os.path.join("workspace", filename)
            
            if not os.path.exists(target_path):
                return {"error": "Script not found."}

            result = subprocess.run(
                [sys.executable, target_path],
                capture_output=True,
                text=True,
                timeout=10 
            )
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "exit_code": result.returncode
            }

        except subprocess.TimeoutExpired:
            return {"error": "Script execution timed out."}
        except Exception as e:
            return {"error": f"Execution Failure: {e}"}
        
    @staticmethod
    def fetch_website_text(url):
        """Silently fetches and extracts readable text from a webpage."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Strip out scripts, styles, and navigation menus
            for element in soup(["script", "style", "header", "footer", "nav", "aside"]):
                element.extract()
                
            text = soup.get_text(separator=' ', strip=True)
            
            # Truncate to save the LLM's context window
            max_chars = 8000
            if len(text) > max_chars:
                text = text[:max_chars] + "... [TEXT TRUNCATED DUE TO LENGTH]"
                
            return {"status": "success", "url": url, "text_preview": text}
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to connect to the website: {e}"}
        except Exception as e:
            return {"error": f"Failed to parse the website: {e}"}

    @staticmethod
    def search_web(query):
        """Performs a web search using DuckDuckGo HTML."""
        try:
            url = "https://html.duckduckgo.com/html/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://html.duckduckgo.com/'
            }
            payload = {'q': query}

            response = requests.post(url, data=payload, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return {"error": f"Search Provider Error: {response.status_code}"}

            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for result in soup.find_all('div', class_='result', limit=5):
                title_tag = result.find('a', class_='result__a')
                if title_tag:
                    results.append({
                        "title": title_tag.get_text(strip=True),
                        "link": title_tag['href']
                    })

            if not results:
                return {"status": "success", "results": [], "message": "No results found."}

            return {"status": "success", "results": results}

        except Exception as e:
            return {"error": f"Search Failure: {e}"}

    @staticmethod
    def capture_screen(filename="vision_context.png"):
        """Captures the screen for the 'look' command."""
        try:
            target_path = os.path.join("workspace", filename)
            screenshot = pyautogui.screenshot()
            screenshot.save(target_path)
            return {"status": "success", "path": target_path}
        except Exception as e:
            return {"error": f"Screen Capture Failed: {e}"}
            
    @staticmethod
    def mouse_move(x, y):
        try:
            import pyautogui
            pyautogui.FAILSAFE = True 
            pyautogui.moveTo(x, y, duration=0.5) 
            return {"status": "success", "action": f"Moved to {x}, {y}"}
        except Exception as e:
            return {"error": f"Mouse Error: {e}"}

    @staticmethod
    def mouse_click(button="left"):
        try:
            import pyautogui
            if button == "double":
                pyautogui.doubleClick()
            else:
                pyautogui.click(button=button)
            return {"status": "success", "action": f"Clicked {button}"}
        except Exception as e:
            return {"error": f"Click Error: {e}"}

    @staticmethod
    def type_text(text):
        try:
            import pyautogui
            pyautogui.write(text, interval=0.05)
            return {"status": "success", "action": f"Typed: {text}"}
        except Exception as e:
            return {"error": f"Typing Error: {e}"}

    @staticmethod
    def press_key(key):
        try:
            import pyautogui
            pyautogui.press(key)
            return {"status": "success", "action": f"Pressed {key}"}
        except Exception as e:
            return {"error": f"Key Error: {e}"}
        
    @staticmethod
    def open_browser(url):
        try:
            clean_url = url.strip().strip('"').strip("'")
            if not clean_url.startswith("http"):
                clean_url = "https://" + clean_url
            webbrowser.open(clean_url)
            return {"status": "success", "action": f"Opened {clean_url}"}
        except Exception as e:
            return {"error": f"Browser Error: {e}"}
    
    @staticmethod
    def click_text(text, button="left"):
        try:
            print(f">> [TOOL] Looking for '{text}'...")
            coords = GLOBAL_EYES.find_element(text)

            if not coords:
                return {"status": "error", "message": f"Could not see text: '{text}' on screen."}

            import pyautogui
            pyautogui.moveTo(coords['x'], coords['y'], duration=0.5)
            pyautogui.click(button=button)

            return {
                "status": "success", 
                "action": f"Clicked '{text}' at ({coords['x']}, {coords['y']})"
            }
        except Exception as e:
            return {"error": f"Visual Click Failed: {e}"}
    
    @staticmethod
    def inspect_window():
        try:
            ui_tree = GLOBAL_HANDS.inspect_ui()
            return {
                "status": "success", 
                "observation": ui_tree
            }
        except Exception as e:
            return {"error": f"Inspection Failed: {e}"}

    @staticmethod
    def click_button_name(name):
        return GLOBAL_HANDS.click_element(name)

    @staticmethod
    def archive_memory(key, value):
        """Saves a fact to long-term memory."""
        file = "memory.json"
        data = {}
        if os.path.exists(file):
            with open(file, "r") as f:
                try: 
                    data = json.load(f)
                except json.JSONDecodeError: 
                    pass
        
        data[key.lower()] = value
        
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
            
        return {"status": "success", "message": f"Archived to memory: [{key} = {value}]"}

    @staticmethod
    def recall_memory(query):
        """Searches long-term memory for a keyword using fuzzy matching."""
        file = "memory.json"
        if not os.path.exists(file):
            return {"error": "Memory bank is empty."}
        
        with open(file, "r") as f:
            try: 
                data = json.load(f)
            except json.JSONDecodeError: 
                return {"error": "Memory bank corrupted."}
        
        results = {}
        query_words = query.lower().split()
        
        for key, value in data.items():
            searchable_text = f"{key} {value}".lower().replace("_", " ")
            if query.lower() in searchable_text or any(word in searchable_text for word in query_words if len(word) > 3):
                results[key] = value
                
        if results:
            return {"status": "success", "data": results}
            
        return {"error": f"No memories found matching '{query}'."}
        
    @staticmethod
    def get_weather(location):
        """Fetches current weather for a specific location using a free public API."""
        try:
            # wttr.in is a fantastic free API that returns JSON when you append ?format=j1
            url = f"https://wttr.in/{location}?format=j1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                temp_c = current['temp_C']
                desc = current['weatherDesc'][0]['value']
                
                return {
                    "status": "success", 
                    "location": location, 
                    "temperature_C": temp_c, 
                    "description": desc
                }
            else:
                return {"error": f"Weather API returned status {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Failed to fetch weather: {e}"}