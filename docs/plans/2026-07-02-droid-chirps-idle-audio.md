# Droid Chirps and Idle Attention Audio Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Extend GLITCH from single `*-uwu` speech tokens into a mood-aware droid chirp vocabulary, including idle inquisitive whistles and low-volume mumble/chirp attention bids after user inactivity.

**Architecture:** Keep the pet browser-first and simple. Use deterministic backend cue selection for testability, and use browser Web Audio API for the actual droid-style sound design. Use Web Speech `speechSynthesis` only for short nonsense syllables (`bzz-uwu`, `mrrp`, `krrt`) because full spoken lines break the droid illusion.

**Tech Stack:** Python/FastAPI/WebSocket, deterministic pet state functions, vanilla JS, browser Web Audio API (`AudioContext`, `OscillatorNode`, `GainNode`, optional `BiquadFilterNode`), browser `speechSynthesis` as optional layer.

---

## Feasibility verdict

Achievable with the current system, and it fits the GLITCH identity.

Current repo support already exists:

- `src/responses.py:32-44` has mood -> short vocal token mapping.
- `src/main.py:56-65` already sends `vocal_noise` and `spoken_text` over `/ws`.
- `src/index.html:511-532` already has a Web Audio `playBlip()` oscillator/gain envelope.
- `src/index.html:501-631` already has frontend idle animations and blips.
- `src/index.html:693-719` and `src/index.html:888-914` already use browser `speechSynthesis` for tiny vocalisations.
- `tests/test_responses.py:14-29` already covers short uwu noise behaviour.

Recommended direction: expand procedural chirps first, not generated audio files and not long TTS. Use no Star Wars samples; imitate the interaction pattern only: questioning rising whistles, descending annoyed bloops, clustered binary-like burbles.

External evidence checked:

- MDN Web Audio API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API says Web Audio controls audio sources, effects, visualizations, panning, and more; it includes oscillators and filters.
- MDN OscillatorNode: https://developer.mozilla.org/en-US/docs/Web/API/OscillatorNode describes oscillator nodes as generated periodic waveforms, suitable for constant tones that we can sweep into chirps.
- MDN advanced Web Audio tutorial: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Advanced_techniques covers sound creation, sequencing, envelopes, filters, wavetables, and frequency modulation.
- MDN Web Speech API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API confirms speech synthesis reads text via platform/device synthesizers; this means voice availability and exact output vary by browser, so it should be an optional flavour layer rather than the core sound engine.
- Article MCP search for dev.to/HN was noisy and did not produce useful stack-specific articles; official MDN docs are the primary evidence.

---

## Product constraints

- Keep GLITCH low-fi cyberpet / tiny gremlin / terminal toy, not anime companion.
- Avoid copyrighted recognisable R2-D2 sound samples or exact replicas.
- Idle attention sounds must be opt-in through the existing voice/audio toggle or a nearby setting; do not surprise-play audio before a user gesture.
- Do not play over user speech, pet speech, active mic capture, settings modal interaction, or page hidden state.
- Keep idle probes sparse enough to be charming, not spammy.
- Keep deterministic pet-state tests for cue selection; browser audio synthesis can be smoke-tested by static page assertions plus manual browser check.

---

## Proposed sound model

### Cue categories

1. `turn_ack`
   - When GLITCH responds to a user message.
   - Short, mood-coloured chirp before/with the text log.

2. `touch_react`
   - Existing face pointer interactions.
   - Short tactile chirps: blink/tongue/kawaii.

3. `idle_probe`
   - User has not typed/spoken/touched for a threshold.
   - Curious rising chirp, face glance, log line such as `GLITCH: prrp?`.

4. `idle_mumble`
   - Longer idle/neglect stage.
   - Quiet clustered burbles, not full speech.

5. `neglect_alarm`
   - High attention debt or `neglect_stage` upset/left.
   - Rare sharper trill/glitch burst.

### Initial cue vocabulary

Use abstract cue IDs instead of hardcoding sound recipes everywhere:

