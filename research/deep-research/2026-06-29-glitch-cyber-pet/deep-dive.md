# GLITCH Cyber Pet Deep Research — Deep Dive

Date: 2026-06-29

## Scope and method

Question: how should GLITCH evolve from a voice-assistant pivot into a startup-shaped, viral, non-anime AI cyber pet?

Sources used:

- `article_research` MCP: `plan_article_research`, `search_articles`, `build_topic_brief` across dev.to, Hacker News Algolia, and RSS.
- `devto` MCP: `search_by_tech` and `get_devto_article` for full dev.to bodies.
- Direct fetched pages: Replika, Finch, Tamagotchi Uni, Desktop Goose, Friend.
- Existing GLITCH docs and reference repos.

Caveat: Hermes web search / Firecrawl was unavailable in this session, and the local deep-research graph path was not present. This report therefore uses MCP article sources plus direct page verification rather than broad web extraction.

Raw evidence files:

- `research/notes/mcp-research-raw.json`
- `research/notes/devto-full-articles.json`
- `research/notes/competitor-pages.json`

---

## 1. Technical lens

The existing architecture is enough for the MVP. `voice-assistant` already provides the hard part: FastAPI WebSockets, Deepgram STT, Cartesia TTS, OpenAI-compatible LLM calls, SQLite WAL, and a browser audio UI. GLITCH should not start by adding more infrastructure.

The new technical requirement is not “better AI”; it is a deterministic Pet State Engine. Mood, hunger, affection, energy, attention debt, and neglect stage should be state-machine outputs, not free-form LLM outputs. LLMs can classify tone or generate speech, but the state transition must be testable.

MCP findings:

- dev.to article `How we built AIventure, an AI-Powered Retro Dungeon` shows a relevant pattern: AI can be embedded into a retro web-game wrapper where the novelty is not a general chatbot but a small playable world.
- dev.to WebSocket examples reinforce that real-time state feedback and live-room energy matter. For GLITCH, that maps to immediate face/background changes before TTS finishes.
- The `Polymarket's price WebSocket can stall while connected` hit is not product-relevant, but it is a useful engineering reminder: WebSockets need heartbeat/stall detection once GLITCH uses long-lived voice streams.

Technical implication: Phase order should be `state engine -> ASCII UI -> text loop -> persistence -> voice`, not `voice -> prompt -> UI`.

---

## 2. Economic lens

The low-fi direction is economically attractive because it avoids expensive avatar/rendering work. A static webpage with ASCII faces can validate retention and sharing before spending on 3D avatars, mobile apps, or desktop overlays.

Likely monetization paths, in order of feasibility:

1. Paid “personalities” or modes: goblin, gremlin, productivity bully, cozy pet, chaos pet.
2. Voice packs once voice is proven.
3. Persistent memory / “lifelong pet” tier.
4. Desktop overlay / streamer mode.
5. Reaction clip export templates.

Avoid early monetization that fights the toy loop. Subscriptions only make sense if users return for days, not if the demo is a one-off joke.

---

## 3. Historical lens

GLITCH sits between three precedents:

- Tamagotchi: durable care loop, neglect consequences, portable identity.
- Desktop Goose: annoying/funny ambient presence that users share because behaviour is legible.
- AI companions such as Replika: emotional continuity and memory.

The historical lesson is that “neediness” works when it is bounded. Tamagotchi-style care loops are engaging because the rules are understandable. Desktop Goose-style annoyance works because the joke is immediate. AI companion intimacy can create retention, but it also drags the product into therapy/romance expectations.

GLITCH should borrow care and consequence, not therapeutic intimacy.

---

## 4. Business lens

The AI companion category is crowded. Replika’s page explicitly positions as an “AI friend” and claimed 42,160,934 users worldwide when fetched. Finch occupies a self-care pet lane. Character.ai is a broad character-chat platform, though its page returned 403 in this session. Friend positions around ambient companionship hardware (“Your new roommate is waiting”).

GLITCH’s best wedge is anti-positioning:

- Not AI girlfriend/boyfriend.
- Not therapist.
- Not general character chat.
- Not productivity assistant.
- A tiny reactive gremlin with a voice.

The business opportunity is not to out-feature incumbents. It is to be instantly understandable in a 5-second clip.

---

## 5. Strategic lens

Strategic priority: own a visual and behavioural meme before building a platform.

