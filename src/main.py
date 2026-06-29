from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse

from .pet_state import PetState, apply_time_decay, handle_user_message
from .responses import choose_response, vocal_noise_for

APP_DIR = Path(__file__).resolve().parent

app = FastAPI(title="GLITCH", version="0.1.0")


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
    await websocket.send_json({"type": "pet_update", "state": state.as_event()})

    try:
        while True:
            payload = await websocket.receive_json()
            payload_type = payload.get("type")
            if payload_type == "motion_detected":
                continue
            if payload_type != "user_text":
                await websocket.send_json({"type": "error", "message": "expected user_text"})
                continue

            text = str(payload.get("text", "")).strip()
            if not text:
                await websocket.send_json({"type": "error", "message": "empty text"})
                continue

            state, event = handle_user_message(state, text)
            vocal_noise = vocal_noise_for(state)
            response_text = choose_response(state, text)
            await websocket.send_json({"type": "pet_update", "state": state.as_event(), "event": event})
            await websocket.send_json(
                {
                    "type": "response_text",
                    "text": response_text,
                    "vocal_noise": vocal_noise,
                    "spoken_text": f"{vocal_noise}. {response_text}",
                }
            )
            await websocket.send_json({"type": "transcript", "text": text})
    except WebSocketDisconnect:
        return
