from src.pet_state import PetState
from src.responses import choose_response, vocal_noise_for


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