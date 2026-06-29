# HappyMonkeyAI/voice-assistant

- URL: https://github.com/HappyMonkeyAI/voice-assistant
- License: MIT according to the repository README/LICENSE in the cloned reference.
- Stack/runtime: FastAPI, WebSockets, Deepgram streaming STT, Cartesia streaming TTS, OpenAI-compatible LLM client, SQLite WAL, static HTML/CSS/JS frontend, Docker Compose.
- Why it matters: This is the strongest baseline for GLITCH's premium voice loop and persistent session architecture.
- What to cherry-pick:
  - `/ws` bidirectional audio/session pattern.
  - Deepgram transcript queue and Cartesia streaming audio path.
  - SQLite WAL setup for non-blocking persistence.
  - Existing frontend audio handling and status event concepts.
- What to avoid:
  - Business intake concepts: `LeadProfile`, staged Gmail/calendar actions, corporate dashboard language.
  - Overly polished glassmorphic assistant aesthetic if it dilutes the low-fi pet identity.
- Repo relationship: Primary implementation reference, but GLITCH should replace the lead-intake schema with pet vitals and a mood engine.
