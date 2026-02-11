# SystemZero

## Designation
**Autonomous Multimodal Agent** (v1.2)

## Overview
System Zero is a local, context-aware AI agent capable of interacting with the OS, the visual world, and the internet. It operates under a strict human-in-the-loop security protocol.

## Capabilities
1.  **Core:** Read/Write files, List directories, System Info.
2.  **Execution:** Write and run Python scripts in a sandbox.
3.  **Vision:** Analyze images via \@filename\ syntax.
4.  **Network:** Fetch and scrape text from websites.
5.  **Memory:** Retains context across multiple turns.

## Architecture
* **Brain:** Gemini Flash (Multimodal).
* **Tools:**
    * \etch_url\ (Web Scraper)
    * \
un_python_script\ (Code Executor)
    * \write_file\ (File System)
* **Security:**
    * \workspace/\ Sandbox enforcement.
    * JSON-strict parsing.
    * User confirmation gate.

## Usage
1.  \pip install -r requirements.txt\
2.  \python main.py\
3.  **Commands:**
    * "\Check the news on bbc.com\"
    * "\Look at @chart.png and summarize it\"
    * "\Write a script to calculate Pi\"

