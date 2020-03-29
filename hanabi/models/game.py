import uuid
from random import random

from sqlalchemy.dialects.postgresql import UUID

from hanabi import db
from .card import CARD_COUNT_MAP, Card, CardColor
from .lobby import Lobby


class Game(db.Model):

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
            "bomb-count": 3,
            "whose-turn": player_name,
            "cards-in-deck": 0,
        }
