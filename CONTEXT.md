# GLITCH Context

## Source-of-truth hierarchy

1. Live code and tests once implemented.
2. `CONTEXT.md` for project rules and architecture intent.
3. `docs/adr/` for durable decisions.
4. `docs/plans/` for work breakdowns; plans are executable guidance, not permanent truth after code diverges.
5. `research/` for external references only.

If docs and code conflict, inspect the code, update the docs, and add/adjust an ADR if the conflict reflects an architecture change.

## Product thesis

GLITCH is an anti-therapy cyber pet: a tiny, voice-enabled, emotionally reactive gremlin that users must entertain, feed with attention, and occasionally apologise to. It should feel like an indie web toy with founder-grade viral hooks, not a generic chatbot skin.

Non-goals:

- Do not build another anime companion, waifu, or submissive assistant.
- Do not make a polished corporate dashboard.
- Do not overbuild account systems, 3D avatars, stores, or social graphs before the core pet loop is fun.

## MVP architecture

Use the existing voice assistant architecture as the primary baseline:

- FastAPI serves the static web page and owns `/ws` pet sessions.
- Browser sends microphone audio chunks to the backend.
- Backend streams audio to Deepgram and receives transcripts.
- Backend passes transcripts through a Pet State Engine and a short-response LLM prompt.
- Backend streams Cartesia PCM audio back to the browser.
- Backend sends JSON state events such as `pet_update`, `status`, `transcript`, and `reaction_clip_ready`.
- SQLite WAL stores pet state and timeline events without blocking voice turns.

Motion-aware behaviour is optional for v2:

- Borrow the browser motion-detection pattern only if webcam presence becomes part of the loop.
- Do not require camera permission for the first public MVP.

## Core state model

Initial persistent state should be intentionally small:

- `mood`: `happy | playful | cranky | sad | sleepy | glitch`
- `affection`: 0-100
- `energy`: 0-100
- `hunger`: 0-100
- `attention_debt`: 0-100
- `last_interaction_at`
- `neglect_stage`: `none | annoyed | upset | left`
- `face`: one of a fixed set of ASCII/emoji expressions
- `background`: one of a fixed set of CSS state tokens

Every user utterance can change state. Time passing can also change state.

## Visual language

Keep the first UI raw and memorable:

- Full-page mood background, e.g. green for fed, red for angry, blue for neglected, black/red for glitch.
- Huge monospaced face in the centre.
- Minimal stats shown as chunky terminal bars.
- Use text/ASCII expressions over anime art or 3D rendering.
- Make screenshots instantly legible on X/TikTok.

Example faces:

- Happy: `[^._.^]`, `(◕‿◕)`
- Cranky: `(ಠ_ಠ)`, `(•̀_•́)`, `凸(｀0´)凸`
- Sad: `(._.)`, `(╥﹏╥)`
- Glitch: `[ERROR]`, `(̶◉̶_̶◉̶)`

## Personality rules

GLITCH is sassy, needy, and funny, but not abusive. It can roast behaviour, not identity.

- Responses should usually be 1-2 sentences.
- It can interrupt boring rambling once interruption support is safe.
- It can demand attention, snacks, gossip, or project updates.
- It must not encourage self-harm, harassment, or unsafe behaviour.
- It must not present itself as therapy or emotional-health support.

## Workflow protocol

- Work in small vertical slices: state model -> UI reaction -> voice turn -> persistence -> sharing.
- Add tests for state transitions before adding personality flourishes.
- Keep frontend vanilla until the loop is validated.
- Preserve low-latency turn-taking; do not add blocking LLM/state calls in the audio path.
- If a product or architecture decision changes the loop, record it in `docs/adr/`.

## What not to do

- Do not copy reference repo code blindly; cherry-pick patterns.
- Do not ship camera permission in MVP unless the user explicitly chooses that route.
- Do not make mood purely prompt-driven; state transitions need deterministic tests.
- Do not store secrets in webroot or commit `.env` files.
- Do not let generated clips include private transcript content without an explicit share action.
