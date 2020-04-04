import pytest

from game import models


@pytest.fixture
def two_card_game(db):
    lobby = models.Lobby.objects.create()
    shawn = lobby.members.create(name="Sean")
    gus = lobby.members.create(name="Gus")

    # Manually create a game so we control the cards
    game = lobby.games.create(is_in_progress=True)
    shawn_player = game.players.create(lobby_member=shawn, order=0)
    gus_player = game.players.create(lobby_member=gus, order=1)

    game.cards.create(color=models.Card.RED, deck_order=0, number=1)
    game.cards.create(color=models.Card.BLUE, deck_order=1, number=1)

    shawn_player.give_card(game.draw_card(shawn_player))
    gus_player.give_card((game.draw_card(gus_player)))

    return game, shawn_player, gus_player
