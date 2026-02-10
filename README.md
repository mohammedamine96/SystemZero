# SystemZero

## Designation
**Multimodal Local Action Agent** (v1.1)

## Overview
System Zero is a context-aware, multimodal agent that interfaces with the local OS. It can read/write files, execute code, and **analyze images**.

## Architecture
* **Brain:** \src/brain.py\ - Gemini Flash with Vision support.
* **Tools:** \src/tools.py\ - File System & Code Execution Sandbox.
* **Interface:** \main.py\ - Supports \@filename\ syntax for image injection.

## Capabilities
1.  **Code Execution:** Write and run Python scripts.
2.  **Vision:** Analyze images in the workspace using \@filename.png\.
3.  **Memory:** Remembers previous actions and context.

## Usage
1.  \pip install -r requirements.txt\
2.  Setup \.env\ with \GEMINI_API_KEY\.
3.  **Vision Example:**
    * Drop \error_log.png\ into \workspace/\.
    * Run: "\Analyze the error in @error_log.png and write a fix to fix.py\"

