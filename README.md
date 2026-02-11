# 🤖 System Zero (v1.4)
The Autonomous Multimodal Action Agent

System Zero is a local-first, context-aware AI agent framework powered by Gemini 3 Flash. It bridges the gap between high-level natural language intent and low-level OS execution, featuring a secure "Human-in-the-Loop" architecture.

## 🌟 Key Capabilities

### 👁️ Multimodal Vision
Analyze any image in your workspace. Use the `@filename` syntax to "show" the agent screenshots, diagrams, or logs.
Example: "Fix the error shown in `@bug_report.png`"

### 🔗 Autonomous Chaining (Recursive Logic)
System Zero breaks down complex goals into multiple steps. It executes a tool, sees the result, and automatically decides the next move until the mission is complete.

### ⚡ Trust Mode (Auto-Pilot)
Authorize entire mission chains by typing `y!`. This allows the agent to work autonomously without stopping for approval at every step.

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10+
* Google Gemini API Key

### 2. Installation
Initialize your environment and install dependencies:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install google-genai pillow requests beautifulsoup4 python-dotenv
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
* **Path Locking**: The agent is physically blocked from writing files outside of the `workspace/` folder to protect system integrity.
* **Error-Loop Protection**: A "3-strike" safety break prevents the agent from stuck-infinite-loops or hitting API rate limits.
* **Approval Gate**: By default, no code is executed without a manual `y` confirmation.

## 📂 Project Structure
* `main.py`: The recursive execution loop and human-gate interface.
* `src/brain.py`: Stateful chat session and multimodal processing.
* `src/tools.py`: The "hands" of the system (FS, Web, Python execution).
* `workspace/`: The secure sandbox for all agent activities.

## 📜 Version History
* **v1.0**: Base Execution Loop & Tooling.
* **v1.1**: Vision Module (`@tag` support).
* **v1.2**: Web Access & Scraper.
* **v1.3**: Persistent Memory (`memory.json`).
* **v1.4**: Recursive Autonomy & Trust Mode.
