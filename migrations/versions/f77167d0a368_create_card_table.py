"""Create card table

Revision ID: f77167d0a368
Revises: fbe03d87119c
Create Date: 2020-03-28 22:23:57.889471

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f77167d0a368"
down_revision = "fbe03d87119c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic ###
    op.create_table(
        "card",
        sa.Column(
            "color",
            sa.Enum(
                "BLUE", "GREEN", "RED", "WHITE", "YELLOW", name="cardcolor"
            ),
            nullable=False,
        ),
        sa.Column("deck_order", sa.SmallInteger(), nullable=False),
        sa.Column("game_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("number", sa.SmallInteger(), nullable=False),
        sa.ForeignKeyConstraint(["game_id"], ["game.id"],),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "deck_order", "game_id", name="uix_game_card_order"
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic ###
    op.drop_table("card")
    # ### end Alembic commands ###
