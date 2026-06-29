# Glitch Pet

Glitch is a low-fi AI cyber pet you can talk to in the browser. It is not an anime companion and not a therapy bot. The product direction is a stark, funny, slightly needy digital gremlin with simple ASCII-style expressions, aggressive colour states, and voice-first interaction.

Working thesis: reuse the low-latency voice architecture from HappyMonkeyAI/voice-assistant, borrow optional motion-awareness ideas from HappyMonkeyAI/motion-aware-voice-chat-bot, and replace the business-intake layer with a persistent pet-vitals and mood engine.

## Product shape

- Browser-first MVP: one page, one pet face, microphone controls, mood/vitals panel, transcript log.
- Visual identity: terminal/pixel/cyberpet, simple emoji or ASCII face, full-page colour mood states.
- Voice identity: short, sassy, needy, playful; never waifu/anime-coded and never soft corporate assistant.
- Core loop: talk to GLITCH, feed it attention or interesting updates, watch mood shift, return later to consequences.
- Viral loop: share short dramatic reaction clips or rescue/forgiveness links after neglect.

## Runtime assumptions

Initial implementation should stay close to the reference stack:

- Backend: Python 3.10+ or 3.12, FastAPI, WebSockets.
- STT/TTS: Deepgram + Cartesia streaming from `voice-assistant` for the high-quality voice path; browser Web Speech can be a fallback only.
- LLM: OpenAI-compatible local or hosted model endpoint.
- Persistence: SQLite in WAL mode for pet state, session history, timeline events, and shareable rescue links.
- Frontend: single static HTML/CSS/JS page until product behaviour is proven.

## Canonical docs

- `CONTEXT.md` — operating manual and source-of-truth hierarchy.
- `HERMES.md` — agent workflow and repo guardrails.
- `docs/adr/` — durable architecture and product decisions.
- `docs/plans/` — implementation plans for feature slices.
- `research/` — reference-only notes on external projects and product positioning.

## Reference projects

- `HappyMonkeyAI/voice-assistant`: low-latency streaming voice, FastAPI WebSocket gateway, Deepgram STT, Cartesia TTS, OpenAI-compatible LLM, SQLite WAL.
- `HappyMonkeyAI/motion-aware-voice-chat-bot`: browser webcam motion detection, simple state machine, optional MCP/tool integration, browser STT/TTS fallback.

## Quick start

The current scaffold runs a browser-first text loop: FastAPI serves the low-fi GLITCH page, `/ws` accepts `user_text` messages, and the deterministic Pet State Engine emits `pet_update` plus short response events.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 -m pytest -q
uvicorn src.main:app --reload
```

Then open `http://127.0.0.1:8000/`.

The voice path is intentionally not wired yet. The next slice is persistence, then Deepgram/Cartesia once the text mood loop feels fun.