- happy: `mrrp_trill`, `pwee_up`, `yip_blip`
- playful: `bzz_giggle`, `doot_doot`, `zip_bloop`
- cranky: `grr_buzz`, `descending_bonk`, `static_snort`
- sad: `weh_fall`, `lonely_ping`, `low_wobble`
- sleepy: `zz_drift`, `soft_boop`, `slow_modem`
- glitch: `krrt_static`, `error_sputter`, `bitcrush_burst`
- idle curious: `question_whistle`, `where_human`, `tiny_scan`
- idle mumble: `binary_mutter`, `soft_complaint`, `dust_pixels`

---

## Task 1: Add deterministic droid cue definitions

**Objective:** Replace the single mood token concept with structured cue metadata while preserving current tests.

**Files:**
- Modify: `src/responses.py`
- Test: `tests/test_responses.py`

**Step 1: Write failing tests**

Add tests that assert:

- `vocal_noise_for(PetState(mood="playful"))` still returns a short text token for compatibility.
- New `droid_cue_for(state, category="turn_ack")` returns a dict with:
  - `id`
  - `category`
  - `vocal_text`
  - `mood`
  - `sequence`
- `sequence` is a non-empty list of notes, each with `frequency`, `duration`, and optional `wave`.
- No cue `vocal_text` exceeds 3 whitespace-separated tokens.

**Step 2: Run failing test**

Run:

`pytest tests/test_responses.py -v`

Expected: fail because `droid_cue_for` does not exist.

**Step 3: Implement minimal cue API**

In `src/responses.py`:

- Add `DROID_CUES_BY_MOOD` and `DROID_IDLE_CUES` constants.
- Add `droid_cue_for(state: PetState, category: str = "turn_ack", seed: str = "") -> dict[str, object]`.
- Keep `vocal_noise_for()` as a compatibility wrapper returning `cue["vocal_text"]` for `turn_ack`.
- Keep `choose_response()` unchanged except where it calls `vocal_noise_for()`.

Suggested deterministic selection:

- Use `(len(seed) + state.hunger + state.attention_debt + state.energy) % len(options)`.
- Do not import `random` for core cue selection.

**Step 4: Run test**

Run:

`pytest tests/test_responses.py -v`

Expected: pass.

---

## Task 2: Add idle cue policy to the backend

**Objective:** Make idle attention bids deterministic and testable instead of pure frontend randomness.

**Files:**
- Modify: `src/responses.py`
- Modify: `src/main.py`
- Test: `tests/test_responses.py`
- Test: `tests/test_main.py`

**Step 1: Write failing tests**

In `tests/test_responses.py`, add cases for a function such as:

`idle_cue_for(state: PetState, idle_seconds: int) -> dict[str, object] | None`

Expected behaviours:

- `idle_seconds < 45` returns `None`.
- `idle_seconds >= 45` returns category `idle_probe`.
- `idle_seconds >= 150` returns category `idle_mumble`.
- `idle_seconds >= 300` or `attention_debt >= 70` returns category `neglect_alarm` or stronger mood-appropriate cue.
- `neglect_stage="left"` returns a glitch cue.

In `tests/test_main.py`, add a WebSocket case:

- connect to `/ws`
- receive initial `pet_update`
- send `{"type":"idle_probe","idle_seconds":60}`
- expect a `sound_cue` event with `category="idle_probe"`
- expect no `response_text` full sentence for idle probes

**Step 2: Run failing tests**

Run:

`pytest tests/test_responses.py tests/test_main.py -v`

Expected: fail because idle cue functions and WebSocket type do not exist.

**Step 3: Implement idle cue policy**

In `src/responses.py`:

- Add `idle_cue_for()`.
- Keep thresholds as named constants:
  - `IDLE_PROBE_SECONDS = 45`
  - `IDLE_MUMBLE_SECONDS = 150`
  - `IDLE_ALARM_SECONDS = 300`

In `src/main.py`:

- Import `droid_cue_for` and `idle_cue_for`.
- For `user_text`, include `sound_cue` alongside `vocal_noise`, or send a separate `sound_cue` event before `response_text`.
- For `idle_probe`, do:
  - parse `idle_seconds`
  - call `apply_time_decay(state)` if needed
  - call `idle_cue_for(state, idle_seconds)`
  - if cue exists, send `{"type":"sound_cue", "cue": cue}`
  - optionally send `pet_update` if decay changed mood/vitals
  - do not generate a text response

