# Hermes Guide for CHIP

## Default behaviour

Before implementation work, read `CONTEXT.md`, the relevant ADRs, and the active plan in `docs/plans/`.

## Guardrails

- Treat `research/` as reference material, not project truth.
- Keep the project browser-first and simple until the core pet loop is fun.
- Avoid anime-companion drift; the intended identity is low-fi cyberpet / tiny gremlin / terminal toy.
- Use deterministic pet-state tests for mood/vital changes.
- Keep latency visible in verification: test WebSocket connection, state event emission, and audio path separately.
- Never commit `.env`, API keys, generated private clips, or SQLite data files.

## Validation preferences

When code exists, prefer these gates:

1. Unit tests for the Pet State Engine.
2. Backend import/startup check.
3. WebSocket smoke test for state events.
4. Browser manual check for face/background state transitions.
5. Optional end-to-end voice check with real credentials.

## Reference paths

- `docs/adr/0001-product-identity.md`
- `docs/adr/0002-voice-first-browser-mvp.md`
- `docs/adr/0003-pet-state-and-persistence.md`
- `docs/plans/2026-06-29-chip-mvp.md`
