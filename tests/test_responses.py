from src.pet_state import PetState
from src.responses import choose_response, droid_cue_for, idle_cue_for, vocal_noise_for


def test_response_is_short_and_conditioned_on_mood():
    cranky = choose_response(PetState(mood="cranky"), "you are boring")
    playful = choose_response(PetState(mood="playful"), "good gremlin snack")

    assert cranky != playful
    assert len(cranky.split()) <= 30
    assert len(playful.split()) <= 30


def test_each_mood_has_a_short_uwu_noise():
    noises = {
        mood: vocal_noise_for(PetState(mood=mood))
        for mood in ["happy", "playful", "cranky", "sad", "sleepy", "glitch"]
    }

    assert noises["playful"] == "bzz-uwu"
    assert noises["cranky"].endswith("uwu")
    assert all(1 <= len(noise.split()) <= 2 for noise in noises.values())


def test_response_can_include_uwu_noise_without_getting_long():
    response = choose_response(PetState(mood="playful"), "good gremlin snack", include_noise=True)

    assert response.startswith("bzz-uwu")
    assert len(response.split()) <= 32


def test_similar_happy_chatter_has_more_variety():
    messages = [
        "okay stop",
        "got safe",
        "the videos",
        "respect",
        "doing as you live",
        "same to you",
        "tell me more",
        "fine then",
    ]

    responses = {choose_response(PetState(mood="happy"), message) for message in messages}

    assert len(responses) >= 5
    assert all(len(response.split()) <= 30 for response in responses)


def test_droid_vocal_noises_vary_for_similar_chatter():
    messages = [
        "okay stop",
        "got safe",
        "the videos",
        "respect",
        "doing as you live",
        "same to you",
    ]

    noises = {droid_cue_for(PetState(mood="happy"), seed=message)["vocal_text"] for message in messages}

    assert len(noises) >= 3
    assert all(1 <= len(str(noise).split()) <= 3 for noise in noises)


def test_droid_cue_contains_short_vocal_text_and_playable_sequence():
    cue = droid_cue_for(PetState(mood="playful"), category="turn_ack", seed="good gremlin snack")

    assert cue["category"] == "turn_ack"
    assert cue["mood"] == "playful"
    assert cue["vocal_text"] == "bzz-uwu"
    assert len(str(cue["vocal_text"]).split()) <= 3
    assert cue["sequence"]
    for note in cue["sequence"]:
        assert note["frequency"] > 0
        assert 0 < note["duration"] <= 0.5


def test_idle_cue_policy_escalates_with_idle_time_and_neglect():
    playful = PetState(mood="playful")
    upset = PetState(mood="sad", attention_debt=80, neglect_stage="upset")
    left = PetState(mood="glitch", neglect_stage="left")

    assert idle_cue_for(playful, idle_seconds=30) is None
    assert idle_cue_for(playful, idle_seconds=60)["category"] == "idle_probe"
    assert idle_cue_for(playful, idle_seconds=180)["category"] == "idle_mumble"
    assert idle_cue_for(upset, idle_seconds=60)["category"] == "neglect_alarm"
    assert idle_cue_for(left, idle_seconds=60)["mood"] == "glitch"