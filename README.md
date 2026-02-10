# SystemZero

## Designation
**Context-Aware Local Action Agent** (v1.0)

## Overview
System Zero is a secure, human-in-the-loop framework that allows an LLM (Gemini Flash) to interface with the local operating system. Unlike standard chatbots, System Zero allows for **persistent context**, **file manipulation**, and **code execution** within a sandboxed environment.

## Architecture
* **Brain:** \src/brain.py\ - Manages the Gemini Chat Session (Stateful Memory).
* **Parser:** \src/parser.py\ - Enforces strict JSON output from the LLM.
* **Dispatcher:** \src/dispatcher.py\ - Routes commands to specific tools.
* **Tools:** \src/tools.py\ - The execution layer (Sandbox: \./workspace\).

## Capabilities
1.  **Contextual Logic:** Knows what you did 5 minutes ago.
2.  **File Operations:** Can read, write, and list files.
3.  **Code Execution:** Can write Python scripts and run them immediately.
4.  **Security:**
    * **Human Gate:** User must approve every action.
    * **Sandbox:** Write/Run operations restricted to \./workspace\.

## Usage
1.  \pip install -r requirements.txt\
2.  Setup \.env\ with \GEMINI_API_KEY\.
3.  \python main.py\
4.  **Example Workflow:**
    * User: "\Write a script to calculate the Fibonacci sequence.\"
    * System: [Writes file]
    * User: "\Run it.\"
    * System: [Executes file]

