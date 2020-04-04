import requests
from rest_framework import status


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
