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
            
            elif action == "archive_memory":
                key = params.get("key")
                value = params.get("value")
                if not key or value is None:
                    return {"error": "Missing 'key' or 'value' for archive_memory."}
                return Toolbox.archive_memory(key, value)
            
            elif action == "search_web":
                query = params.get("query")
                if not query:
                    return {"error": "Missing 'query' parameter for search_web."}
                return Toolbox.search_web(query)
            
            elif action == "task_complete":
                summary = params.get("summary", "Task Completed.")
                print(f"\n>> [MISSION ACCOMPLISHED]: {summary}")
                return {"status": "complete", "message": summary}

            elif action == "mouse_move":
                x = params.get("x")
                y = params.get("y")
                if x is None or y is None:
                    return {"error": "Missing coordinates for mouse_move."}
                return Toolbox.mouse_move(int(x), int(y))

            elif action == "mouse_click":
                button = params.get("button", "left")
                return Toolbox.mouse_click(button)

            elif action == "type_text":
                text = params.get("text")
                if not text:
                    return {"error": "Missing text for type_text."}
                return Toolbox.type_text(text)

            elif action == "press_key":
                key = params.get("key")
                if not key:
                    return {"error": "Missing key for press_key."}
                return Toolbox.press_key(key)
            
            elif action == "open_browser":
                url = params.get("url")
                if not url:
                    return {"error": "Missing 'url' parameter."}
                return Toolbox.open_browser(url)
            
            elif action == "error":
                return {"status": "Aborted by Brain", "reason": command.get("thought")}

            else:
                return {"error": f"Unknown Action: {action}. Execution Blocked."}

        except Exception as e:
            return {"error": f"Dispatch Failure: {e}"}