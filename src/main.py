from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse

from .pet_state import PetState, apply_time_decay, handle_user_message
from .responses import choose_response, droid_cue_for, idle_cue_for, vocal_noise_for

APP_DIR = Path(__file__).resolve().parent

app = FastAPI(title="GLITCH", version="0.3.4")


@app.get("/", response_class=HTMLResponse)
def index(response: Response) -> str:
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return (APP_DIR / "index.html").read_text(encoding="utf-8")


@app.get("/glitch.mp3")
def glitch_mp3() -> FileResponse:
    return FileResponse(APP_DIR.parent / "glitch.mp3")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    state = apply_time_decay(PetState())
    last_vocal_noise = ""
    turn_count = 0
    await websocket.send_json({"type": "pet_update", "state": state.as_event()})

    try:
        while True:
            payload = await websocket.receive_json()
            payload_type = payload.get("type")
            if payload_type == "motion_detected":
                continue
            if payload_type == "idle_probe":
                idle_seconds = int(payload.get("idle_seconds", 0))
                state = apply_time_decay(state)
                cue = idle_cue_for(state, idle_seconds)
                if cue:
                    await websocket.send_json({"type": "sound_cue", "cue": cue})
                continue
            if payload_type != "user_text":
                await websocket.send_json({"type": "error", "message": "expected user_text"})
                continue

            text = str(payload.get("text", "")).strip()
            if not text:
                await websocket.send_json({"type": "error", "message": "empty text"})
                continue

            state, event = handle_user_message(state, text)
            turn_count += 1
            sound_cue = droid_cue_for(state, seed=f"{text}|{turn_count}")
            for retry in range(1, 5):
                if sound_cue["vocal_text"] != last_vocal_noise:
                    break
                sound_cue = droid_cue_for(state, seed=f"{text}|{turn_count}|retry-{retry}")
            vocal_noise = str(sound_cue["vocal_text"])
            last_vocal_noise = vocal_noise
            response_text = choose_response(state, text)
            await websocket.send_json({"type": "pet_update", "state": state.as_event(), "event": event})
            await websocket.send_json({"type": "sound_cue", "cue": sound_cue})
            await websocket.send_json(
                {
                    "type": "response_text",
                    "text": response_text,
                    "vocal_noise": vocal_noise,
                    "spoken_text": vocal_noise,
                }
            )
            await websocket.send_json({"type": "transcript", "text": text})
    except WebSocketDisconnect:
        return
