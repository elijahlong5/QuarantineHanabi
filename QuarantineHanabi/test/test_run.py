import pytest
from werkzeug.exceptions import HTTPException

import run
from Game import HanabiGame, Player
from run import lobby_api


@pytest.fixture(autouse=True)
def flask_context():
    # Have to reset global state every test
    run.hanabi_lobbies = {}

    with run.app.app_context():
        yield


def test_lobby_api():
    # Create fake lobby
    access_token = "foo"
    jim = Player("Jim", 0)
    john = Player("John", 1)
    players = {
        "Jim": jim,
        "John": john,
    }
    game = HanabiGame()
    game.players = players

    run.hanabi_lobbies[access_token] = game

    expected_data = {
        "players": {
            "Jim": {"name": jim.name, "order": jim.turn_order},
            "John": {"name": john.name, "order": john.turn_order},
        }
    }

    response = lobby_api("foo")

    assert response.get_json() == expected_data


def test_lobby_api_invalid_access_token_should_404():
    with pytest.raises(HTTPException) as e:
        lobby_api("foo")

    assert e.value.code == 404
