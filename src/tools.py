import os
import platform
import sys          
import subprocess
import requests
from bs4 import BeautifulSoup
import pyautogui 
from src.vision import Vision
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
        """
        Reads a text file.
        SECURITY: Enforces workspace lock and size limits.
        """
        try:
            # FIX: Automatically enforce workspace path
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
                timeout=10 # Increased timeout slightly
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
    def fetch_url(url):
        try:
            if not url.startswith("http"):
                return {"error": "Invalid URL."}

            headers = {'User-Agent': 'SystemZero/1.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return {"error": f"HTTP Error: {response.status_code}"}

            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text()
            
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return {
                "url": url,
                "status": "success",
                "content": clean_text[:4000] + "... (truncated)" if len(clean_text) > 4000 else clean_text
            }

        except Exception as e:
            return {"error": f"Fetch Failure: {e}"}

    @staticmethod
    def search_web(query):
        """
        Performs a web search using DuckDuckGo HTML.
        """
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
        """
        Captures the screen for the 'look' command.
        """
        try:
            target_path = os.path.join("workspace", filename)
            screenshot = pyautogui.screenshot()
            screenshot.save(target_path)
            return {"status": "success", "path": target_path}
        except Exception as e:
            return {"error": f"Screen Capture Failed: {e}"}
            
    @staticmethod
    def archive_memory(key, value):
        import json
        memory_file = "workspace/memory.json"
        try:
            data = {}
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    data = json.load(f)
            data[key] = value
            with open(memory_file, 'w') as f:
                json.dump(data, f, indent=2)
            return {"status": "success", "message": f"Memorized {key}"}
        except Exception as e:
            return {"error": f"Archive Failure: {e}"}
        
    @staticmethod
    def mouse_move(x, y):
        """
        Moves the cursor to specific coordinates.
        params: x (int), y (int)
        """
        try:
            import pyautogui
            # Safety: Fail-safe triggers if mouse is slammed to a corner
            pyautogui.FAILSAFE = True 
            pyautogui.moveTo(x, y, duration=0.5) # duration prevents instant teleportation
            return {"status": "success", "action": f"Moved to {x}, {y}"}
        except Exception as e:
            return {"error": f"Mouse Error: {e}"}

    @staticmethod
    def mouse_click(button="left"):
        """
        Clicks the mouse.
        params: button ("left", "right", "double")
        """
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
        """
        Types text on the keyboard.
        params: text (str)
        """
        try:
            import pyautogui
            pyautogui.write(text, interval=0.05) # interval makes it look natural
            return {"status": "success", "action": f"Typed: {text}"}
        except Exception as e:
            return {"error": f"Typing Error: {e}"}

    @staticmethod
    def press_key(key):
        """
        Presses a specific key (e.g., 'enter', 'win', 'tab').
        params: key (str)
        """
        try:
            import pyautogui
            pyautogui.press(key)
            return {"status": "success", "action": f"Pressed {key}"}
        except Exception as e:
            return {"error": f"Key Error: {e}"}
        
    @staticmethod
    def open_browser(url):
        """
        Opens the default web browser to a specific URL.
        SECURITY: This bypasses GUI typing errors (like autocomplete).
        """
        import webbrowser
        try:
            # We strip quotes just in case the LLM hallucinates them
            clean_url = url.strip().strip('"').strip("'")
            
            if not clean_url.startswith("http"):
                clean_url = "https://" + clean_url
                
            webbrowser.open(clean_url)
            return {"status": "success", "action": f"Opened {clean_url}"}
        except Exception as e:
            return {"error": f"Browser Error: {e}"}
    
    @staticmethod
    def click_text(text, button="left"):
        """
        Scans the screen for text and clicks it.
        params: text (str), button ("left", "right")
        """
        try:
            print(f">> [TOOL] Looking for '{text}'...")
            coords = GLOBAL_EYES.find_element(text)

            if not coords:
                return {"status": "error", "message": f"Could not see text: '{text}' on screen."}

            # Move and Click
            import pyautogui
            pyautogui.moveTo(coords['x'], coords['y'], duration=0.5)
            pyautogui.click(button=button)

            return {
                "status": "success", 
                "action": f"Clicked '{text}' at ({coords['x']}, {coords['y']})"
            }
        except Exception as e:
            return {"error": f"Visual Click Failed: {e}"}