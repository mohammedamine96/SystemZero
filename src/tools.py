import os
import platform
import sys          
import subprocess
import requests
from bs4 import BeautifulSoup

class Toolbox:
    # hada kijbad l info dyal pc
    @staticmethod
    def get_system_info():
        """Returns basic OS details."""
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

    # hada kichof lik path dyalk
    @staticmethod
    def list_directory(path="."):
        """
        Lists files in the specified directory.
        SECURITY: This is a read-only operation.
        """
        try:
            # Basic validation to prevent traversing too far up if needed
            # For now, we trust the user context but catch errors
            if not os.path.exists(path):
                return {"error": "Path does not exist."}
                
            return {
                "path": path,
                "files": os.listdir(path)
            }
        except Exception as e:
            return {"error": f"Access Denied or Invalid Path: {e}"}

    #hada ki9ra les file
    @staticmethod
    def read_file(path):
        """
        Reads a text file.
        SECURITY: 
        1. Enforces 'workspace/' directory lock (Sandbox).
        2. Enforces size limit.
        """
        try:
            # SANITIZATION: Force workspace path if not absolute
            if not path.startswith("workspace"):
                target_path = os.path.join("workspace", path)
            else:
                target_path = path

            if not os.path.exists(target_path):
                return {"error": f"File not found in workspace: {target_path}"}
            
            # Check size (1MB limit)
            file_size = os.path.getsize(target_path)
            if file_size > 1024 * 1024:
                return {"error": f"File too large ({file_size} bytes). Limit is 1MB."}

            with open(target_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {"content": content[:2000] + "... (truncated)" if len(content) > 2000 else content}

        except Exception as e:
            return {"error": f"Read Failure: {e}"}
    
    # hadi lyadin dyalo li kikatbo flpc
    @staticmethod
    def write_file(filename, content):
        """
        Writes content to a file. 
        SECURITY: 
        1. Enforces 'workspace/' directory lock.
        2. Prevents directory traversal (../).
        """
        try:
            # 1. Sanitize Path (Sandbox Enforcement)
            # We force the file to be inside the 'workspace' directory.
            if ".." in filename or "/" in filename or "\\" in filename:
                return {"error": "Security Violation: You can only write to the root of the 'workspace' directory. Do not use paths."}
            
            target_path = os.path.join("workspace", filename)
            
            # 2. Write
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return {"status": "success", "path": target_path, "bytes_written": len(content)}

        except Exception as e:
            return {"error": f"Write Failure: {e}"}

    # hada ki khaam les file python
    @staticmethod
    def run_python_script(filename):
        """
        Executes a Python script from the workspace.
        SECURITY: 
        1. Only runs files inside 'workspace/'.
        2. Captures stdout/stderr to return to the Brain.
        3. Sets a timeout (5 seconds) to prevent infinite loops.
        """
        import subprocess
        try:
            # 1. Sanitize Path
            if ".." in filename or "/" in filename or "\\" in filename:
                return {"error": "Security Violation: script must be in workspace root."}
            
            target_path = os.path.join("workspace", filename)
            
            if not os.path.exists(target_path):
                return {"error": "Script not found in workspace."}

            # 2. Execute with Timeout
            # We use subprocess.run to spawn a new Python process
            result = subprocess.run(
                [sys.executable, target_path],
                capture_output=True,
                text=True,
                timeout=5 # Safety timeout
            )
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "exit_code": result.returncode
            }

        except subprocess.TimeoutExpired:
            return {"error": "Script execution timed out (limit: 5s)."}
        except Exception as e:
            return {"error": f"Execution Failure: {e}"}
        
    @staticmethod
    def fetch_url(url):
        """
        Fetches text content from a URL.
        SECURITY: Read-only (GET request).
        """
        try:
            # 1. Validation
            if not url.startswith("http"):
                return {"error": "Invalid URL. Must start with http:// or https://"}

            # 2. Request (with timeout to prevent hanging)
            headers = {'User-Agent': 'SystemZero/1.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return {"error": f"HTTP Error: {response.status_code}"}

            # 3. Parse & Clean
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Limit length to prevent context overflow (approx 4000 chars)
            return {
                "url": url,
                "status": "success",
                "content": clean_text[:4000] + "... (truncated)" if len(clean_text) > 4000 else clean_text
            }

        except Exception as e:
            return {"error": f"Fetch Failure: {e}"}
    
    @staticmethod
    def archive_memory(key, value):
        """
        Stores a persistent key-value pair in memory.json.
        Useful for remembering user preferences or project status.
        """
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
    def search_web(query):
        try:
            url = "https://html.duckduckgo.com/html/"
            # IMPROVED HEADER: Looks more like a real chrome browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://html.duckduckgo.com/'
            }
            payload = {'q': query}

            response = requests.post(url, data=payload, headers=headers, timeout=10)
            
            # Debugging: Print status if it fails
            if response.status_code != 200:
                # If 202 happens, it's often a temporary block. 
                # We return a specific error so the brain knows to wait or try fetch_url.
                return {"error": f"Search Blocked (Status {response.status_code}). Try fetch_url directly if known."}

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
            
# Self-Diagnostic
if __name__ == "__main__":
    print("Testing Toolbox...")
    print(f"System Info: {Toolbox.get_system_info()}")
    print(f"List Dir: {Toolbox.list_directory('.')}")
    
    # Create a dummy file to test reading
    with open("test_safe.txt", "w") as f:
        f.write("System Zero Security Test Content.")
    
    print(f"Read File: {Toolbox.read_file('test_safe.txt')}")
    
    # Cleanup
    os.remove("test_safe.txt")