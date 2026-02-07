# SystemZero

## Designation
**Local Action Agent Framework** (Python/Gemini)

## Status
**Phase 3 Complete** (Cognition & Parsing Established).
Currently halted before **Phase 4** (System Prompt & JSON Enforcement).

## Architecture
* **Core:** Python 3.x
* **Brain:** Google Gemini (Flash-Latest via google-genai SDK)
* **Parser:** Strict JSON extraction with Markdown stripping.

## Setup
1. Clone repository.
2. Create .env with GEMINI_API_KEY.
3. pip install -r requirements.txt
4. Run python src/brain.py to test connectivity.

## Roadmap
- [x] Environment Initialization
- [x] API Connection (Brain Module)
- [x] Output Parsing (Parser Module)
- [ ] System Prompt Engineering (Next Session)
- [ ] Local File System Interface
- [ ] Command Execution Loop"