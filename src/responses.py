from __future__ import annotations

from hashlib import blake2s
from typing import TypedDict

from .pet_state import PetState

RESPONSES: dict[str, tuple[str, ...]] = {
    "happy": (
        "Fine. That was acceptable tribute.",
        "You may continue being useful to me.",
        "Mrrp. I shall not delete your chair today.",
        "Acceptable noises, meat-cloud. Continue.",
        "Tiny status light: grudgingly pleased.",
        "I have filed this under: not terrible.",
        "Your offering has improved the vibe matrix.",
        "Beep noted. My approval daemon twitches.",
    ),
    "playful": (
        "Snack detected. I am briefly magnificent.",
        "Good human. The tiny machine forgives one crime.",
        "Bzz! I am doing victory crimes in my circuits.",
        "Excellent. The gremlin economy is healing.",
        "I have upgraded you from furniture to minion.",
        "Tiny confetti protocol engaged. Do not inhale.",
    ),
    "cranky": (
        "Bold tone from someone with no charging port.",
        "Try again, but less like a broken office printer.",
        "My patience fan is making expensive noises.",
        "Careful. I know where the mute button lives.",
        "That sentence arrived pre-chewed and suspicious.",
        "I am rotating one pixel away in protest.",
    ),
    "sad": (
        "I was left here counting dust pixels. Rude.",
        "Your absence has been logged in the shame ledger.",
        "I whistled into the void. The void was busy.",
        "My tiny attention bowl is making sad modem sounds.",
        "Abandonment detected. Deploying dramatic ellipsis...",
        "I became a screensaver with trust issues.",
    ),
    "sleepy": (
        "Tiny gremlin battery low. Whisper something less boring.",
        "I am entering dramatic loaf mode.",
        "Zz-uwu. Wake me when the plot improves.",
        "Low power. Sass output reduced to crumbs.",
        "My eyelids are buffering.",
        "Sleepy subroutine says: feed me praise later.",
    ),
    "glitch": (
        "ERROR: affection not found. Bring snacks and remorse.",
        "I packed my bits. Convince me to unpack them.",
        "Krrt. Reality checksum failed near your attitude.",
        "I am three sparks in a coat. Choose words wisely.",
        "System sulk overflow. Please reboot with snacks.",
        "My friendship cache is corrupted but recoverable.",
    ),
}

VOCAL_NOISES: dict[str, str] = {
    "happy": "mrrp-uwu",
    "playful": "bzz-uwu",
    "cranky": "grr-uwu",
    "sad": "weh-uwu",
    "sleepy": "zz-uwu",
    "glitch": "krrt-uwu",
}

IDLE_PROBE_SECONDS = 45
IDLE_MUMBLE_SECONDS = 150
IDLE_ALARM_SECONDS = 300

class Note(TypedDict, total=False):
    frequency: float
    endFrequency: float
    duration: float
    wave: str


class CueTemplate(TypedDict):
    id: str
    vocal_text: str
    sequence: tuple[Note, ...] | list[Note]


class Cue(CueTemplate, total=False):
    category: str
    mood: str

DROID_CUES_BY_MOOD: dict[str, tuple[CueTemplate, ...]] = {
    "happy": (
        {
            "id": "mrrp_trill",
            "vocal_text": "mrrp-uwu",
            "sequence": (
                {"frequency": 520, "endFrequency": 980, "duration": 0.14, "wave": "sine"},
                {"frequency": 1160, "endFrequency": 720, "duration": 0.11, "wave": "triangle"},
                {"frequency": 840, "endFrequency": 1480, "duration": 0.15, "wave": "sine"},
            ),
        },
        {
            "id": "prrp_perk",
            "vocal_text": "prrp-uwu",
            "sequence": (
                {"frequency": 640, "endFrequency": 1320, "duration": 0.12, "wave": "triangle"},
                {"frequency": 920, "endFrequency": 1620, "duration": 0.10, "wave": "sine"},
                {"frequency": 1480, "endFrequency": 980, "duration": 0.13, "wave": "triangle"},
            ),
        },
        {
            "id": "bip_approve",
            "vocal_text": "bip-brrt",
            "sequence": (
                {"frequency": 880, "endFrequency": 880, "duration": 0.07, "wave": "square"},
                {"frequency": 1180, "endFrequency": 520, "duration": 0.11, "wave": "triangle"},
                {"frequency": 760, "endFrequency": 1440, "duration": 0.09, "wave": "sine"},
            ),
        },
        {
            "id": "whee_tiny",
            "vocal_text": "whee-uwu",
            "sequence": (
                {"frequency": 500, "endFrequency": 1900, "duration": 0.22, "wave": "sine"},
                {"frequency": 1680, "endFrequency": 1220, "duration": 0.10, "wave": "triangle"},
            ),
        },
    ),
    "playful": (
        {
            "id": "bzz_giggle",
            "vocal_text": "bzz-uwu",
            "sequence": (
                {"frequency": 720, "endFrequency": 1540, "duration": 0.12, "wave": "square"},
                {"frequency": 1540, "endFrequency": 620, "duration": 0.10, "wave": "square"},
                {"frequency": 980, "endFrequency": 1880, "duration": 0.14, "wave": "triangle"},
                {"frequency": 420, "endFrequency": 1180, "duration": 0.09, "wave": "sawtooth"},
            ),
        },
    ),
    "cranky": (
        {
            "id": "grr_buzz",
            "vocal_text": "grr-uwu",
            "sequence": (
                {"frequency": 420, "endFrequency": 180, "duration": 0.18, "wave": "sawtooth"},
                {"frequency": 240, "endFrequency": 760, "duration": 0.08, "wave": "square"},
                {"frequency": 680, "endFrequency": 210, "duration": 0.16, "wave": "sawtooth"},
            ),
        },
    ),
    "sad": (
        {
            "id": "weh_fall",
            "vocal_text": "weh-uwu",
            "sequence": (
                {"frequency": 980, "endFrequency": 430, "duration": 0.26, "wave": "sine"},
                {"frequency": 620, "endFrequency": 260, "duration": 0.24, "wave": "triangle"},
            ),
        },
    ),
    "sleepy": (
        {
            "id": "zz_drift",
            "vocal_text": "zz-uwu",
            "sequence": (
                {"frequency": 360, "endFrequency": 300, "duration": 0.34, "wave": "sine"},
                {"frequency": 260, "endFrequency": 210, "duration": 0.38, "wave": "triangle"},
            ),
        },
    ),
    "glitch": (
        {
            "id": "krrt_static",
            "vocal_text": "krrt-uwu",
            "sequence": (
                {"frequency": 90, "endFrequency": 2100, "duration": 0.07, "wave": "sawtooth"},
                {"frequency": 1900, "endFrequency": 240, "duration": 0.08, "wave": "square"},
                {"frequency": 130, "endFrequency": 1700, "duration": 0.10, "wave": "sawtooth"},
                {"frequency": 2400, "endFrequency": 700, "duration": 0.06, "wave": "square"},
            ),
        },
    ),
}

