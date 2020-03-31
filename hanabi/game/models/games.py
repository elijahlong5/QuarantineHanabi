import random
import uuid

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from .cards import Card


class Game(models.Model):
    CARD_COUNT_MAP = {
        1: 3,
        2: 2,
        3: 2,
        4: 2,
        5: 1,
    }

    created_at = models.DateTimeField(
        auto_now_add=True, null=False, verbose_name=_("created at")
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )
    is_in_progress = models.BooleanField(
        null=False, verbose_name=_("in progress")
    )
    lobby = models.ForeignKey(
        "Lobby",
        null=False,
        on_delete=models.CASCADE,
        related_name="games",
        related_query_name="game",
        verbose_name=_("lobby"),
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=False, verbose_name=_("updated at")
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = _("game")
        verbose_name_plural = _("games")

    @classmethod
    def create_from_lobby(cls, lobby):
        """
        Create a new game for the lobby. The game is populated with
        players for each of the members in the lobby in a randomized
        order. The cards for the game are also generated in a random
        order.

        Args:
            lobby:
                The lobby to create the game for.

        Returns:
            The created game.
        """

        members = list(lobby.members.all())
        random.shuffle(members)

        with transaction.atomic():
            game = cls.objects.create(is_in_progress=True, lobby=lobby)

            for i, member in enumerate(members):
                game.players.create(lobby_member=member, order=i)

            colors = [Card.BLUE, Card.GREEN, Card.RED, Card.WHITE, Card.YELLOW]
            cards_per_color = sum(
                cls.CARD_COUNT_MAP[number] for number in cls.CARD_COUNT_MAP
            )
            deck_length = cards_per_color * len(colors)
            deck_order_values = list(range(deck_length))

            for color in colors:
                for number, count in cls.CARD_COUNT_MAP.items():
                    for __ in range(count):
                        game.cards.create(
                            color=color,
                            deck_order=deck_order_values.pop(),
                            number=number,
                        )

        return game
