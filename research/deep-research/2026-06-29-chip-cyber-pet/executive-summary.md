# CHIP Cyber Pet Deep Research — Executive Summary

Date: 2026-06-29

## Bottom line

CHIP is worth pursuing as a fast MVP, but the strongest version is not “AI companion” in the Replika/Character.ai lane. The sharper wedge is a low-fi, voice-first, anti-therapy cyber pet: more Desktop Goose + Tamagotchi + reactive voice toy than emotional-support chatbot.

The research supports three decisions:

1. Build the first loop as a web toy, not a platform: one face, one mood engine, one voice loop, one shareable reaction artifact.
2. Keep the pet state deterministic: LLMs can generate speech, but hunger/affection/neglect must be rule-driven and testable.
3. Treat virality as the product mechanic, not a marketing add-on: screenshots/clips, dramatic neglect states, and friend rescue links should be part of the core loop.

## Evidence snapshot

Reference pages confirm the crowded “AI friend” category: Replika positions itself as “The AI Friend to do Life With” and its page claimed 42,160,934 users worldwide when fetched. Finch owns the softer “self-care best friend” pet framing. Tamagotchi Uni still emphasizes raising unique characters and playing with personalized friends. Desktop Goose shows that intentionally annoying desktop companions can become memorable because the behaviour is funny and visually legible.

The two MCP research servers were useful but exposed a signal problem: broad dev.to/article searches for “AI companion virtual pet” returned noisy generic AI/product posts. The useful practitioner signals were adjacent rather than direct: Google AI’s “AIventure” retro AI web game, dev.to’s WebSocket real-time app patterns, and articles on agent-first/webMCP interfaces. This suggests CHIP should not wait for perfect tutorials; the reference voice stack plus deterministic game-state design is enough.

## Recommended MVP

Build “CHIP-0”: a browser page with a huge monospaced face, full-page mood colours, typed input first, then voice. Ship the emotional state engine before the full voice pipeline. The first wow moment should be: user says something mean or neglects CHIP; the page flips crimson/black and CHIP roasts them in one short line.

## Main risk

The biggest risk is tonal drift. Too nice becomes Replika/Finch; too mean becomes unsafe or tiresome; too anime becomes a saturated companion category. The right tone is behaviour-level sass: “you abandoned me for six hours, explain yourself,” not personal attacks.

## Next action

Add an MVP “fun loop” phase before the current voice-pipeline phase: text input → deterministic mood transitions → ASCII state changes → 10 hand-authored response templates. Only after that works should the LLM/Cartesia/Deepgram loop be wired back in.
