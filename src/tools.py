import os
import platform
import sys          
import subprocess

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
        1. Checks if file exists.
        2. Enforces a strict size limit (1MB) to prevent memory crashes.
        """
        try:
            if not os.path.exists(path):
                return {"error": "File not found."}
            
            # Check size (1MB limit)
            file_size = os.path.getsize(path)
            if file_size > 1024 * 1024:
                return {"error": f"File too large ({file_size} bytes). Limit is 1MB."}

            with open(path, 'r', encoding='utf-8') as f:
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