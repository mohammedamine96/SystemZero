# FIXED IMPORT: pointing to src.tools
from src.tools import Toolbox

class Dispatcher:
    @staticmethod
    def execute(command):
        try:
            if not isinstance(command, dict):
                return {"error": "Dispatcher received invalid data type."}

            action = command.get("action")
            params = command.get("params", {})

            if action == "get_system_info":
                return Toolbox.get_system_info()
            
            elif action == "list_directory":
                target_path = params.get("path", ".")
                return Toolbox.list_directory(target_path)
            
            elif action == "read_file":
                target_path = params.get("path")
                if not target_path:
                    return {"error": "Missing 'path' parameter for read_file."}
                return Toolbox.read_file(target_path)
            
            elif action == "write_file":
                filename = params.get("filename")
                content = params.get("content")
                if not filename or content is None:
                    return {"error": "Missing 'filename' or 'content' for write_file."}
                return Toolbox.write_file(filename, content)
            
            elif action == "run_python_script":
                filename = params.get("filename")
                if not filename:
                    return {"error": "Missing 'filename' for run_python_script."}
                return Toolbox.run_python_script(filename)
            
            elif action == "fetch_url":
                url = params.get("url")
                if not url:
                    return {"error": "Missing 'url' parameter for fetch_url."}
                return Toolbox.fetch_url(url)
            
            elif action == "error":
                return {"status": "Aborted by Brain", "reason": command.get("thought")}

            else:
                return {"error": f"Unknown Action: {action}. Execution Blocked."}

        except Exception as e:
            return {"error": f"Dispatch Failure: {e}"}