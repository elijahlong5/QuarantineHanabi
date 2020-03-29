"""Create draw action table

Revision ID: fd45a3ed0be0
Revises: 6d3955140753
Create Date: 2020-03-29 10:27:12.312572

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "fd45a3ed0be0"
down_revision = "6d3955140753"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic ###
    op.create_table(
        "draw_action",
        sa.Column("action_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("card_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["action_id"], ["action.id"],),
        sa.ForeignKeyConstraint(["card_id"], ["card.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic ###
    op.drop_table("draw_action")
    # ### end Alembic commands ###
