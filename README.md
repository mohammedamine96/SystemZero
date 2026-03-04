# 🌌 System Zero (v5.0)
**The Sovereign, Swarm-Capable Desktop Agent**

System Zero is an advanced, locally-hosted AI assistant that lives inside your Windows operating system. Powered by a multi-model Groq architecture (Llama 3.3 70B & Llama 3.1 8B), System Zero transcends standard chatbots. It is a proactive, self-modifying, self-correcting entity. It can control your PC, spawn parallel sub-agents, surf the deep web, and be commanded remotely from your mobile device.

---

## 👑 The v5.0 Paradigms (Advanced Agentic Architecture)

* **🐝 The Hive Mind (Multi-Agent Swarm):** Can spawn independent, parallel Llama-3.1-8B sub-agents to handle long-running background tasks (like deep research or coding) without freezing the Master Brain.
* **🧠 True Learning (Neural Feedback Loop):** Automatically writes Post-Mortem Analyses when it makes a mistake and archives the solution into its ChromaDB vector memory to permanently rewrite its future behavior.
* **🛰️ The Remote Tether:** Securely linked to a Telegram Bot, allowing the Operator to text System Zero from anywhere on Earth to execute local PC commands and receive alerts.
* **🕸️ The Puppeteer (Deep Web Automation):** Uses a headless Playwright Chromium engine to bypass basic HTML scrapers, rendering JavaScript, clicking selectors, and reading dynamic web applications.

---

## 🛠️ Core Capabilities (The Base Modules)

* **🧬 The Architect (Self-Modification):** System Zero can write new Python tools, inject them into its own `tools.py` DNA, and permanently learn new skills without human coding.
* **👁️ The Watcher (Proactive Automation):** Spawns independent background cron threads to monitor APIs or local files, triggering audible/mobile alerts.
* **💾 The Hippocampus (Semantic Memory):** Uses `ChromaDB` and local `sentence-transformers` for true Retrieval-Augmented Generation (RAG).
* **🖥️ Cyber-Dashboard:** A stunning, CustomTkinter dark-mode GUI with a live, thread-safe matrix console.
* **🗣️ Neural Audio Cortex:** Generates ultra-realistic, human-like voice responses using `edge-tts` and Microsoft Azure's premium voice models.
* **👁️ True Vision (Llama-4-Scout):** Captures the screen to conceptually understand images, code, and UI layouts.
* **👻 Ghost Hands:** Inspects the raw Windows UI tree to interact with desktop application buttons directly.
* **💻 The Coder:** Autonomously writes, saves, and executes Python scripts to solve math or data problems natively.
* **📚 The Scholar:** Reads and extracts intelligence directly from binary `.pdf` documents using `PyPDF2`.

---

## 🚀 Installation & Setup

### 1. Clone & Environment:
```bash
git clone <your-repo-url>
cd SystemZero
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies:
```bash
pip install requests beautifulsoup4 pyautogui uiautomation psutil PyPDF2 chromadb sentence-transformers pyperclip customtkinter edge-tts pygame pyTelegramBotAPI playwright groq

# Install the headless Chromium browser for the Puppeteer module
playwright install
```

### 3. API Keys & Credentials:
Create a `.env` file in the root directory and add your credentials:
```env
GROQ_API_KEY=your_groq_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_numeric_chat_id
```

### 4. Ignition:
```bash
python main.py
```
*(Note: On the first boot, it will download the sentence-transformers model. Open your Telegram bot and send "/start" to initiate the secure mobile handshake).*

---

## 📖 Version History
* **v5.0 - The Advanced Paradigms:** Added Hive Mind (Swarm), Puppeteer (Playwright), Remote Tether (Telegram), and True Learning (Auto-reflection).
* **v4.0 - The Singularity:** Added Architect (Self-Modification) and Watcher (Proactive Background Automation).
* **v3.2:** Upgraded Hippocampus to ChromaDB Semantic Vector Memory.
* **v3.0:** Integrated Llama-4-Scout for True Vision screen analysis.
* **v2.0:** Added Audio Cortex (Continuous listening & TTS).
* **v1.0:** Core engine, Coder, Researcher, and basic Actuators initialized.
