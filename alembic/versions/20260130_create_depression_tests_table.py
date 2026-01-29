"""create depression tests table

Revision ID: 20260130dt01
Revises: 20260128mj01
Create Date: 2026-01-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260130dt01"
down_revision: Union[str, Sequence[str], None] = "20260128mj01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the depression_tests table."""
    op.create_table(
        "depression_tests",
        sa.Column("depression_test_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("sleep_hour", sa.String(), nullable=True),
        sa.Column("appetite", sa.String(), nullable=True),
        sa.Column("exercise", sa.String(), nullable=True),
        sa.Column("screen_time", sa.Boolean(), nullable=True),
        sa.Column("academic_work", sa.String(), nullable=True),
        sa.Column("socialize", sa.Boolean(), nullable=True),
        sa.Column("energy_level", sa.Integer(), nullable=True),
        sa.Column("trouble_concentrating", sa.String(), nullable=True),
        sa.Column("negative_thoughts", sa.String(), nullable=True),
        sa.Column("decision_making", sa.String(), nullable=True),
        sa.Column("bothered_things", sa.String(), nullable=True),
        sa.Column("stressful_events", sa.String(), nullable=True),
        sa.Column("PHQ_label_one", sa.String(), nullable=True),
        sa.Column("PHQ_label_two", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("depression_test_id"),
    )
    op.create_index("ix_depression_tests_depression_test_id", "depression_tests", ["depression_test_id"])
    op.create_index("ix_depression_tests_user_id", "depression_tests", ["user_id"])


def downgrade() -> None:
    """Drop the depression_tests table."""
    op.drop_index("ix_depression_tests_user_id", table_name="depression_tests")
    op.drop_index("ix_depression_tests_depression_test_id", table_name="depression_tests")
    op.drop_table("depression_tests")
