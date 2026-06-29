from datetime import datetime, timedelta, timezone

from src.pet_state import PetState, apply_time_decay, handle_user_message


def test_praise_increases_affection_and_sets_happy_face():
    state = PetState(affection=50, energy=80, hunger=25, attention_debt=10, mood="cranky")

    updated, event = handle_user_message(state, "good gremlin, you did great", now=datetime(2026, 6, 29, tzinfo=timezone.utc))

    assert updated.affection > 50
    assert updated.mood in {"happy", "playful"}
    assert updated.face in {"[^._.^]", "(◕‿◕)"}
    assert event["signals"]["praise"] is True


def test_harsh_message_reduces_affection_and_sets_cranky_face():
    state = PetState(affection=55, energy=80, hunger=10, attention_debt=0, mood="happy")

    updated, event = handle_user_message(state, "you are awful and boring", now=datetime(2026, 6, 29, tzinfo=timezone.utc))

    assert updated.affection < 55
    assert updated.mood == "cranky"
    assert updated.face in {"(ಠ_ಠ)", "(•̀_•́)"}
    assert event["signals"]["harsh"] is True


def test_feeding_keywords_reduce_hunger():
    state = PetState(hunger=80, affection=40, attention_debt=25)

    updated, event = handle_user_message(state, "I brought snacks and a battery treat", now=datetime(2026, 6, 29, tzinfo=timezone.utc))

    assert updated.hunger < 80
    assert updated.affection > 40
    assert event["signals"]["feeding"] is True


def test_time_decay_increases_hunger_and_attention_debt():
    last_seen = datetime(2026, 6, 29, 8, tzinfo=timezone.utc)
    state = PetState(hunger=10, attention_debt=5, last_interaction_at=last_seen)

    updated = apply_time_decay(state, now=last_seen + timedelta(hours=6))

    assert updated.hunger > 10
    assert updated.attention_debt > 5
    assert updated.neglect_stage in {"annoyed", "upset"}


def test_extreme_neglect_sets_left_stage_and_glitch_visuals():
    last_seen = datetime(2026, 6, 25, 8, tzinfo=timezone.utc)
    state = PetState(hunger=50, attention_debt=70, affection=20, last_interaction_at=last_seen)

    updated = apply_time_decay(state, now=last_seen + timedelta(days=3))

    assert updated.neglect_stage == "left"
    assert updated.mood == "glitch"
    assert updated.face == "[ERROR]"
    assert updated.background == "glitch"
