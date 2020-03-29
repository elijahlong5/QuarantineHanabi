import enum
import uuid

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
