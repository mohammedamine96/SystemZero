import os
import platform

class Toolbox:
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