import pytest
from werkzeug.exceptions import HTTPException

import hanabi
from hanabi import routes
from hanabi.game import HanabiGame, Player
from hanabi.routes import lobby_api


@pytest.fixture(autouse=True)
def flask_context():
    # Have to reset global state every test
    routes.hanabi_lobbies = {}

    with hanabi.app.app_context():
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

    routes.hanabi_lobbies[access_token] = game

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
