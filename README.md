# 🤖 System Zero (v2.0)
**The Autonomous Desktop Operator**

System Zero is a local-first, context-aware AI agent that controls your computer. It bridges the gap between natural language intent and low-level OS execution.

**Powered by:** Llama 3.3 (70B) via Groq Cloud.
**Speed:** Near-Instant (~300 tokens/sec).
**Cost:** Free.

---

## 🌟 Key Capabilities

### 🧠 Super-Intelligence (Groq Llama 3.3)
The brain has been upgraded to **Llama 3.3 (70B)**. It understands complex logic, follows strict JSON schemas, and has no daily rate limits for standard use.

### 🖥️ Desktop App Control
System Zero can open and control Windows applications (WhatsApp, Calculator, Notepad) by simulating human keyboard/mouse inputs.
* **Protocol:** It presses the `Win` key, searches for the app, and launches it.

### 🎙️ Voice Command (Ears Module)
Talk to your agent naturally.
* **Activation:** Type `voice` in the console.
* **Deactivation:** Say "Switch to text".
* **Engine:** Google Speech Recognition.

### ⌨️ Verbatim Typing
The agent includes a "Verbatim Mode" to type exactly what you dictate, bypassing polite AI filters.

### 🖱️ Cybernetic Interaction
* **Mouse:** Move to coordinates, Click (Left/Right/Double).
* **Keyboard:** Type text, Press specific keys (Enter, Esc, Win, Tab).

### 🌐 Autonomous Web Search
The agent can actively research the web using a local, API-free scraper (DuckDuckGo HTML).

---

## 🚀 Getting Started

### 1. Prerequisites
* **OS:** Windows 10/11
* **Python:** 3.10 or higher (3.12 Recommended)
* **Groq API Key:** [Get it for free here](https://console.groq.com/keys)

### 2. Installation
Initialize your environment and install dependencies:

```powershell
# 1. Create Environment
python -m venv venv
.\venv\Scripts\activate

# 2. Install Dependencies
pip install -r requirements.txt
```

**Required Packages (requirements.txt):**
```plaintext
groq
python-dotenv
pyautogui
SpeechRecognition
pyaudio
requests
beautifulsoup4
pillow
```

### 3. Configuration
Create a `.env` file in the root directory and add your API Key:

```env
GROQ_API_KEY=gsk_your_key_here
```

### 4. Running the Agent
```powershell
python main.py
```

## 🎮 How to Use

### 🗣️ Voice Mode
1. Run the agent.
2. Wait for `[EARS] Calibrating...`.
3. Type `voice` and hit Enter.
4. Speak your command (e.g., "Open Notepad and type Hello").

### 🖱️ Desktop Control
To open apps, be specific about using the Start Menu:
* **User:** "Open WhatsApp using the start menu."
* **System:** Presses `Win` -> Types `WhatsApp` -> Presses `Enter`.

### 🛡️ Safety & Control
* **Stop Execution:** Press `Ctrl+C` in the terminal.
* **Emergency Stop:** Slam your mouse cursor to any corner of the screen (PyAutoGUI Fail-Safe).
* **Approval Gate:** By default, the agent asks for confirmation (`y`). Type `y!` to enable Trust Mode (Autonomous execution).

## 📂 System Architecture

| Module | Function |
| :--- | :--- |
| `main.py` | **The Central Nervous System.** Handles the input loop (Voice/Text) and error recovery. |
| `src/brain.py` | **Groq Integration.** Connects to Llama 3.3 to process intent into JSON. |
| `src/ears.py` | **Auditory Cortex.** Handles microphone input and Speech-to-Text. |
| `src/dispatcher.py` | **The Body.** Routes JSON commands to the correct tools. |
| `src/tools.py` | **The Hands.** Contains `mouse_move`, `type_text`, `open_browser`, etc. |
| `src/prompts.py` | **The Rules.** Defines the system personality and JSON schema. |

## 📜 Version History
* **v1.0:** Gemini API Base.
* **v1.5:** Vision & Local Tools.
* **v1.6:** Operator Mode (Mouse/Keyboard).
* **v1.7:** Auditory Interface (Voice).
* **v2.0:** Groq Migration. Replaced Gemini with Llama 3.3 for speed/autonomy. Added Desktop App Protocols.
