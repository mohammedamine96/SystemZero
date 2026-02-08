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
            
            elif action == "error":
                return {"status": "Aborted by Brain", "reason": command.get("thought")}

            else:
                return {"error": f"Unknown Action: {action}. Execution Blocked."}

        except Exception as e:
            return {"error": f"Dispatch Failure: {e}"}