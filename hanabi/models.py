import random
import uuid

from sqlalchemy import VARCHAR, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from hanabi import db


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

    players = relationship("Player", back_populates="lobby")

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

    lobby = relationship("Lobby", back_populates="players")

    __table_args__ = (
        db.UniqueConstraint("lobby_id", "name", name="uix_lobby_players"),
        db.UniqueConstraint(
            "lobby_id", "order", name="uix_lobby_player_order"
        ),
    )
