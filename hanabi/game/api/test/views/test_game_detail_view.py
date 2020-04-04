import pytest
import requests
from rest_framework import status

from game import models


@pytest.mark.integration
def test_get_game_without_player_id_should_return_400(live_server):
    lobby = models.Lobby.objects.create()
    game = models.Game.create_from_lobby(lobby)

    url = f"{live_server}/api/games/{game.id}/"
    response = requests.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_get_game_with_invalid_player_id_should_return_400(live_server):
    lobby = models.Lobby.objects.create()
    game = models.Game.create_from_lobby(lobby)

    url = f"{live_server}/api/games/{game.id}/"
    response = requests.get(url, params={"as_player": "foo"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_get_game_with_valid_player_should_return_game_state(live_server):
    lobby = models.Lobby.objects.create()
    jake = lobby.members.create(name="Jake")
    amy = lobby.members.create(name="Amy")
    game = models.Game.create_from_lobby(lobby)

    url = f"{live_server}/api/games/{game.id}/"
    response = requests.get(url, params={"as_player": jake.name})

    assert response.status_code == status.HTTP_200_OK

    game_state = response.json()

    # Ensure static properties of game are present.
    assert game_state["id"]
    assert game_state["is_in_progress"]

    # Ensure game looks like a new game.
    assert game_state["active_player"] == game.players.first().name
    assert game_state["remaining_bombs"] == 3
    assert game_state["remaining_cards"] == 40  # Each dealt 5 cards
    assert game_state["remaining_hints"] == 8
    # Empty pile for each color
    assert game_state["piles"] == {
        "BLUE": 0,
        "GREEN": 0,
        "RED": 0,
        "WHITE": 0,
        "YELLOW": 0,
    }
    # Empty discard pile
    assert game_state["discards"] == []

    player_reps = game_state["players"]

    jake_state = next(rep for rep in player_reps if rep["name"] == jake.name)
    amy_state = next(rep for rep in player_reps if rep["name"] == amy.name)

    assert len(jake_state["cards"]) == 5
    for card in jake_state["cards"]:
        assert card["id"]
        # The color/number of the player's own cards should not be
        # visible.
        assert "color" not in card
        assert "number" not in card

    assert len(amy_state["cards"]) == 5
    for card in amy_state["cards"]:
        assert card["id"]
        # The color/number of other players' cards should be visible.
        assert card["color"]
        assert card["number"]
