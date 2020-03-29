import enum
import random
import uuid

from sqlalchemy import ForeignKey, Integer, VARCHAR
from sqlalchemy.dialects.postgresql import UUID

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


class Game(db.Model):

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    is_in_progress = db.Column(db.Boolean, nullable=False)
    lobby_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("lobby.id"), nullable=False
    )

    cards = db.relationship("Card", back_populates="game")
    lobby = db.relationship("Lobby", back_populates="games")

    @classmethod
    def create_with_cards(cls, lobby: "Lobby") -> "Game":
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
        return "".join(random.choices(cls.CODE_CHARACTERS, k=5))


class Player(db.Model):

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    lobby_id = db.Column(
        UUID(as_uuid=True), ForeignKey("lobby.id"), nullable=False
    )
    name = db.Column(VARCHAR, nullable=False)
    order = db.Column(Integer, nullable=False)

    lobby = db.relationship("Lobby", back_populates="players")

    __table_args__ = (
        db.UniqueConstraint("lobby_id", "name", name="uix_lobby_players"),
        db.UniqueConstraint(
            "lobby_id", "order", name="uix_lobby_player_order"
        ),
    )
