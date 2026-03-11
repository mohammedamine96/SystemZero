# 🌌 System Zero (v6.0)
**The Sovereign, Swarm-Capable Desktop Entity**

System Zero is an advanced, locally-hosted AI assistant that lives inside your Windows operating system. Evolving far beyond a standard chatbot, System Zero is a proactive, self-modifying, self-correcting multimodal entity. It can control your PC, see the physical world, spawn parallel sub-agents, surf the deep web, and be commanded remotely from your mobile device.

---

## 🧠 The Bicameral Brain (Multi-Cloud Architecture)

System Zero operates on a split-brain architecture to bypass API rate limits and maximize processing speed:
* **The Left Hemisphere (Logic & Speed):** Powered by Groq (`llama-3.3-70b-versatile`), this handles rapid text reasoning, code generation, and UI logic.
* **The Right Hemisphere (The Optical Nerve):** Powered by Google's `gemini-2.5-flash`, this handles massive visual payloads, allowing System Zero to process desktop screenshots and physical webcam images flawlessly.

---

## 👑 The Advanced Paradigms (v6.0 Upgrades)

* **🛡️ Semantic Security Shield:** Replaced legacy regex keyword filters with a local `all-MiniLM-L6-v2` vector similarity filter. Zero now mathematically calculates the true destructive intent of its own thoughts before executing them, halting catastrophic actions at the gate.
* **⚡ Async Watcher Engine:** Replaced toxic synchronous threading with a highly optimized, cooperative `asyncio` event loop. Zero can now monitor dozens of background tasks simultaneously without suffocating low-RAM environments.
* **🧠 Active Synaptic Pruning:** Cured the "Synaptic Decay" vector overload by granting the Hippocampus the mechanical ability to actively search for and permanently delete obsolete or useless long-term memories.
* **🧬 The Architect (AST-Linted Self-Modification):** System Zero can autonomously write new Python tools and permanently learn new skills. In v6.0, an Abstract Syntax Tree (AST) safety linter guarantees injected code will never brick the interpreter.
* **🐝 The Hive Mind (Swarm Intelligence):** Can spawn independent, parallel Llama-3 sub-agents (`delegate_task`) to handle long-running background tasks (like deep research) without freezing the Master Brain.
* **👁️ The Omni-Sensor (Physical Vision):** Using OpenCV and the Gemini Vision Engine, System Zero can access your physical webcam to look into the real world. Ask *"What am I holding?"* and it will capture and analyze the physical environment.

---

## 🛠️ Core Anatomy & Modules

* **👂 The Auditory Cortex:** Uses Picovoice Porcupine for low-power wake-word detection ("Start") and a local `Faster-Whisper` neural engine for high-fidelity continuous listening. It features a "Mute Switch" to safely yield the microphone while speaking.
* **🗣️ The Neural Mouth:** Generates ultra-realistic, human-like voice responses using `edge-tts` and Microsoft Azure's premium voice models.
* **💾 The Hippocampus (Semantic Memory):** Uses `ChromaDB` and local `sentence-transformers` for true Retrieval-Augmented Generation (RAG). 
* **🛰️ The Remote Tether:** Securely linked to a Telegram Bot, allowing the Operator to text System Zero from anywhere on Earth to execute local PC commands.
* **🕸️ The Puppeteer:** Uses a headless Playwright Chromium engine to bypass basic HTML scrapers, render JavaScript, and click UI elements on dynamic web applications.
* **👻 Cybernetics (Ghost Hands & True Vision):** Uses `easyocr` and `llama-4-scout` to conceptually understand the screen, and `pywinauto` to inject ghost-clicks directly into the Windows UI tree. Now featuring Spatially-Filtered Optical Verification for 100% accurate mechanical executions.
* **🖥️ Cyber-Dashboard:** A stunning, CustomTkinter dark-mode GUI with a live, thread-safe matrix console.

---

## 🚀 Installation & Ignition

### 1. Clone & Environment
```bash
git clone https://github.com/mohammedamine96/SystemZero.git
cd SystemZero
python -m venv venv
venv\Scripts\activate
```

### 2. Install Neural Dependencies
```bash
pip install -r requirements.txt

# Install the headless Chromium browser for the Puppeteer module
playwright install
```

### 3. API Keys & Credentials
Create a `.env` file in the root directory (ensure Windows does not name it `.env.txt`) and add your required credentials:

```env
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_google_gemini_key_here
PICOVOICE_API_KEY=your_picovoice_porcupine_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_numeric_chat_id
```

### 4. Boot Sequence
```bash
python main.py
```
*(Note: On the first boot, it will download the sentence-transformers model for the Hippocampus. Say "Start" to awaken the Auditory Cortex).*

---

## 📖 Version Evolution (The 30-Day Journey)

* **v6.0 - Sovereign Stabilization:** Engineered the Async Watcher Engine, deployed the Semantic Security Shield, eradicated hardcoded UI race conditions with Spatial Optical Verification, and cured Synaptic Decay with active forgetting tools.
* **v5.0 - The Omni-Sensor & Bicameral Brain:** Integrated Gemini 2.5 Flash for physical webcam vision. Upgraded Auditory Cortex to Porcupine + Faster-Whisper.
* **v4.0 - The Singularity:** Added Architect (Self-Modification), Hive Mind (Swarm), and Watcher (Proactive Background Automation).
* **v3.2 - The Hippocampus:** Upgraded memory to local ChromaDB Semantic Vector Memory.
* **v3.0 - The Eyes & Voice:** Integrated Llama-4-Scout for True Vision, EasyOCR, and Edge-TTS for continuous audio interactions.
* **v2.0 - The Hands:** Added Ghost Mode (UI Automation), WhatsApp integration, and native Windows OS controls.
* **v1.0 - The Matrix:** Core execution loop, The Coder (Python scripting), and basic logic routing established.
