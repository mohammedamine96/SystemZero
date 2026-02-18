# ⚡ System Zero (v3.1)

**The Fully Autonomous, Voice-Activated Desktop Agent.**

System Zero is a local-first AI agent that operates your Windows PC. It uses **Llama 3.3** for reasoning, **Computer Vision** to see the screen, and **Direct UI Injection** to control applications without hijacking your mouse.

It features a "God Mode" (Trust Session) for continuous, hands-free voice command execution.

## 🌟 Key Capabilities

### 🧠 The Brain (Groq Llama 3.3)
* **Model:** Llama 3.3 70B (Versatile).
* **Speed:** ~300 tokens/sec.
* **Logic:** Follows strict JSON schemas for deterministic control.

### 👁️ The Eyes (Computer Vision)
* **Engine:** EasyOCR + OpenCV (CUDA Accelerated).
* **Function:** Scans the screen for text/buttons when "Ghost Mode" fails.
* **Latency:** <2s with GPU acceleration.

### ✋ The Hands (Ghost Mode)
* **Technology:** `pywinauto` (Windows UI Automation).
* **Capability:** Clicks buttons directly via API injection (0ms latency, invisible to the user).
* **Fallback:** Uses standard `pyautogui` mouse movement if API injection fails.

### 👂 The Ears (Continuous Listening)
* **Wake Word:** "Start" (Passive Listening Loop).
* **Protocol:** Once activated, it enters a continuous conversation loop.
* **Commands:** "Sleep", "Stop Listening", "Switch to Text".

### 🗣️ The Mouth (Neural Speech)
* **Engine:** Edge-TTS (Microsoft Azure Neural Voices).
* **Behavior:** Blocking/Synchronous speech (Agent waits for speech to finish before acting).

---

## 🚀 Installation

### 1. Clone & Environment
```bash
git clone https://github.com/mohammedamine96/SystemZero.git
cd SystemZero
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
> **Note:** For GPU acceleration (recommended), install PyTorch with CUDA support manually.

### 3. Configuration
Create a `.env` file in the root directory:
```ini
GROQ_API_KEY=gsk_your_key_here
```

## 🎮 Usage Guide

### 🗣️ Voice Mode (The "Ironman" Experience)
1. Run the agent: `python main.py`
2. Type `voice` to enter Voice Mode.
3. Say "Start" to wake the agent.
4. **Issue Commands:** "Open Notepad", "Search YouTube for lo-fi music", etc.

> **God Mode:** In Voice Mode, the agent does not ask for confirmation. It executes commands instantly.

### 🖥️ Text Mode (Safe Mode)
1. Run the agent: `python main.py`
2. Type commands manually.

> **Safety Gate:** The agent will ask for confirmation (y/n) before executing actions.

## 📂 Architecture

| Module | Function |
| :--- | :--- |
| `main.py` | **Central Nervous System.** Handles the Input/Output loop and State Management. |
| `src/brain.py` | **LLM Interface.** Converts natural language into JSON instructions. |
| `src/ears.py` | Wake Word detection and Speech-to-Text. |
| `src/mouth.py` | Text-to-Speech engine. |
| `src/eyes.py` | OCR and Screen Analysis. |
| `src/hands.py` | Windows UI Automation (Ghost Clicks). |
| `src/tools.py` | The toolkit definition (File I/O, Browser, OS interaction). |

## ⚠️ Disclaimer
**System Zero v3.1 (God Mode)** executes commands immediately.
If you tell it to "Delete System32", it might actually try. **Use Voice Mode with caution.**
