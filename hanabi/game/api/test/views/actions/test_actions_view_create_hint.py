import pytest
import requests
from rest_framework import status


@pytest.mark.integration
def test_create_hint_for_color(live_server, two_card_game):
    game, shawn, gus = two_card_game

    data = {
        "action_type": "HINT",
        "player_name": shawn.name,
        "hint_action": {
            "color": gus.cards[0].color,
            "target_player_name": gus.name,
        },
    }
    url = f"{live_server}/api/games/{game.id}/actions/"
    response = requests.post(url, json=data)

    assert response.status_code == status.HTTP_201_CREATED, response.json()

    action = response.json()

    assert action["id"]
    assert action["player_name"] == shawn.name

    hint_action = action["hint_action"]

    assert hint_action["color"] == gus.cards[0].color
    assert hint_action["target_player_name"] == gus.name


@pytest.mark.integration
def test_create_hint_for_number(live_server, two_card_game):
    game, shawn, gus = two_card_game

    data = {
        "action_type": "HINT",
        "player_name": shawn.name,
        "hint_action": {
            "number": gus.cards[0].number,
            "target_player_name": gus.name,
        },
    }
    url = f"{live_server}/api/games/{game.id}/actions/"
    response = requests.post(url, json=data)

    assert response.status_code == status.HTTP_201_CREATED, response.json()

    action = response.json()

    assert action["id"]
    assert action["player_name"] == shawn.name

    hint_action = action["hint_action"]

    assert hint_action["number"] == gus.cards[0].number
    assert hint_action["target_player_name"] == gus.name


@pytest.mark.integration
def test_create_hint_with_both_color_and_number(live_server, two_card_game):
    game, shawn, gus = two_card_game

    data = {
        "action_type": "HINT",
        "player_name": shawn.name,
        "hint_action": {
            "color": gus.cards[0].color,
            "number": gus.cards[0].number,
            "target_player_name": gus.name,
        },
    }
    url = f"{live_server}/api/games/{game.id}/actions/"
    response = requests.post(url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_hint_as_wrong_player(live_server, two_card_game):
    game, shawn, gus = two_card_game

    data = {
        "action_type": "HINT",
        "player_name": gus.name,
        "hint_action": {
            "color": shawn.cards[0].color,
            "target_player_name": shawn.name,
        },
    }
    url = f"{live_server}/api/games/{game.id}/actions/"
    response = requests.post(url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_create_hint_for_invalid_player(live_server, two_card_game):
    game, shawn, gus = two_card_game

    data = {
        "action_type": "HINT",
        "player_name": shawn.name,
        "hint_action": {
            "color": gus.cards[0].color,
            "target_player_name": "juliet",  # Juliet doesn't play games
        },
    }
    url = f"{live_server}/api/games/{game.id}/actions/"
    response = requests.post(url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_create_hint_for_self(live_server, two_card_game):
    game, shawn, gus = two_card_game

    data = {
        "action_type": "HINT",
        "player_name": shawn.name,
        "hint_action": {
            "color": shawn.cards[0].color,
            "target_player_name": shawn.name,
        },
    }
    url = f"{live_server}/api/games/{game.id}/actions/"
    response = requests.post(url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_create_hint_with_none_remaining(live_server, two_card_game):
    game, shawn, gus = two_card_game
    actions_url = f"{live_server}/api/games/{game.id}/actions/"

    action_infos = (
        (shawn.name, gus.cards[0].color, gus.name),
        (gus.name, shawn.cards[0].color, shawn.name),
    )

    # Give out all 8 hints, alternating between players
    for i in range(8):
        player_name, color, target_player_name = action_infos[
            i % len(action_infos)
        ]

        data = {
            "action_type": "HINT",
            "player_name": player_name,
            "hint_action": {
                "color": color,
                "target_player_name": target_player_name,
            },
        }
        response = requests.post(actions_url, json=data)
        assert response.status_code == status.HTTP_201_CREATED, response.json()

    # After using all the hints, the next hint should fail
    data = {
        "action_type": "HINT",
        "player_name": shawn.name,
        "hint_action": {
            "color": gus.cards[0].color,
            "target_player_name": gus.name,
        },
    }
    url = f"{live_server}/api/games/{game.id}/actions/"
    response = requests.post(url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
