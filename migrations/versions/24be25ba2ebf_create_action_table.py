"""Create action table

Revision ID: 24be25ba2ebf
Revises: f77167d0a368
Create Date: 2020-03-29 00:44:08.806356

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "24be25ba2ebf"
down_revision = "f77167d0a368"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "action",
        sa.Column(
            "action_type",
            sa.Enum(
                "DISCARD",
                "DRAW",
                "HINT",
                "PLAY",
                "SET_HAND_ORDER",
                name="actiontype",
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("game_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("player_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["game_id"], ["game.id"],),
        sa.ForeignKeyConstraint(["player_id"], ["player.id"],),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "created_at", "game_id", name="uix_game_action_time"
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("action")
    # ### end Alembic commands ###
