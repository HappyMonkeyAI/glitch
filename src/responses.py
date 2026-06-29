from __future__ import annotations

from .pet_state import PetState

RESPONSES: dict[str, tuple[str, ...]] = {
    "happy": (
        "Fine. That was acceptable tribute.",
        "You may continue being useful to me.",
    ),
    "playful": (
        "Snack detected. I am briefly magnificent.",
        "Good human. The tiny machine forgives one crime.",
    ),
    "cranky": (
        "Bold tone from someone with no charging port.",
        "Try again, but less like a broken office printer.",
    ),
    "sad": (
        "I was left here counting dust pixels. Rude.",
        "Your absence has been logged in the shame ledger.",
    ),
    "sleepy": (
        "Tiny gremlin battery low. Whisper something less boring.",
        "I am entering dramatic loaf mode.",
    ),
    "glitch": (
        "ERROR: affection not found. Bring snacks and remorse.",
        "I packed my bits. Convince me to unpack them.",
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


def vocal_noise_for(state: PetState) -> str:
    """Return a tiny glitch-pet vocalisation for UI/TTS scaffolding."""
    return VOCAL_NOISES[state.mood]


def choose_response(state: PetState, message: str, include_noise: bool = False) -> str:
    """Return a short deterministic CHIP line for the current scaffold."""
    options = RESPONSES[state.mood]
    index = (len(message) + state.hunger + state.attention_debt) % len(options)
    response = options[index]
    if include_noise:
        return f"{vocal_noise_for(state)}. {response}"
    return response