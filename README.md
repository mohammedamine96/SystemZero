# 🤖 System Zero (v1.6)
The Autonomous Multimodal Action Agent

System Zero is a local-first, context-aware AI agent framework powered by Gemini 3 Flash. It bridges the gap between high-level natural language intent and low-level OS execution, featuring a secure "Human-in-the-Loop" architecture.

## 🌟 Key Capabilities

### 🖱️ Cybernetic Operator (GUI Control) **[NEW]**
The agent now possesses "Hands." It can control the mouse and keyboard to interact with applications that lack APIs.
* **Tools:** `mouse_move`, `mouse_click`, `type_text`, `press_key`.
* **Safety:** Includes `pyautogui` fail-safes (slam mouse to corner to abort).

### 🚀 Direct Browser Injection **[NEW]**
Uses the `open_browser` tool to bypass the address bar and autocomplete traps, launching specific URLs directly via the OS shell.

### 👁️ On-Demand Vision ("Look")
Type `look` in the console to instantly capture your screen. The agent will analyze the visual context and suggest actions.

### 🌐 Autonomous Web Search
The agent can actively research the web using a local, API-free scraper (DuckDuckGo HTML).

### 🛑 Self-Termination Protocol
System Zero knows when it's done. Using the `task_complete` signal, it exits execution loops gracefully.

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10+
* Google Gemini API Key

### 2. Installation
Initialize your environment and install dependencies:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install google-genai pillow requests beautifulsoup4 python-dotenv pyautogui
```

### 3. Setup Credentials
Create a `.env` file in the root directory and add your API key:

```env
GEMINI_API_KEY=YOUR_KEY_HERE
```

### 4. Running the Agent

```powershell
python main.py
```

## 🛡️ Security & Safety
* **Path Locking:** The agent is physically blocked from writing files outside of the `workspace/` folder.
* **Fail-Safe:** If the mouse moves uncontrollably, slam it to any corner of the screen to trigger the pyautogui emergency stop.
* **Approval Gate:** By default, no code is executed without a manual `y` confirmation.

## 📂 Project Structure
* `main.py`: The recursive execution loop, vision interceptor, and human-gate interface.
* `src/brain.py`: Stateful chat session and multimodal processing.
* `src/dispatcher.py`: The neural routing layer (maps JSON -> Tool Functions).
* `src/tools.py`: The "hands" (FS, Scraper, Vision, Mouse/Keyboard, Browser).
* `workspace/`: The secure sandbox for all agent activities.

## 📜 Version History
* **v1.0:** Base Execution Loop & Tooling.
* **v1.1:** Vision Module (@tag support).
* **v1.2:** Web Access & Scraper.
* **v1.3:** Persistent Memory (`memory.json`).
* **v1.4:** Recursive Autonomy & Trust Mode.
* **v1.5:** Integrated look command and Task Termination.
* **v1.6:** Operator Mode. Added GUI Automation (Mouse/Keyboard) and Direct Browser Control.
