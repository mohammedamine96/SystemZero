# 🤖 System Zero (v1.7)
The Autonomous Multimodal Action Agent

System Zero is a local-first, context-aware AI agent framework powered by Gemini 3 Flash. It bridges the gap between high-level natural language intent and low-level OS execution.

## 🌟 Key Capabilities

### 🎙️ Voice Control (Auditory Input) **[NEW]**
Talk to your agent naturally.
* **Activation:** Type `voice` in the console.
* **Deactivation:** Say "Switch to text".
* **Engine:** Uses Google Speech Recognition for high-accuracy command parsing.

### 🖱️ Cybernetic Operator (GUI Control)
The agent possesses "Hands." It can control the mouse and keyboard to interact with applications that lack APIs.
* **Tools:** `mouse_move`, `mouse_click`, `type_text`, `press_key`.
* **Safety:** Slam mouse to corner to abort.

### 🚀 Direct Browser Injection
Uses the `open_browser` tool to bypass autocomplete traps, launching specific URLs directly via the OS shell.

### 👁️ On-Demand Vision ("Look")
Type `look` (or say "Look at this") to instantly capture your screen. The agent will analyze the visual context.

### 🌐 Autonomous Web Search
The agent can actively research the web using a local, API-free scraper (DuckDuckGo HTML).

### 🛑 Self-Termination Protocol
System Zero knows when it's done. Using the `task_complete` signal, it exits execution loops gracefully.

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10+
* Google Gemini API Key
* Microphone

### 2. Installation
Initialize your environment and install dependencies:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
# Requirements: google-genai pillow requests beautifulsoup4 python-dotenv pyautogui SpeechRecognition pyaudio
```

### 3. Setup Credentials
Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=YOUR_KEY_HERE
```

### 4. Running the Agent

```powershell
python main.py
```

## 🛡️ Security & Safety
* **Path Locking:** The agent is blocked from writing files outside `workspace/`.
* **Fail-Safe:** Mouse movement limits.
* **Approval Gate:** Mandatory `y` confirmation (works in Voice Mode too).

## 📂 Project Structure
* `main.py`: Hybrid Input Loop (Voice/Text) and Orchestrator.
* `src/ears.py`: Audio driver and Speech-to-Text engine.
* `src/brain.py`: LLM Logic.
* `src/dispatcher.py`: Neural Routing.
* `src/tools.py`: The Body (FS, Web, GUI, Vision).
* `workspace/`: Secure Sandbox.

## 📜 Version History
* **v1.0 - v1.4:** Foundations (File I/O, Web Scraper, Memory).
* **v1.5:** Vision & Termination Protocols.
* **v1.6:** Operator Mode (Mouse/Keyboard).
* **v1.7:** Auditory Interface. Added `src/ears.py` and Voice/Text switching.