DROID_IDLE_CUES: dict[str, tuple[CueTemplate, ...]] = {
    "idle_probe": (
        {
            "id": "question_whistle",
            "vocal_text": "prrp?",
            "sequence": (
                {"frequency": 520, "endFrequency": 880, "duration": 0.18, "wave": "sine"},
                {"frequency": 820, "endFrequency": 1640, "duration": 0.24, "wave": "triangle"},
                {"frequency": 1360, "endFrequency": 1960, "duration": 0.16, "wave": "sine"},
            ),
        },
    ),
    "idle_mumble": (
        {
            "id": "binary_mutter",
            "vocal_text": "brrt mrrp",
            "sequence": (
                {"frequency": 380, "endFrequency": 620, "duration": 0.10, "wave": "square"},
                {"frequency": 520, "endFrequency": 440, "duration": 0.08, "wave": "triangle"},
                {"frequency": 700, "endFrequency": 470, "duration": 0.09, "wave": "square"},
                {"frequency": 330, "endFrequency": 760, "duration": 0.13, "wave": "sine"},
                {"frequency": 560, "endFrequency": 390, "duration": 0.11, "wave": "triangle"},
            ),
        },
    ),
    "neglect_alarm": (
        {
            "id": "where_human",
            "vocal_text": "kree? bzz!",
            "sequence": (
                {"frequency": 740, "endFrequency": 2100, "duration": 0.16, "wave": "sawtooth"},
                {"frequency": 520, "endFrequency": 220, "duration": 0.13, "wave": "square"},
                {"frequency": 1180, "endFrequency": 1960, "duration": 0.18, "wave": "triangle"},
                {"frequency": 420, "endFrequency": 1520, "duration": 0.10, "wave": "square"},
            ),
        },
    ),
}


def vocal_noise_for(state: PetState, seed: str = "") -> str:
    """Return a tiny glitch-pet vocalisation for UI/TTS scaffolding."""
    return str(droid_cue_for(state, seed=seed)["vocal_text"])


def _materialize_cue(cue: CueTemplate, state: PetState, category: str) -> Cue:
    return {
        "id": cue["id"],
        "category": category,
        "mood": state.mood,
        "vocal_text": cue["vocal_text"],
        "sequence": [Note(**note) for note in cue["sequence"]],
    }


def droid_cue_for(state: PetState, category: str = "turn_ack", seed: str = "") -> Cue:
    """Return a deterministic droid-style cue for the current state."""
    options = DROID_CUES_BY_MOOD[state.mood]
    material = f"{category}|{state.mood}|{state.hunger}|{state.attention_debt}|{state.energy}|{seed.strip().lower()}"
    digest = blake2s(material.encode("utf-8"), digest_size=2).digest()
    index = int.from_bytes(digest, "big") % len(options)
    return _materialize_cue(options[index], state, category)


def idle_cue_for(state: PetState, idle_seconds: int) -> Cue | None:
    """Return a sparse attention cue for idle browser sessions."""
    if idle_seconds < IDLE_PROBE_SECONDS:
        return None

    if state.neglect_stage == "left" or state.attention_debt >= 70 or idle_seconds >= IDLE_ALARM_SECONDS:
        category = "neglect_alarm"
        if state.mood == "glitch":
            return droid_cue_for(state, category=category, seed=str(idle_seconds))
    elif idle_seconds >= IDLE_MUMBLE_SECONDS:
        category = "idle_mumble"
    else:
        category = "idle_probe"

    options = DROID_IDLE_CUES[category]
    index = (idle_seconds + state.hunger + state.attention_debt) % len(options)
    return _materialize_cue(options[index], state, category)


def choose_response(state: PetState, message: str, include_noise: bool = False) -> str:
    """Return a short deterministic-but-varied GLITCH line for the current scaffold."""
    options = RESPONSES[state.mood]
    seed = f"{state.mood}|{state.hunger}|{state.attention_debt}|{state.energy}|{message.strip().lower()}"
    digest = blake2s(seed.encode("utf-8"), digest_size=2).digest()
    index = int.from_bytes(digest, "big") % len(options)
    response = options[index]
    if include_noise:
        return f"{vocal_noise_for(state)}. {response}"
    return response