# HappyMonkeyAI/motion-aware-voice-chat-bot

- URL: https://github.com/HappyMonkeyAI/motion-aware-voice-chat-bot
- License: MIT according to the repository LICENSE.md in the cloned reference.
- Stack/runtime: Python 3.12, FastAPI, browser webcam capture, pixel-difference motion detection, WebSocket chat, OpenAI-compatible vision model, browser STT/TTS, optional MCP tool integration.
- Why it matters: Useful for later presence-aware pet behaviours and simple state-machine structure.
- What to cherry-pick:
  - Browser-side motion detection if GLITCH becomes an ambient desktop/webcam pet.
  - `BotStateMachine` style timing transitions for greeting, nudge, and inactivity.
  - Optional MCP/tool pattern only if it directly improves pet play.
- What to avoid:
  - Requiring camera permission in the first MVP.
  - Generic friendly assistant persona.
  - Vision Q&A as the central product loop.
- Repo relationship: Secondary reference for v2 motion/presence features.
