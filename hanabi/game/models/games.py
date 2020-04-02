import random
import uuid

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from .actions import DrawAction, Action
from .cards import Card


class Game(models.Model):
    CARD_COUNT_MAP = {
        1: 3,
        2: 2,
        3: 2,
        4: 2,
        5: 1,
    }
    INITIAL_BOMB_COUNT = 3

    HAND_SIZE = 4

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
            random.shuffle(deck_order_values)

            for color in colors:
                for number, count in cls.CARD_COUNT_MAP.items():
                    for __ in range(count):
                        game.cards.create(
                            color=color,
                            deck_order=deck_order_values.pop(),
                            number=number,
                        )
            game.deal()
        return game

    @property
    def remaining_bombs(self):
        failed_plays = self.actions.filter(
            play_action__was_successful=False
        ).count()

        return max(0, self.INITIAL_BOMB_COUNT - failed_plays)

    @property
    def remaining_cards(self):
        deck_size = self.cards.count()
        drawn_cards = self.actions.filter(draw_action__isnull=False).count()

        return deck_size - drawn_cards

    def deal(self):
        hand_size = 5 if self.players.count() < 4 else 4
        for __ in range(hand_size):
            for player in self.players.order_by("order"):
                player.give_card(self.draw_card(player))

    def draw_card(self, player):
        card = (
            self.cards.filter(draw_action__isnull=True)
            .order_by("deck_order")
            .first()
        )
        action = self.actions.create(action_type=Action.DRAW, player=player)

        return DrawAction.objects.create(action=action, card=card)

    def is_playable(self, card):
        if card.number == 1:
            return not self.actions.filter(
                play_action__card__color=card.color,
                play_action__was_successful=True,
            ).exists()

        return self.actions.filter(
            play_action__card__color=card.color,
            play_action__card__number=card.number - 1,
            play_action__was_successful=True,
        ).exists()
