# 🤖 System Zero (v1.5)
The Autonomous Multimodal Action Agent

System Zero is a local-first, context-aware AI agent framework powered by Gemini 3 Flash. It bridges the gap between high-level natural language intent and low-level OS execution, featuring a secure "Human-in-the-Loop" architecture.

## 🌟 Key Capabilities

### 👁️ On-Demand Vision ("Look")
Type `look` in the console to instantly capture your screen. The agent will analyze the visual context and suggest actions.
*Also supports `@filename` to analyze specific images.*

### 🌐 Autonomous Web Search
The agent can actively research the web using a local, API-free scraper (DuckDuckGo HTML). It parses search results to find documentation, stock prices, or news without burning extra API tokens.

### 🛑 Self-Termination Protocol
System Zero knows when it's done. Using the `task_complete` signal, it exits execution loops gracefully, preventing "hallucination drift" where agents keep working past the goal.

### 🔗 Autonomous Chaining (Recursive Logic)
System Zero breaks down complex goals into multiple steps. It executes a tool, sees the result, and automatically decides the next move until the mission is complete.

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
**Path Locking:** The agent is physically blocked from writing files outside of the `workspace/` folder.

**Error-Loop Protection:** A "3-strike" safety break prevents the agent from stuck-infinite-loops.

**Approval Gate:** By default, no code is executed without a manual `y` confirmation.

## 📂 Project Structure
* `main.py`: The recursive execution loop, vision interceptor, and human-gate interface.
* `src/brain.py`: Stateful chat session and multimodal processing.
* `src/dispatcher.py`: The neural routing layer (maps JSON -> Tool Functions).
* `src/tools.py`: The "hands" (FS, Scraper, Screen Capture, Python execution).
* `workspace/`: The secure sandbox for all agent activities.

## 📜 Version History
* **v1.0:** Base Execution Loop & Tooling.
* **v1.1:** Vision Module (@tag support).
* **v1.2:** Web Access & Scraper.
* **v1.3:** Persistent Memory (memory.json).
* **v1.4:** Recursive Autonomy & Trust Mode.
* **v1.5:** The Final Polish. Integrated `look` command, `task_complete` protocol, and robust Web Search.
