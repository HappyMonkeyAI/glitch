# GLITCH MVP Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a browser-first voice cyber pet with persistent vitals, ASCII mood UI, and a short sassy voice loop.

**Architecture:** Start from the `voice-assistant` FastAPI/WebSocket architecture. Replace lead extraction with a deterministic Pet State Engine and send `pet_update` events to a single-page low-fi frontend.

**Tech Stack:** Python, FastAPI, Pydantic, SQLite WAL, vanilla HTML/CSS/JS, Deepgram STT, Cartesia TTS, OpenAI-compatible LLM.

---

### Phase 0: Repo scaffold

**Objective:** Create the minimal app structure without copying reference repo business logic.

**Files:**
- Create: `src/main.py`
- Create: `src/pet_state.py`
- Create: `src/index.html`
- Create: `tests/test_pet_state.py`
- Create: `requirements.txt`
- Create: `.env.example`

**Steps:**
1. Add dependencies: `fastapi`, `uvicorn[standard]`, `pydantic`, `python-dotenv`, `openai`, `deepgram-sdk`, `cartesia`, `pytest`.
2. Add a FastAPI app that serves `/` and exposes `/ws`.
3. Add a placeholder WebSocket protocol: client text message -> backend returns `pet_update` and `response_text`.
4. Run `python -m py_compile src/main.py src/pet_state.py`.

### Phase 1: Pet State Engine

**Objective:** Make mood and vitals deterministic and testable.

**Files:**
- Modify: `src/pet_state.py`
- Test: `tests/test_pet_state.py`

**State model:**
- `mood`, `affection`, `energy`, `hunger`, `attention_debt`, `neglect_stage`, `face`, `background`.

**Test cases:**
1. Praise increases affection and sets happy/playful face.
2. Insults or harsh tone reduce affection and can set cranky face.
3. Feeding keywords reduce hunger.
4. Time decay increases hunger/attention debt.
5. Extreme neglect sets `neglect_stage="left"` and glitch/sad visual state.

**Verification:**
Run `pytest tests/test_pet_state.py -v`.

### Phase 2: SQLite WAL persistence

**Objective:** Persist current pet state and timeline events.

**Files:**
- Create: `src/storage.py`
- Modify: `src/main.py`
- Test: `tests/test_storage.py`

**Tables:**
- `pet_state(key TEXT PRIMARY KEY, value TEXT, updated_at DATETIME)` or one-row JSON state.
- `timeline(id INTEGER PRIMARY KEY, event_type TEXT, payload TEXT, created_at DATETIME)`.
- `rescue_links(id TEXT PRIMARY KEY, status TEXT, payload TEXT, created_at DATETIME)`.

**Verification:**
Run `pytest tests/test_storage.py -v` and manually inspect that WAL mode is enabled.

### Phase 3: Low-fi frontend

**Objective:** Render GLITCH as a big ASCII face with mood background.

**Files:**
- Modify: `src/index.html`

**Behaviour:**
- Connect to `/ws`.
- Render `face`, `mood`, and vital bars from `pet_update`.
- Switch CSS classes for happy/cranky/sad/sleepy/glitch.
- Provide text input first; microphone button can follow.

**Verification:**
Run the app and send test messages. Confirm background/face changes with WebSocket events.

### Phase 4: Voice pipeline

**Objective:** Add the real speech loop after text mood changes work.

**Files:**
- Modify: `src/main.py`
- Modify: `src/index.html`

**Behaviour:**
- Browser streams mic audio to `/ws`.
- Backend streams to Deepgram.
- Final transcripts update pet state and call the response LLM.
- Cartesia streams audio back to browser.

**Verification:**
Run a manual browser test with real `DEEPGRAM_API_KEY`, `CARTESIA_API_KEY`, and `LLM_*` settings.

### Phase 5: Personality prompt

**Objective:** Make GLITCH speak in short, sassy, non-anime lines conditioned on vitals.

**Files:**
- Create: `src/personality.py`
- Test: `tests/test_personality.py`

**Rules:**
- Keep responses 1-2 sentences.
- No markdown, no roleplay stage directions in spoken output.
- Roast behaviour, not identity.
- Include current mood/vitals in the system prompt.

**Verification:**
Snapshot-test prompt construction and run a few manual transcript turns.

### Phase 6: Share hooks

**Objective:** Add explicit, privacy-safe viral primitives.

**Files:**
- Create: `src/share.py`
- Modify: `src/storage.py`
- Modify: `src/index.html`

**Features:**
- Generate a rescue link when neglect stage reaches `left`.
- Add a local-only reaction-card export first: face + mood + selected transcript line.
- Do not auto-share private transcripts.

**Verification:**
Create a rescue link in tests and confirm the exported reaction card contains only explicit selected text.