**Step 4: Run tests**

Run:

`pytest tests/test_responses.py tests/test_main.py -v`

Expected: pass.

---

## Task 3: Replace one-shot `playBlip()` with reusable droid synth

**Objective:** Create a small Web Audio synth that can play cue sequences, sweeps, and filtered bursts without adding dependencies.

**Files:**
- Modify: `src/index.html`
- Test: `tests/test_main.py`

**Step 1: Write static page assertions**

In `tests/test_main.py::test_root_serves_glitch_page`, add assertions that the page includes:

- `playDroidCue`
- `ensureAudioContext`
- `OscillatorNode` or `createOscillator`
- `BiquadFilterNode` or `createBiquadFilter`
- `sound_cue`
- `glitchIdleChirpsEnabled`

**Step 2: Run failing test**

Run:

`pytest tests/test_main.py::test_root_serves_glitch_page -v`

Expected: fail until frontend code exists.

**Step 3: Implement synth helpers in `src/index.html`**

Refactor the audio section near existing `playBlip()`:

- Maintain one shared `audioCtx` instead of creating a new `AudioContext` on each blip.
- Add `ensureAudioContext()` that resumes the context after a user gesture.
- Add `playTone({ frequency, endFrequency, duration, wave, gain, delay, filter })`.
- Add `playDroidCue(cue)` that iterates `cue.sequence` and schedules tones.
- Keep `playBlip()` as a wrapper around `playDroidCue()` so existing call sites keep working.

Sound design rules:

- Use short durations: 0.04s-0.35s per note.
- Use fast pitch sweeps for question whistles.
- Use descending sweeps for sad/annoyed cues.
- Use square/sawtooth at low gain for cranky/glitch.
- Add very short filtered noise-like bursts only if simple oscillator tones feel too clean; do not add large audio assets in this task.

**Step 4: Run static test**

Run:

`pytest tests/test_main.py::test_root_serves_glitch_page -v`

Expected: pass.

---

## Task 4: Wire WebSocket `sound_cue` events into the frontend

**Objective:** Make backend cues audible and visible in the browser.

**Files:**
- Modify: `src/index.html`
- Test: `tests/test_main.py`

**Step 1: Add failing assertions**

In `tests/test_main.py`, assert root HTML contains:

- `msg.type === 'sound_cue'`
- `playDroidCue(msg.cue)`
- `msg.cue.vocal_text`

**Step 2: Run failing test**

Run:

`pytest tests/test_main.py::test_root_serves_glitch_page -v`

Expected: fail.

**Step 3: Implement frontend event handling**

In `ws.onmessage`:

- For `sound_cue`, call `playDroidCue(msg.cue)` if audio/voice is enabled.
- If `msg.cue.vocal_text` exists and the user enabled speech, call existing `chirp()` with the text; keep it very short.
- Add a log line like `GLITCH: <strong>prrp?</strong>` for idle probes only.
- Do not call `speechSynthesis` for full `response_text` unless the current implementation is intentionally preserved; droid mode should default to cue text only.

**Step 4: Run tests**

Run:

`pytest tests/test_main.py -v`

Expected: pass.

---

## Task 5: Add idle attention scheduler with cooldowns and user control

**Objective:** Make GLITCH occasionally call for attention after inactivity, without becoming annoying or violating browser autoplay rules.

**Files:**
- Modify: `src/index.html`
- Test: `tests/test_main.py`

**Step 1: Add failing static assertions**

Assert the root page includes:

- `scheduleNextAttentionProbe`
- `lastHumanActivityAt`
- `IDLE_PROBE_MIN_MS`
- `document.visibilityState`
- `idleChirpsEnabled`

**Step 2: Run failing test**

Run:

`pytest tests/test_main.py::test_root_serves_glitch_page -v`

Expected: fail.

**Step 3: Implement scheduler**

Frontend behaviour:

- Track `lastHumanActivityAt` on:
  - text input
  - form submit
  - pointerdown on face/main
  - mic speech result
  - settings open/close
