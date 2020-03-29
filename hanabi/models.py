import enum
import random
import uuid

from sqlalchemy import func, VARCHAR, Integer
from sqlalchemy.dialects.postgresql import UUID, ENUM

from hanabi import db


CARD_COUNT_MAP = {
    1: 3,
    2: 2,
    3: 2,
    4: 2,
    5: 1,
}
"""
A map specifying how many cards of each number should be created.
"""


class ActionType(enum.Enum):
    DISCARD = 1
    DRAW = 2
    HINT = 3
    PLAY = 4
    SET_HAND_ORDER = 5


class CardColor(enum.Enum):
    """
    Colors that a card can have.

    Note that this is tied to the database, so changing values here will change
    values of existing cards.
    """

    BLUE = 0
    GREEN = 1
    RED = 2
    WHITE = 3
    YELLOW = 4


class Action(db.Model):

    action_type = db.Column(db.Enum(ActionType), nullable=False)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    game_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("game.id"), nullable=False
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    player_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("player.id"), nullable=False
    )

    game = db.relationship("Game", back_populates="actions")
    player = db.relationship("Player", back_populates="actions")

    __table_args__ = (
        db.UniqueConstraint(
            "created_at", "game_id", name="uix_game_action_time"
        ),
    )


class Card(db.Model):

    color = db.Column(db.Enum(CardColor), nullable=False)
    deck_order = db.Column(db.SmallInteger, nullable=False)
    game_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("game.id"), nullable=False
    )
    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    number = db.Column(db.SmallInteger, nullable=False)

    game = db.relationship("Game", back_populates="cards")

    __table_args__ = (
        db.UniqueConstraint(
            "deck_order", "game_id", name="uix_game_card_order"
        ),
    )


class DiscardAction(db.Model):

    action_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("action.id"), nullable=False
    )
    card_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("card.id"), nullable=False
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True)

    action = db.relationship("Action")
    card = db.relationship("Card")


class DrawAction(db.Model):

    action_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("action.id"), nullable=False
    )
    card_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("card.id"), nullable=False
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True)

    action = db.relationship("Action")
    card = db.relationship("Card")


class Game(db.Model):
    INITIAL_BOMB_COUNT = 3

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    is_in_progress = db.Column(db.Boolean, nullable=False)
    lobby_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("lobby.id"), nullable=False
    )

    actions = db.relationship("Action", back_populates="game")
    cards = db.relationship("Card", back_populates="game")
    lobby = db.relationship("Lobby", back_populates="games")

    @classmethod
    def create_with_cards(cls, lobby):
        """
        Initialize a new game with a shuffled deck of cards.

        Args:
            lobby:
                The lobby to create the game in.

        Returns:
            A new game with a set of shuffled cards.
        """
        game = cls(lobby=lobby)

        cards = []
        for color in CardColor:
            for number, count in CARD_COUNT_MAP.items():
                for _ in range(count):
                    cards.append(
                        Card(color=color, game_id=game.id, number=number)
                    )

        order_positions = list(range(len(cards)))
        random.shuffle(order_positions)

        for order, card in zip(order_positions, cards):
            card.deck_order = order

        game.cards = cards

        return game

    @classmethod
    def get_game_for_lobby_or_404(cls, lobby_code: str) -> "Game":
        return (
            cls.query.join(Lobby)
            .filter(Lobby.code == lobby_code)
            .filter(cls.is_in_progress)
            .first_or_404()
        )

    def game_state(self, player_name: str) -> dict:
        return {
            "whose-game-state": player_name,
            "players": {},
            "game-log": [],
            "piles": {},
            "discard-pile": [],
            "bomb-count": self.remaining_bomb_count,
            "whose-turn": self.whose_turn(),
            "cards-in-deck": self.remaining_card_count,
        }

    @property
    def remaining_bomb_count(self):
        """
        Returns:
            The number of remaining bombs left.
        """
        failed_plays = PlayAction.query.filter_by(was_successful=False).count()

        return max(0, self.INITIAL_BOMB_COUNT - failed_plays)

    @property
    def remaining_card_count(self):
        deck_length = Card.query.filter_by(game=self).count()
        drawn_card_count = (
            Card.query.join(DrawAction)
            .join(Action)
            .filter(Action.game == self)
            .count()
        )

        return deck_length - drawn_card_count

    def whose_turn(self):
        """
        Returns:
            The name of the player who the game is waiting for a move
            from.
        """
        players = Player.query.filter_by(lobby=self.lobby).order_by(
            Player.order
        )
        last_play = (
            Action.query.filter(Action.game == self)
            .filter(
                Action.action_type.in_(
                    [ActionType.HINT, ActionType.DISCARD, ActionType.PLAY]
                )
            )
            .order_by(Action.created_at.desc())
            .first()
        )

        if not last_play:
            return players[0].name

        last_player = last_play.player
        new_index = (last_player.order + 1) % len(players)

        return players[new_index].name


class HintAction(db.Model):

    action_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("action.id"), nullable=False
    )
    card_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("card.id"), nullable=False
    )
    color = db.Column(ENUM(CardColor, create_type=False), nullable=True)
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    number = db.Column(db.SmallInteger, nullable=True)
    target_player_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("player.id"), nullable=False
    )

    action = db.relationship("Action")
    target_player = db.relationship("Player")

    __table_args__ = (
        # A hint must either provide a color or a number.
        db.CheckConstraint(
            "(color IS NULL) != (number IS NULL)", name="check_color_or_number"
        ),
    )


class Lobby(db.Model):
    CODE_CHARACTERS = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
    """
    The set of characters that are used to create an access code. The
    set is composed of uppercase ASCII characters and digits, with
    potentially ambiguous characters removed.
    """

    CODE_LENGTH = 5
    """
    The length of the access code used to join the lobby.
    """

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    code = db.Column(VARCHAR(CODE_LENGTH), nullable=False, unique=True)

    games = db.relationship("Game", back_populates="lobby")
    players = db.relationship("Player", back_populates="lobby")

    @classmethod
    def generate_code(cls) -> str:
        """
        Create a random code that can be used to access the lobby.

        Notes
            This is not cryptographically secure. See:
            https://stackoverflow.com/a/23728630/3762084

        Returns
            A random string that can be used to access the lobby.
        """
        return "".join(random.choices(cls.CODE_CHARACTERS, k=cls.CODE_LENGTH))


class PlayAction(db.Model):

    action_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("action.id"), nullable=False
    )
    card_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("card.id"), nullable=False
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    was_successful = db.Column(db.Boolean, nullable=False)

    action = db.relationship("Action")
    card = db.relationship("Card")


class Player(db.Model):

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    lobby_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("lobby.id"), nullable=False
    )
    name = db.Column(VARCHAR, nullable=False)
    order = db.Column(Integer, nullable=False)

    actions = db.relationship("Action", back_populates="player")
    lobby = db.relationship("Lobby", back_populates="players")

    __table_args__ = (
        db.UniqueConstraint("lobby_id", "name", name="uix_lobby_players"),
        db.UniqueConstraint(
            "lobby_id", "order", name="uix_lobby_player_order"
        ),
    )
