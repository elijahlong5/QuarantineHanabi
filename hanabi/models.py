from sqlalchemy import VARCHAR
from sqlalchemy.dialects.postgresql import UUID

from hanabi import db


class Lobby(db.Model):
    id = db.Column(UUID(), primary_key=True)
    code = db.Column(VARCHAR(5), nullable=False, unique=True)
