from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Literal

Mood = Literal["happy", "playful", "cranky", "sad", "sleepy", "glitch"]
NeglectStage = Literal["none", "annoyed", "upset", "left"]

PRAISE_WORDS = {"good", "great", "nice", "love", "proud", "clever", "cute", "thanks", "thank"}
HARSH_WORDS = {"awful", "hate", "boring", "bad", "stupid", "useless", "shut", "annoying"}
FEEDING_WORDS = {"snack", "snacks", "feed", "feeding", "food", "treat", "battery", "cookie"}

VISUALS: dict[Mood, tuple[str, str]] = {
    "happy": ("[^._.^]", "happy"),
    "playful": ("(◕‿◕)", "happy"),
    "cranky": ("(ಠ_ಠ)", "cranky"),
    "sad": ("(._.)", "sad"),
    "sleepy": ("(-_-) zzz", "sleepy"),
    "glitch": ("[ERROR]", "glitch"),
}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _clamp(value: int, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, value))


@dataclass(frozen=True)
class PetState:
    mood: Mood = "happy"
    affection: int = 60
    energy: int = 75
    hunger: int = 20
    attention_debt: int = 0
    last_interaction_at: datetime | None = None
    neglect_stage: NeglectStage = "none"
    face: str = "[^._.^]"
    background: str = "happy"

    def as_event(self) -> dict[str, object]:
        return {
            "mood": self.mood,
            "affection": self.affection,
            "energy": self.energy,
            "hunger": self.hunger,
            "attention_debt": self.attention_debt,
            "last_interaction_at": self.last_interaction_at.isoformat() if self.last_interaction_at else None,
            "neglect_stage": self.neglect_stage,
            "face": self.face,
            "background": self.background,
        }


def with_visuals(state: PetState) -> PetState:
    visual = VISUALS[state.mood]
    face, background = visual  # type: ignore[misc]
    return replace(state, face=face, background=background)


def _signals(message: str) -> dict[str, bool]:
    words = {part.strip(".,!?;:()[]{}'\"").lower() for part in message.split()}
    lowered = message.lower()
    return {
        "praise": bool(words & PRAISE_WORDS),
        "harsh": bool(words & HARSH_WORDS),
        "feeding": bool(words & FEEDING_WORDS) or "brought snacks" in lowered,
        "boring": "boring" in words,
    }


def handle_user_message(state: PetState, message: str, now: datetime | None = None) -> tuple[PetState, dict[str, object]]:
    now = now or _now()
    state = apply_time_decay(state, now=now)
    signals = _signals(message)

    affection = state.affection
    hunger = state.hunger
    energy = state.energy
    attention_debt = state.attention_debt

    if signals["praise"]:
        affection += 16
        attention_debt -= 10
    if signals["harsh"]:
        affection -= 22
        energy -= 6
    if signals["feeding"]:
        hunger -= 35
        affection += 6
        attention_debt -= 5

    energy -= 3
    attention_debt = _clamp(attention_debt - 8)
    affection = _clamp(affection)
    hunger = _clamp(hunger)
    energy = _clamp(energy)

    mood: Mood
    if state.neglect_stage == "left" and not (signals["feeding"] or signals["praise"]):
        mood = "glitch"
    elif signals["harsh"] or affection < 35:
        mood = "cranky"
    elif hunger > 80 or attention_debt > 75:
        mood = "sad"
    elif energy < 20:
        mood = "sleepy"
    elif signals["feeding"] or signals["praise"]:
        mood = "playful" if affection >= 70 else "happy"
    else:
        mood = state.mood if state.mood != "glitch" else "cranky"

    neglect_stage: NeglectStage = "none" if attention_debt < 35 else "annoyed" if attention_debt < 70 else "upset"
    updated = PetState(
        mood=mood,
        affection=affection,
        energy=energy,
        hunger=hunger,
        attention_debt=attention_debt,
        last_interaction_at=now,
        neglect_stage=neglect_stage,
    )
    updated = with_visuals(updated)
    event = {"type": "interaction", "message": message, "signals": signals, "state": updated.as_event()}
    return updated, event


def apply_time_decay(state: PetState, now: datetime | None = None) -> PetState:
    now = now or _now()
    if state.last_interaction_at is None:
        return with_visuals(replace(state, last_interaction_at=now))

    elapsed_seconds = max(0, int((now - state.last_interaction_at).total_seconds()))
    elapsed_hours = elapsed_seconds / 3600
    if elapsed_hours <= 0:
        return with_visuals(state)

    hunger = _clamp(state.hunger + int(elapsed_hours * 5))
    attention_debt = _clamp(state.attention_debt + int(elapsed_hours * 7))
    energy = _clamp(state.energy + int(elapsed_hours * 3))
    affection = _clamp(state.affection - int(elapsed_hours * 1.5))

    if elapsed_hours >= 48 or attention_debt >= 95:
        neglect_stage: NeglectStage = "left"
        mood: Mood = "glitch"
    elif attention_debt >= 70:
        neglect_stage = "upset"
        mood = "sad"
    elif attention_debt >= 35:
        neglect_stage = "annoyed"
        mood = "cranky"
    elif energy < 20:
        neglect_stage = "none"
        mood = "sleepy"
    else:
        neglect_stage = "none"
        mood = state.mood

    return with_visuals(
        replace(
            state,
            mood=mood,
            affection=affection,
            energy=energy,
            hunger=hunger,
            attention_debt=attention_debt,
            neglect_stage=neglect_stage,
        )
    )
