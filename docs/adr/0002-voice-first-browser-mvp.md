# ADR 0002: Voice-First Browser MVP

## Status

Accepted

## Context

Two reference projects are available:

- `voice-assistant` has the stronger low-latency speech pipeline: FastAPI WebSockets, Deepgram STT, Cartesia TTS, OpenAI-compatible LLM, SQLite WAL.
- `motion-aware-voice-chat-bot` has useful browser motion detection and a simple engagement state machine, but relies on browser STT/TTS for the main voice loop.

## Decision

The first GLITCH build will be a browser-first web app using the `voice-assistant` pipeline as the baseline. Motion/camera features remain optional v2 work.

## Consequences

- First MVP can focus on mood, voice, and retention without camera permission friction.
- The single-page UI can reuse the same deployment style as `voice-assistant`.
- Browser Web Speech can be kept as a fallback, not the main premium path.
- Motion-aware prompts can be revisited once the pet loop is already fun.
