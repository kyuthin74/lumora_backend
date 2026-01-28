"""create mood journaling table

Revision ID: 20260128mj01
Revises: 20260124ec02
Create Date: 2026-01-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "20260128mj01"
down_revision: Union[str, Sequence[str], None] = "20260124ec02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the mood_journaling table."""
    op.create_table(
        "mood_journaling",
        sa.Column("mood_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("mood_type", sa.String(length=50), nullable=False),
        sa.Column("activities", postgresql.ARRAY(sa.String(length=100)), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("mood_id"),
    )
    op.create_index("ix_mood_journaling_user_id", "mood_journaling", ["user_id"])


def downgrade() -> None:
    """Drop the mood_journaling table."""
    op.drop_index("ix_mood_journaling_user_id", table_name="mood_journaling")
    op.drop_table("mood_journaling")
