# GLITCH Cyber Pet Deep Research — Open Questions

## Product

1. What is the exact safe sass boundary?
   - Need a written policy and eval examples for behaviour-level roasts vs personal attacks.

2. Is the first audience builders, streamers, or general AI companion users?
   - The MVP can serve builders first, but viral mechanics differ by audience.

3. Does GLITCH need voice on day one?
   - Current recommendation: text loop first, voice second. Needs validation.

4. What daily ritual creates return behaviour without becoming annoying?
   - Candidates: one interesting update, daily snack, project gossip, “explain your absence”.

5. Are rescue links funny or manipulative?
   - Needs UX copy tests. Keep it comedic, not emotionally coercive.

## Technical

1. Which state transitions should be deterministic vs LLM-assisted?
   - Deterministic: hunger, decay, affection bounds, neglect stage.
   - LLM-assisted: sentiment/tone classification, response phrasing.

2. How should voice interruption work safely?
   - Need barge-in only after core voice loop is stable.

3. How should private transcript content be handled in share exports?
   - Recommendation: explicit selected line only, never auto-export.

4. Should SQLite store full transcripts or only derived timeline events?
   - Privacy tradeoff. For MVP, prefer timeline events and user-selected snippets.

5. How will generated audio clips be produced?
   - Start with static reaction card export before video/audio composition.

## Research gaps

1. Better market sizing for AI companions beyond direct page claims.
   - Web search was unavailable in this session; needs follow-up with working search/extract.

2. Real user sentiment on “mean” companions.
   - Need Reddit/X/TikTok examples and comments.

3. App-store monetization patterns for Finch/Replika/Tamagotchi-like apps.
   - Need pricing, retention claims, reviews.

4. Safety norms for AI companions targeting loneliness/attachment.
   - Needed before public launch copy.

5. Streamer overlay demand.
   - Need Twitch/OBS/VTuber adjacent research.
