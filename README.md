# 🌌 System Zero (v3.1)
**The Autonomous, Multimodal Desktop Agent**

System Zero is an advanced, locally-hosted AI assistant that lives inside your Windows operating system. Powered by Groq's blazing-fast inference and Llama 3/4 models, System Zero doesn't just chat—it *acts*. It can see your screen, control your mouse and keyboard, read local files, scrape the web, and manage your PC hardware, all driven by voice commands.

---

## 🧠 Core Capabilities (The Modules)

* **🎙️ Audio Cortex (Ears & Mouth):** Always-on wake-word detection ("Zero") with native Windows TTS responses.
* **👁️ True Vision (Llama-4-Scout):** Can capture the screen and conceptually understand images, charts, and UI layouts.
* **👻 Ghost Hands:** Inspects the raw Windows UI tree to interact with buttons directly, bypassing coordinate clicking.
* **💻 The Coder:** Can autonomously write, save, and execute Python scripts to solve complex math or data problems.
* **📚 The Scholar:** Reads and extracts intelligence directly from binary `.pdf` documents using `PyPDF2`.
* **🛡️ The Sentinel:** Monitors PC hardware (CPU/RAM) and acts as a digital scalpel to terminate rogue background processes.
* **⏱️ Chronos:** Manages background threads to track time and trigger native PowerShell alarms without interrupting the main loop.
* **🌍 The Researcher:** Silently scrapes web pages, bypasses HTML clutter, and extracts clean text for summarization.
* **📱 The Communicator:** Automates WhatsApp Web to send messages to contacts.
* **💾 The Hippocampus:** A persistent long-term memory drive (`memory.json`) for recalling user facts and secrets.
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
   *(Note: Ensure PyAudio, PyAutoGUI, UIAutomation, PyPDF2, psutil, and groq are installed).*

3. **API Keys:**
   Create a `.env` file in the root directory and add your Groq API Key:
   ```env
   GROQ_API_KEY=your_key_here
   ```

4. **Ignition:**
   ```bash
   python main.py
   ```

---

## 📖 Version History

* **v1.0:** Core Brain & Dispatcher Engine
* **v1.1:** The Coder (Python execution)
* **v1.2:** The Researcher (Web scraping & search)
* **v1.3:** The Hippocampus (JSON Memory)
* **v1.4:** Blind Actuators (PyAutoGUI keyboard/mouse)
* **v1.5:** Ghost Hands (UI Automation inspection)
* **v1.6:** The Oracle (Weather API)
* **v2.0:** The Audio Cortex (Voice Wake-Word & TTS) (Major Update)
* **v2.1:** The Maestro (OS Media control)
* **v2.2:** The Communicator (WhatsApp automation)
* **v2.3:** Basic Eyes (OCR coordinate clicking)
* **v2.4:** The Dashboard (Tkinter GUI thread integration)
* **v2.5:** The Chronos Module (Background alarms)
* **v3.0:** True Vision (Llama-4-Scout Screen Analysis) (Major Update)
* **v3.1:** The Sentinel & The Scholar (Hardware Diagnostics & PyPDF2)