A red page with `(ಠ_ಠ)` saying “you came crawling back after six hours?” is more memorable than an elegant avatar saying “welcome back.” The low-fi constraint is a strategic asset: it reduces build time and makes clips legible on X/TikTok.

The dev.to `agent-first approach to building products` article is indirectly relevant: it argues that agent-visible surfaces matter. GLITCH can apply this by exposing a simple local MCP/API later, so agents or workflows can “feed” GLITCH events. But that is v2; do not let agent integrations distract from the toy loop.

---

## 6. Customer lens

Likely early users:

1. Builders/devs who like weird toys and voice demos.
2. Streamers / screen-recording users who want funny on-screen reactions.
3. Indie game people who enjoy Tamagotchi/Desktop Goose energy.
4. AI power users tired of polite assistants.

Jobs to be done:

- “Give me a funny little thing to talk to while I work.”
- “Make my screen recording more entertaining.”
- “Let me show friends the weird thing my AI pet said.”
- “I want an AI companion that is not romantic, therapeutic, or anime-coded.”

The onboarding question should not be “tell me about yourself.” It should be “feed GLITCH one interesting thing or accept consequences.”

---

## 7. Product lens

Recommended MVP loop:

1. Open page.
2. GLITCH loads persisted state and applies time decay.
3. Face/background immediately reflects current state.
4. User types or speaks one utterance.
5. Pet State Engine updates vitals.
6. GLITCH replies in one short line.
7. User can export a reaction card/clip.

First state map:

- Happy/fed: green, `[^._.^]`, asks for more gossip.
- Cranky: red, `(ಠ_ಠ)`, short clipped replies.
- Sad/neglected: blue, `(._.)`, guilt-trip but safe.
- Glitch/rage: black/red, `[ERROR]`, repetitive dramatic lines.
- Sleepy: dim purple/gray, low-energy line.

Use hand-authored templates before relying on the LLM. The LLM can expand once the deterministic loop is fun.

---

## 8. Contrarian lens

The strongest objection: this could be a novelty that burns out after one session. A sassy pet is funny once; retention requires evolving state, memory, and social pressure.

Countermeasures:

- Give GLITCH a daily “one interesting thing” ritual.
- Make neglect states visible without being emotionally manipulative.
- Make users want to screenshot the state, not just read the response.
- Add friend rescue links only after the base loop works.

Another objection: “anti-therapy” can become mean or unsafe. The answer is to constrain roasts to behaviour, time, and interaction quality. Never roast identity, appearance, mental health, or protected traits.

---

## 9. First-principles lens

A digital pet is a stateful feedback loop:

- It has needs.
- The user performs actions.
- The pet visibly changes.
- Time matters.
- The user feels responsible enough to return.

AI is useful only if it makes the feedback loop feel alive. It is not the core product. The core product is persistent state plus immediate emotional display.

Therefore, build the smallest possible living loop. Voice is a multiplier. The ASCII face is the interface. Persistence is the retention engine. Sharing is the growth engine.

---

## Product recommendations

### Change the implementation plan

Insert a new Phase 1.5 before full voice:

- Build `response_templates.py` with 30 hand-authored lines across moods.
- Add state-transition tests for praise, neglect, insult, feeding, boredom, and return-after-absence.
- Add screenshot-friendly reaction card export.
- Add a debug panel showing why state changed.

### Keep camera/motion as v2

Motion awareness is tempting, but webcam permission increases friction. Use browser-first text/voice first. Later, a desktop overlay or camera-presence mode can borrow from `motion-aware-voice-chat-bot`.

### Viral experiments

1. “GLITCH is mad at me” reaction card.
2. “Forgiveness link” after neglect.
3. Daily judgement prompt.
4. Streamer overlay once web loop is proven.

---

## Source notes

- Replika page fetched: title “Replika | The AI Friend to do Life With”; description “Meet Replika, the AI companion to do life with”; page text claimed “42,160,934 users worldwide”.
- Finch page fetched: title/description “Finch - Your New Self-Care Best Friend”.
- Tamagotchi Uni page fetched: official site description says users raise unique Tamagotchi characters and play with personalized friends from around the world.
- Desktop Goose itch page fetched: description says “I have created a goose that lives on your desktop. He is an asshole”; page text describes nabbing the mouse, tracking mud, leaving messages, and delivering memes.
- Friend page fetched: title “Friend”; description “Your new roommate is waiting.”
- dev.to full articles fetched through `devto` MCP: AIventure, agent-first products, WebSocket quiz platform, webMCP demo, persona/eval generation.
