"""create menu_items table

Revision ID: 0001
Revises:
Create Date: 2026-02-13
"""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "menu_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("price_cents", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("menu_items")
