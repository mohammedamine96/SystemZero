# 🌌 System Zero (v4.0)
**The Autonomous, Self-Modifying Desktop Agent**

System Zero is an advanced, locally-hosted AI assistant that lives inside your Windows operating system. Powered by Groq's blazing-fast inference and Llama 3/4 models, System Zero is no longer just reactive—it is proactive and evolutionary. It can see your screen, control your mouse and keyboard, scrape the web, run background monitoring tasks, and most importantly: **it can write and permanently inject its own code to learn new skills.**

---

## 🧠 Core Capabilities (The Modules)

* **🧬 The Architect (Self-Modification):** System Zero can write new Python tools, inject them into its own `tools.py` DNA, update its `prompts.py` memory, and use the new skills immediately.
* **👁️ The Watcher (Proactive Automation):** Spawns independent background threads to monitor APIs, websites, or local files, alerting the user via voice when specific conditions are met.
* **🧠 The Hippocampus (Semantic Vector Memory):** Uses `ChromaDB` and local `sentence-transformers` to mathematically embed facts, allowing for true contextual recall (RAG) rather than basic keyword matching.
* **🎙️ Audio Cortex (Ears & Mouth):** Always-on wake-word detection with native Windows TTS responses.
* **👁️ True Vision (Llama-4-Scout):** Can capture the screen and conceptually understand images, charts, and UI layouts.
* **👻 Ghost Hands:** Inspects the raw Windows UI tree to interact with buttons directly, bypassing coordinate clicking.
* **💻 The Coder:** Can autonomously write, save, and execute Python scripts to solve complex math or data problems.
* **📚 The Scholar:** Reads and extracts intelligence directly from binary `.pdf` documents using `PyPDF2`.
* **🛡️ The Sentinel:** Monitors PC hardware (CPU/RAM) and acts as a digital scalpel to terminate rogue background processes.
* **⏱️ Chronos:** Manages background threads to track time and trigger native PowerShell alarms.
* **🌍 The Researcher:** Silently scrapes web pages, bypasses HTML clutter, and extracts clean text.
* **📱 The Communicator:** Automates WhatsApp Web to send messages to contacts.
* **🎵 The Maestro:** Deep OS hooks for controlling native media playback and volume.

---

## 🚀 Installation & Setup

1. **Clone & Environment:**
   ```bash
   git clone <your-repo-url>
   cd SystemZero
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure PyAudio, PyAutoGUI, UIAutomation, PyPDF2, psutil, chromadb, sentence-transformers, pyperclip, and groq are installed).*

3. **API Keys:**
   Create a `.env` file in the root directory and add your Groq API Key:
   ```env
   GROQ_API_KEY=your_key_here
   ```

4. **Ignition:**
   ```bash
   python main.py
   ```

## 📖 Version History
* **v4.0 - The Singularity:** Added Architect (Self-Modification) and Watcher (Proactive Background Automation).
* **v3.2:** Upgraded Hippocampus to ChromaDB Semantic Vector Memory.
* **v3.1:** Added Sentinel (Hardware Diagnostics) and Scholar (PyPDF2 Parsing).
* **v3.0:** Integrated Llama-4-Scout for True Vision screen analysis.
* **v2.5:** Integrated Chronos background threading for alarms.
* **v2.0:** Added Audio Cortex (Continuous listening & TTS).
* **v1.0:** Core engine, Coder, Researcher, and basic Actuators initialized.
