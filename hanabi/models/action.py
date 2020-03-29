import enum

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

from hanabi import db


class ActionType(enum.Enum):
    DISCARD = 1
    PLAY = 2


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