- Add `idleChirpsEnabled`; default it to the existing voice/audio enabled state or add a settings checkbox stored as `localStorage.glitchIdleChirpsEnabled`.
- Schedule probes only when:
  - `idleChirpsEnabled` true
  - `voiceEnabled` or music/audio has been enabled at least once, so browser audio context is unlocked
  - `!isPetSpeaking`
  - `!isUserSpeaking`
  - settings modal closed
  - `document.visibilityState === 'visible'`
  - WebSocket is open
- Send `{"type":"idle_probe","idle_seconds": Math.floor((Date.now() - lastHumanActivityAt) / 1000)}`.
- Cooldowns:
  - first curious probe after 45-75s idle with jitter
  - mumble after 150-240s
  - neglect alarm no more than once every 5 minutes
- Reset/snooze after any user action.

**Step 4: Run tests**

Run:

`pytest tests/test_main.py -v`

Expected: pass.

---

## Task 6: Tune TTS droid mode

**Objective:** Preserve the useful Japanese female/uwu voice effect without letting full speech ruin the illusion.

**Files:**
- Modify: `src/index.html`
- Modify: `src/responses.py`
- Test: `tests/test_responses.py`
- Test: `tests/test_main.py`

**Step 1: Add test expectations**

- Cue `vocal_text` is always short.
- `spoken_text` sent by the backend should not include full `response_text` in droid mode; it should be cue-only or omitted in favour of `sound_cue`.
- Page contains a setting label such as `DROID CHIRPS` or `IDLE CHIRPS`.

**Step 2: Implement setting**

Add a setting near voice selection:

- `DROID CHIRPS: on/off`
- Optional `TTS chirp layer: on/off`

Voice-selection scoring improvement:

- Keep existing manual voice select.
- Add score boosts for `ja`, `Japanese`, and female-ish voice names only as a convenience; do not force it.
- Persist user-selected voice as today.

**Step 3: Run tests**

Run:

`pytest tests/test_responses.py tests/test_main.py -v`

Expected: pass.

---

## Task 7: Manual browser verification

**Objective:** Prove the feature works beyond static tests.

**Files:**
- No code changes unless bugs are found.

**Step 1: Run backend tests**

Run:

`pytest -v`

Expected: all tests pass.

**Step 2: Startup check**

Run:

`python -m py_compile src/main.py src/pet_state.py src/responses.py`

Expected: no output / exit code 0.

**Step 3: Start app**

Run:

`uvicorn src.main:app --host 127.0.0.1 --port 8001`

Expected: server starts.

**Step 4: WebSocket smoke check**

Use a small Python websocket client or browser console to verify:

- initial `pet_update`
- `user_text` returns `pet_update`, `sound_cue` or cue-bearing `response_text`, and `transcript`
- `idle_probe` returns `sound_cue` only

**Step 5: Browser check**

In Chrome/Edge/Safari:

- Open `http://127.0.0.1:8001/`.
- Enable voice/audio.
- Pick the Japanese female voice if available.
- Send `good gremlin snack`.
- Confirm chirp is procedural and speech layer is short.
- Wait 60-90s without touching the page.
- Confirm a curious whistle or mumble plays once, not repeatedly.
- Start talking/typing and confirm idle chirps pause.
- Background music ducks while pet/user audio is active.

---

## Acceptance criteria

- `pytest -v` passes.
- Idle attention noises are opt-in/unlocked by user audio interaction.
- Idle probes are state-aware and deterministic in tests.
- No full-sentence idle TTS; only short droid tokens and procedural tones.
- Existing touch blips still work.
- Existing mobile layout remains untouched.
- No new external dependency is required.
- No generated audio files or copyrighted sound samples are committed.

---

## Implementation notes

This is best implemented as a small vertical slice:

1. Backend cue API and tests.
2. Frontend synth helper replacing `playBlip()` internals.
3. WebSocket `sound_cue` handling.
4. Idle scheduler with cooldowns.
5. TTS voice/tiny-token polish.

Do not start with a large audio asset pipeline. Procedural Web Audio is enough for the MVP and easier to tune live in browser devtools.
