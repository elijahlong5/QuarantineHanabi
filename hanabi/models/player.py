import uuid

from sqlalchemy import VARCHAR, Integer
from sqlalchemy.dialects.postgresql import UUID

from hanabi import db


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
