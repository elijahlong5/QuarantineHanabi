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
    def active_player(self):
        """
        Returns:
            The player that the game is waiting for a move from.
        """
        last_play = (
            self.actions.filter(action_type__in=Action.TURN_ACTION_TYPES)
            .order_by("-created_at")
            .first()
        )
        ordered_players_query = self.players.order_by("order")

        # If no turn-taking plays have happened yet, it is the first
        # player's turn.
        if not last_play:
            return ordered_players_query.first()

        # If there is no player whose turn comes after the previous
        # player, then the game has wrapped back to the first player.
        next_players_query = ordered_players_query.filter(
            order__gt=last_play.player.order
        )
        if not next_players_query.exists():
            return ordered_players_query.first

        # If we are somewhere in the middle of the player order, return
        # the player with next-highest order.
        return next_players_query.first()

    @property
    def piles(self):
        """
        Returns:
            A dictionary containing a map of color names to the highest
            played card for each.
        """
        piles = {}

        colors = self.cards.values_list("color", flat=True).distinct()
        for color in colors:
            last_card = (
                self.cards.filter(
                    color=color, play_action__was_successful=True
                )
                .order_by("-number")
                .first()
            )
            piles[color] = last_card.number if last_card else 0

        return piles

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

    def is_players_turn(self, player):
        """
        Determine if it is a specific player's turn.

        Args:
            player:
                The player to compare to the active player.

        Returns:
            A boolean indicating if it is the provided player's turn.
        """

        return player == self.active_player
