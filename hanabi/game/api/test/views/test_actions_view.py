import requests
from rest_framework import status

from game import models


def test_create_play_action(live_server):
    lobby = models.Lobby.objects.create()
    sean = lobby.members.create(name="Sean")
    gus = lobby.members.create(name="Gus")

    # Manually create a game so we control the cards
    game = lobby.games.create(is_in_progress=True)
    sean_player = game.players.create(lobby_member=sean, order=0)
    gus_player = game.players.create(lobby_member=gus, order=1)

    game.cards.create(color=models.Card.RED, deck_order=0, number=1)
    game.cards.create(color=models.Card.BLUE, deck_order=1, number=1)

    sean_player.give_card(game.draw_card(sean_player))
    gus_player.give_card((game.draw_card(gus_player)))

    # Send a play in
    data = {
        "action_type": "PLAY",
        "player_name": sean_player.name,
        "play_action": {"card_id": str(sean_player.cards[0].id)},
    }
    url = f"{live_server}/api/games/{game.id}/actions/"
    response = requests.post(url, json=data)

    assert response.status_code == status.HTTP_201_CREATED

    action = response.json()

    assert action["id"]
    assert action["player_name"] == sean_player.name

    play_action = action["play_action"]

    assert play_action["was_successful"]