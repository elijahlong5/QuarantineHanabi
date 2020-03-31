import pytest
import requests
from rest_framework import status

from game import models


@pytest.mark.integration
def test_create_game(live_server):
    lobby = models.Lobby.objects.create()
    sean = lobby.members.create(name="Sean")
    gus = lobby.members.create(name="Gus")

    response = requests.post(f"{live_server}/api/lobbies/{lobby.code}/games/")
    assert response.status_code == status.HTTP_201_CREATED

    game = response.json()

    assert game["id"]
    assert game["is_in_progress"]

    assert_player_list_matches(game["players"], sean, gus)


def assert_player_list_matches(player_list, *players):
    players = list(players)

    assert len(player_list) == len(
        players
    ), "The lists have different lengths."

    used_orders = set()
    for player_rep in player_list:
        assert player_rep["id"]

        assert player_rep["order"] not in used_orders
        used_orders.add(player_rep["order"])

        matched_player = assert_player_rep_matches_a_player(
            player_rep, players
        )
        players.remove(matched_player)


def assert_player_rep_matches_a_player(player_rep, players):
    for i, player in enumerate(players):
        if player_rep["name"] == player.name:
            return player

    assert False, f"Received players has unexpected element: {player_rep}"
