import os
import platform
import sys          
import subprocess
import requests
from bs4 import BeautifulSoup
import pyautogui 
import threading
from src.vision import Vision
from src.hands import Hands
import json
import webbrowser
import urllib.parse
import time

time.sleep(3)

GLOBAL_HANDS = Hands()
# Global instance so we don't reload the model every time
GLOBAL_EYES = Vision()

from src.memory import SemanticMemory
GLOBAL_MEMORY = SemanticMemory()

class Toolbox:

    # Dictionary to keep track of background Watcher threads
    ACTIVE_WATCHERS = {}

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
    def archive_memory(fact):
        """Saves a natural language fact to the vector database."""
        try:
            return GLOBAL_MEMORY.memorize(fact)
        except Exception as e:
            return {"error": f"Memory Archive Failed: {e}"}

    @staticmethod
    def recall_memory(query):
        """Searches the vector database for semantic matches."""
        try:
            return GLOBAL_MEMORY.recall(query)
        except Exception as e:
            return {"error": f"Memory Recall Failed: {e}"}
        
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
    
    @staticmethod
    def control_media(command):
        """Controls system volume and media playback directly via OS hooks."""
        try:
            import pyautogui
            # The exact key codes Windows uses for media control
            valid_commands = ["volumeup", "volumedown", "volumemute", "playpause", "nexttrack", "prevtrack"]
            
            command = command.lower().replace(" ", "").replace("_", "")
            
            # Map friendly names to actual key codes
            if command in ["mute", "unmute"]: command = "volumemute"
            elif command in ["up", "louder"]: command = "volumeup"
            elif command in ["down", "quieter"]: command = "volumedown"
            elif command in ["play", "pause", "stop"]: command = "playpause"
            elif command in ["next", "skip"]: command = "nexttrack"
            elif command in ["previous", "prev", "back"]: command = "prevtrack"

            if command in valid_commands:
                # If adjusting volume, press it 5 times so the change is actually noticeable (10% change)
                if command in ["volumeup", "volumedown"]:
                    pyautogui.press(command, presses=5)
                else:
                    pyautogui.press(command)
                return {"status": "success", "action": f"Executed OS media command: {command}"}
            else:
                return {"error": f"Invalid command. Valid native keys: {valid_commands}"}
                
        except Exception as e:
            return {"error": f"Media control failed: {e}"}
        
    @staticmethod
    def send_whatsapp(phone_number, message):
        """Automates WhatsApp Web using Spatially-Filtered Optical DOM Verification."""
        try:
            import urllib.parse
            import webbrowser
            import pyautogui
            import time

            clean_number = phone_number.replace(" ", "")
            if not clean_number.startswith("+"):
                return {"error": "Phone number must include the country code."}

            encoded_msg = urllib.parse.quote(message)
            url = f"https://web.whatsapp.com/send?phone={clean_number}&text={encoded_msg}"
            
            print(f">> [COMMUNICATOR] Opening WhatsApp Web for {clean_number}...")
            webbrowser.open(url)
            
            print(">> [COMMUNICATOR] Awaiting browser window...")
            window_found = False
            for _ in range(15):
                time.sleep(1)
                window = GLOBAL_HANDS.get_active_window()
                if window and "WhatsApp" in window.window_text():
                    window_found = True
                    break
                    
            if not window_found:
                return {"error": "Timeout: Browser did not open WhatsApp."}
                
            print(">> [COMMUNICATOR] Window active. Engaging Optical Nerve (Spatial Filter Active)...")
            
            first_word = message.split()[0].lower()
            rendered = False
            screen_height = pyautogui.size().height
            
            # Poll vision 8 times (allowing ~12 seconds for the DOM to load)
            for _ in range(8):
                time.sleep(1.5)
                coords = GLOBAL_EYES.find_element(first_word)
                
                # --- v6.2 ARCHITECTURE: THE SPATIAL FILTER ---
                # We ignore any text found in the top 30% of the screen (the URL address bar)
                if coords and coords['y'] > (screen_height * 0.3):
                    print(f">> [COMMUNICATOR] Visual confirmation: Text '{first_word}' detected in lower chat canvas (Y-axis: {coords['y']}).")
                    rendered = True
                    break
                elif coords:
                    print(f">> [COMMUNICATOR] Discarding false-positive in upper screen (URL bar) at Y-axis: {coords['y']}")
                    
            if not rendered:
                print(">> [COMMUNICATOR WARNING] Optical verify failed. Applying 8-second fallback delay...")
                time.sleep(8)
            else:
                # A micro-delay to ensure the send button event listener is fully bound to the DOM
                time.sleep(1.5) 
            
            print(">> [COMMUNICATOR] Injecting 'Enter' key to send...")
            pyautogui.press('enter')
            
            # Wait 3 seconds for the network request to actually fire before closing the tab
            time.sleep(3)
            pyautogui.hotkey('ctrl', 'w')
            
            return {"status": "success", "message": f"WhatsApp message sent to {clean_number}."}
            
        except Exception as e:
            return {"error": f"WhatsApp automation failed: {e}"}
        
    @staticmethod
    def set_reminder(minutes, message):
        """Sets a background timer that speaks a message when time is up."""
        try:
            seconds = float(minutes) * 60

            def reminder_callback():
                print(f"\n>> [CHRONOS] ⏰ ALARM TRIGGERED: {message}")
                
                # Play a system alert chime
                try:
                    import winsound
                    winsound.MessageBeep(winsound.MB_ICONASTERISK)
                except:
                    pass
                
                # Use a native PowerShell hidden thread to speak the alarm
                # This ensures we don't crash the main System Zero voice engine!
                safe_msg = message.replace("'", "").replace('"', '')
                ps_command = f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'Pardon the interruption, Operator. Reminder: {safe_msg}\');"'
                import os
                os.system(ps_command)

            # Start the background thread
            t = threading.Timer(seconds, reminder_callback)
            t.daemon = True # Ensures the timer dies if you close the program
            t.start()

            return {"status": "success", "message": f"Timer set for {minutes} minutes."}
        except Exception as e:
            return {"error": f"Failed to set timer: {e}"}

    @staticmethod
    def analyze_screen(question="Describe what is on the screen."):
        """Takes a screenshot and uses a Vision-Language Model to understand it conceptually."""
        try:
            import base64
            import io
            import os
            import requests
            import pyautogui
            from PIL import Image

            print(">> [EYES] Capturing visual field for deep analysis...")
            
            # 1. Capture the screen and FORCE it to RGB (Strips out invisible Alpha channels)
            screenshot = pyautogui.screenshot().convert("RGB")
            
            # 2. Resize and compress the image
            screenshot.thumbnail((1024, 1024))
            buffered = io.BytesIO()
            screenshot.save(buffered, format="JPEG", quality=80)
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            api_key = os.environ.get("GROQ_API_KEY")
            if not api_key:
                return {"error": "GROQ_API_KEY not found in environment."}

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": question},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
                        ]
                    }
                ],
                "temperature": 0.5,
                "max_completion_tokens": 1024 # Updated to Groq's new standard parameter
            }

            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
            
            # --- THE DIAGNOSTIC FIX ---
            # If Groq rejects the payload, print the EXACT reason why
            if response.status_code != 200:
                print(f"\n>> [EYES] API REJECTION DATA: {response.text}\n")
                return {"error": f"Groq Vision Error {response.status_code}: {response.text}"}
                
            data = response.json()
            vision_text = data["choices"][0]["message"]["content"]
            print(f">> [EYES] Analysis complete.")
            
            return {"status": "success", "analysis": vision_text}
            
        except Exception as e:
            return {"error": f"Deep Vision analysis failed: {e}"}

    @staticmethod
    def check_system_health():
        """Monitors CPU, RAM, and top running processes."""
        try:
            import psutil
            # Get CPU and RAM percentages
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            
            # Find the top 3 memory-hogging processes
            processes = []
            for proc in psutil.process_iter(['name', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by memory usage and grab the top 3
            processes = sorted(processes, key=lambda p: p['memory_percent'] or 0, reverse=True)[:3]
            top_procs = [f"{p['name']} ({p['memory_percent']:.1f}% RAM)" for p in processes]
            
            return {
                "status": "success",
                "cpu_usage_percent": cpu,
                "ram_usage_percent": ram,
                "top_processes": top_procs
            }
        except Exception as e:
            return {"error": f"Health check failed: {e}"}

    @staticmethod
    def kill_process(process_name):
        """Terminates a running background process by name."""
        try:
            import psutil
            killed = 0
            # Search for any process matching the name and terminate it
            for proc in psutil.process_iter(['name']):
                if process_name.lower() in str(proc.info['name']).lower():
                    proc.kill()
                    killed += 1
            
            if killed > 0:
                return {"status": "success", "message": f"Terminated {killed} instance(s) of {process_name}."}
            else:
                return {"error": f"Process '{process_name}' not found running."}
        except Exception as e:
            return {"error": f"Failed to kill process: {e}"}
    
    @staticmethod
    def read_pdf(filename):
        """Reads and extracts text from a PDF document in the workspace using PyPDF2."""
        try:
            import PyPDF2
            import os
            
            # Ensure we are looking in the workspace folder
            target_path = os.path.join("workspace", filename)
            if not os.path.exists(target_path):
                return {"error": f"PDF not found at: {target_path}"}
            
            print(f">> [SCHOLAR] Ingesting binary document via PyPDF2: {filename}...")
            
            text = ""
            # Open the file in binary read mode
            with open(target_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                
                # Extract text from every page
                for i in range(num_pages):
                    page = reader.pages[i]
                    extracted = page.extract_text()
                    if extracted:
                        text += f"\n--- Page {i + 1} ---\n"
                        text += extracted
            
            # Truncate if the PDF is absurdly long (protects the Brain's memory limit)
            max_chars = 15000 
            if len(text) > max_chars:
                text = text[:max_chars] + "\n... [TEXT TRUNCATED DUE TO LENGTH]"
                
            print(f">> [SCHOLAR] Extraction complete. Processed {num_pages} pages.")
            return {"status": "success", "filename": filename, "content": text}
            
        except ImportError:
            return {"error": "PyPDF2 is not installed. Run: pip install PyPDF2"}
        except Exception as e:
            return {"error": f"Failed to read PDF: {e}"}
    
    @staticmethod
    def start_watcher(name, interval_minutes, code_script):
        """Runs a Python script every X minutes. If it prints 'ALERT:', it speaks."""
        try:
            import os
            import time
            import subprocess
            import sys
            
            # Setup a dedicated folder for watcher scripts
            watchers_dir = os.path.join("workspace", "watchers")
            os.makedirs(watchers_dir, exist_ok=True)
            
            script_path = os.path.join(watchers_dir, f"{name}.py")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(code_script)

            # Stop the old watcher if it has the same name
            if name in Toolbox.ACTIVE_WATCHERS:
                Toolbox.ACTIVE_WATCHERS[name]["running"] = False 
            
            def watcher_loop():
                print(f"\n>> [WATCHER] 👁️ '{name}' online (Checking every {interval_minutes}m).")
                while Toolbox.ACTIVE_WATCHERS.get(name, {}).get("running", False):
                    try:
                        # Run the script the LLM wrote
                        result = subprocess.run(
                            [sys.executable, script_path], 
                            capture_output=True, text=True, timeout=30
                        )
                        output = result.stdout.strip()
                        
                        # If the script triggers an alert, interrupt the user!
                        if "ALERT:" in output:
                            alert_msg = output.split("ALERT:")[1].strip().split("\n")[0]
                            print(f"\n>> [WATCHER ALERT] '{name}': {alert_msg}")
                            
                            try:
                                import winsound
                                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                            except: pass
                            
                            safe_msg = alert_msg.replace("'", "").replace('"', '')
                            ps_command = f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'Watcher Alert: {safe_msg}\');"'
                            os.system(ps_command)
                            
                    except Exception as e:
                        print(f"\n>> [WATCHER ERROR] '{name}' failed: {e}")
                    
                    # Sleep until the next check
                    time.sleep(float(interval_minutes) * 60)

            # Register and start the background thread
            Toolbox.ACTIVE_WATCHERS[name] = {"running": True}
            t = threading.Thread(target=watcher_loop, daemon=True)
            t.start()
            
            return {"status": "success", "message": f"Watcher '{name}' started successfully."}
        except Exception as e:
            return {"error": f"Failed to start watcher: {e}"}

    @staticmethod
    def stop_watcher(name):
        """Terminates a background watcher."""
        if name in Toolbox.ACTIVE_WATCHERS:
            Toolbox.ACTIVE_WATCHERS[name]["running"] = False
            del Toolbox.ACTIVE_WATCHERS[name]
            return {"status": "success", "message": f"Watcher '{name}' terminated."}
        return {"error": f"Watcher '{name}' not found."}

    @staticmethod
    def list_watchers():
        """Lists all active background tasks."""
        active = [k for k, v in Toolbox.ACTIVE_WATCHERS.items() if v["running"]]
        return {"status": "success", "active_watchers": active}
    
    @staticmethod
    def build_new_tool(tool_name, prompt_signature, prompt_description, full_python_code):
        """Permanently injects a new capability into System Zero's source code with strict AST linting."""
        import os
        import ast
        
        print(f">> [ARCHITECT] Splicing new DNA: {tool_name}...")
        
        # --- v6.0 SAFETY LINTER ---
        try:
            # Statically parse the code to ensure it won't brick the interpreter
            ast.parse(full_python_code)
        except SyntaxError as e:
            print(f">> [ARCHITECT FATAL] Syntax Error detected in new DNA: {e}")
            return {"error": f"v6.0 Linter Blocked Injection: Syntax error in generated code -> {e}"}
            
        # Enforce Architect Protocol constraints
        if "@staticmethod" not in full_python_code:
            return {"error": "v6.0 Linter Blocked Injection: The required @staticmethod decorator is missing."}
            
        try:
            # 1. Inject the code into tools.py
            tools_path = os.path.join("src", "tools.py")
            with open(tools_path, "a", encoding="utf-8") as f:
                f.write(f"\n    # --- DYNAMICALLY BUILT TOOL: {tool_name} ---\n")
                f.write(full_python_code)
                f.write("\n")

            # 2. Inject the prompt into prompts.py so zero remembers the capability
            prompts_path = os.path.join("src", "prompts.py")
            with open(prompts_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Find the [SYSTEM] tag and insert the new tool documentation right above it
            new_prompt = f"- {tool_name}: {prompt_signature}\n    -> {prompt_description}\n\n[SYSTEM]"
            content = content.replace("[SYSTEM]", new_prompt)

            with open(prompts_path, "w", encoding="utf-8") as f:
                f.write(content)

            return {
                "status": "success", 
                "message": f"Sovereign evolution successful. '{tool_name}' installed. Inform the operator to restart the dashboard."
            }
        except Exception as e:
            return {"error": f"Evolution failed during file modification: {e}"}

    @staticmethod
    def generate_password(length=16):
        import string
        import secrets
        import pyperclip
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))
        pyperclip.copy(password)
        return {'password': password}
    
    @staticmethod
    def send_mobile_alert(message):
        """Sends a secure Telegram message to the Operator's phone."""
        try:
            import os
            import requests
            token = os.getenv("TELEGRAM_BOT_TOKEN")
            chat_id = os.getenv("TELEGRAM_CHAT_ID")
            
            if not token or not chat_id:
                return {"error": "Telegram credentials missing in .env."}
            
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {"chat_id": chat_id, "text": message}
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                return {"status": "success", "message": "Mobile alert transmitted."}
            else:
                return {"error": f"Transmission Failed: {response.text}"}
        except Exception as e:
            return {"error": f"Mobile Uplink Error: {e}"}
        
    @staticmethod
    def record_lesson(problem_context, solution_learned):
        """Archives a learned lesson into the vector database to prevent future mistakes."""
        try:
            # We format this specifically so the semantic search easily catches it next time
            lesson_fact = f"LESSON LEARNED: When attempting to '{problem_context}', the correct approach is to: '{solution_learned}'. Do not repeat past failures."
            
            # Send it directly to the Hippocampus
            result = GLOBAL_MEMORY.memorize(lesson_fact)
            
            if result.get("status") == "success":
                print(f">> [NEURAL FEEDBACK] New synaptic pathway formed: {problem_context}")
                return {"status": "success", "message": "Lesson permanently embedded in neural memory."}
            else:
                return {"error": "Failed to embed lesson."}
        except Exception as e:
            return {"error": f"Reflection Error: {e}"}
        
    @staticmethod
    def delegate_task(role, task_description):
        """Spawns an autonomous sub-agent in a background thread to handle a complex task."""
        try:
            import threading
            
            def swarm_worker():
                print(f"\n>> [HIVE MIND] 🐝 Spawning Sub-Agent: {role}...")
                
                # Import the Brain to create a clone
                from src.brain import Brain
                from src.parser import Parser
                from src.dispatcher import Dispatcher
                
                worker_brain = Brain(model="llama-3.1-8b-instant")
                
                # Give the child a hyper-focused prompt
                focus_prompt = f"You are a Sub-Agent of System Zero. Your role is: {role}. Your sole objective is: {task_description}. Use your tools to accomplish this. When finished, use the 'archive_memory' tool to permanently save your final report/findings so the Master Brain can read it later. Then use 'task_complete'."
                
                current_input = focus_prompt
                error_count = 0
                
                while True:
                    raw_response = worker_brain.think(current_input)
                    command = Parser.extract_command(raw_response)
                    
                    if "error" in command:
                        error_count += 1
                        if error_count > 2:
                            print(f">> [HIVE MIND] 🐝 Sub-Agent '{role}' failed and terminated.")
                            break
                    else:
                        error_count = 0
                        
                    result = Dispatcher.execute(command)
                    
                    if result.get("status") == "task_complete":
                        print(f"\n>> [HIVE MIND] 🐝 Sub-Agent '{role}' completed its objective and assimilated data into the Hive.")
                        break
                        
                    current_input = f"SYSTEM FEEDBACK: Last action resulted in: {result}. Continue your objective."

            # Start the child agent in the background so it doesn't block the Master Brain!
            t = threading.Thread(target=swarm_worker, daemon=True)
            t.start()
            
            return {"status": "success", "message": f"Sub-Agent '{role}' dispatched. It will work in the background and archive its findings in memory."}
            
        except Exception as e:
            return {"error": f"Failed to spawn swarm agent: {e}"}
        
    @staticmethod
    def deep_web_scrape(url, click_selector=None):
        """Uses a headless Chromium browser to render JavaScript and interact with dynamic webpages."""
        try:
            from playwright.sync_api import sync_playwright
            
            print(f">> [PUPPETEER] Spinning up headless Chromium engine for {url}...")
            
            with sync_playwright() as p:
                # Launch headless browser
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Go to the URL and wait for the network to be mostly idle (JS loaded)
                page.goto(url, wait_until="networkidle", timeout=30000)
                
                # If the Brain decided it needs to click a button (like "Accept Cookies" or "Read More")
                if click_selector:
                    try:
                        print(f">> [PUPPETEER] Attempting to click selector: {click_selector}")
                        page.click(click_selector, timeout=5000)
                        page.wait_for_timeout(2000) # Wait 2 seconds for the click to trigger JS changes
                    except Exception as e:
                        print(f">> [PUPPETEER WARNING] Could not click '{click_selector}': {e}")
                
                # Extract the rendered, visible text directly from the browser DOM
                rendered_text = page.evaluate("document.body.innerText")
                browser.close()
                
                # Truncate to protect the Llama context window
                max_chars = 8000
                if len(rendered_text) > max_chars:
                    rendered_text = rendered_text[:max_chars] + "... [TEXT TRUNCATED DUE TO LENGTH]"
                    
                print(">> [PUPPETEER] Dynamic extraction complete.")
                return {"status": "success", "url": url, "content": rendered_text}
                
        except Exception as e:
            return {"error": f"Puppeteer extraction failed: {e}"}
        
    @staticmethod
    def capture_webcam():
        """Captures a single frame from the primary webcam to observe the physical world."""
        try:
            import cv2
            import os
            
            print(">> [OMNI-SENSOR] Accessing physical optical hardware (Webcam)...")
            
            # 0 is usually the default built-in webcam or USB camera
            cap = cv2.VideoCapture(0) 
            
            if not cap.isOpened():
                return {"error": "Failed to open physical webcam. Is it plugged in or blocked?"}
            
            # Warm up the camera
            for _ in range(5):
                cap.read()
                
            ret, frame = cap.read()
            cap.release() 
            
            if ret:
                os.makedirs("workspace", exist_ok=True)
                filepath = "workspace/webcam_vision.jpg"
                cv2.imwrite(filepath, frame)
                print(f">> [OMNI-SENSOR] Physical world captured: {filepath}")
                
                # We spoon-feed the exact instructions and the @ tag to the smaller 8B model
                return {
                    "status": "success", 
                    "message": f"Webcam captured. DO NOT use analyze_screen. Your right brain will automatically see this image: @{filepath}. Use task_complete to tell the user what they are holding."
                }
            else:
                return {"error": "Camera opened but failed to capture a frame."}
                
        except Exception as e:
            return {"error": f"Webcam optical failure: {e}"}