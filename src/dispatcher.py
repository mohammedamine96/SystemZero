from src.tools import Toolbox

class Dispatcher:
    @staticmethod
    def execute(command):
        try:
            if not isinstance(command, dict):
                return {"error": "Dispatcher received invalid data type."}

            action = command.get("action")
            params = command.get("params", {})

            # --- SYSTEM & FILES ---
            if action == "get_system_info":
                return Toolbox.get_system_info()
            
            elif action == "list_directory":
                return Toolbox.list_directory(params.get("path", "."))
            
            elif action == "read_file":
                if not params.get("path"): return {"error": "Missing path."}
                return Toolbox.read_file(params.get("path"))
            
            elif action == "write_file":
                return Toolbox.write_file(params.get("filename"), params.get("content"))
            
            elif action == "run_python_script":
                return Toolbox.run_python_script(params.get("filename"))
            
            # --- WEB (THE RESEARCHER) ---
            elif action == "open_browser":
                return Toolbox.open_browser(params.get("url"))
            
            elif action == "search_web":
                return Toolbox.search_web(params.get("query"))

            elif action == "fetch_website_text":
                url = params.get("url")
                if not url: return {"error": "Missing 'url' parameter."}
                return Toolbox.fetch_website_text(url)
            
            # --- MEMORY (HIPPOCAMPUS) ---
            elif action == "archive_memory":
                fact = params.get("fact")
                if not fact: return {"error": "Missing 'fact' parameter."}
                return Toolbox.archive_memory(fact)
                
            elif action == "recall_memory":
                query = params.get("query")
                if not query: return {"error": "Missing 'query' parameter."}
                return Toolbox.recall_memory(query)

            # --- KEYBOARD & MOUSE (BLIND) ---
            elif action == "mouse_move":
                return Toolbox.mouse_move(params.get("x"), params.get("y"))

            elif action == "mouse_click":
                return Toolbox.mouse_click(params.get("button", "left"))

            elif action == "type_text":
                return Toolbox.type_text(params.get("text"))

            elif action == "press_key":
                return Toolbox.press_key(params.get("key"))
            
            # --- VISION (EYES) ---
            elif action == "click_text":
                text = params.get("text")
                if not text: return {"error": "Missing 'text' parameter."}
                return Toolbox.click_text(text, params.get("button", "left"))

            # --- HANDS (GHOST MODE) ---
            elif action == "inspect_window":
                # No params needed, just scans active window
                return Toolbox.inspect_window()
            
            elif action == "click_button_name":
                name = params.get("name")
                if not name: return {"error": "Missing 'name' parameter."}
                return Toolbox.click_button_name(name)
            
            # --- ORACLE (APIs) ---
            elif action == "get_weather":
                location = params.get("location")
                if not location: return {"error": "Missing 'location' parameter."}
                return Toolbox.get_weather(location)
            
            # --- MAESTRO (SYSTEM CONTROL) ---
            elif action == "control_media":
                cmd = params.get("command")
                if not cmd: return {"error": "Missing 'command' parameter."}
                return Toolbox.control_media(cmd)
            
            elif action == "set_reminder":
                mins = params.get("minutes")
                msg = params.get("message")
                if not mins or not msg: return {"error": "Missing 'minutes' or 'message'."}
                return Toolbox.set_reminder(mins, msg)
            
            # --- COMMUNICATOR (MESSAGING) ---
            elif action == "send_whatsapp":
                phone = params.get("phone_number")
                msg = params.get("message")
                if not phone or not msg: return {"error": "Missing 'phone_number' or 'message'."}
                return Toolbox.send_whatsapp(phone, msg)
            
            # --- VISION (EYES) ---
            elif action == "analyze_screen":
                question = params.get("question", "What is on the screen?")
                return Toolbox.analyze_screen(question)

            elif action == "click_text":
                text = params.get("text")
                if not text: return {"error": "Missing 'text' parameter."}
                return Toolbox.click_text(text, params.get("button", "left"))
            
            # --- SENTINEL (PC HEALTH & DIAGNOSTICS) ---
            elif action == "check_system_health":
                return Toolbox.check_system_health()
                
            elif action == "kill_process":
                name = params.get("process_name")
                if not name: return {"error": "Missing 'process_name' parameter."}
                return Toolbox.kill_process(name)
            
            # --- SCHOLAR (DOCUMENT PARSING) ---
            elif action == "read_pdf":
                filename = params.get("filename")
                if not filename: return {"error": "Missing 'filename' parameter."}
                return Toolbox.read_pdf(filename)
            
            # --- FINISH ---
            elif action == "task_complete":
                summary = params.get("summary", "Task Completed.")
                print(f"\n>> [MISSION ACCOMPLISHED]: {summary}")
                return {"status": "task_complete", "message": summary}

            elif action == "error":
                return {"status": "Aborted by Brain", "reason": command.get("thought")}

            else:
                return {"error": f"Unknown Action: {action}. Execution Blocked."}

        except Exception as e:
            return {"error": f"Dispatch Failure: {e}"}