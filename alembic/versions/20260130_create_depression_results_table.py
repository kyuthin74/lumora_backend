"""create depression results table

Revision ID: 20260130dr01
Revises: 20260130dt01
Create Date: 2026-01-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260130dr01"
down_revision: Union[str, Sequence[str], None] = "20260130dt01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the depression_results table."""
    op.create_table(
        "depression_results",
        sa.Column("result_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("depression_test_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("severity", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["depression_test_id"], ["depression_tests.depression_test_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("result_id"),
    )
    op.create_index("ix_depression_results_result_id", "depression_results", ["result_id"])
    op.create_index("ix_depression_results_user_id", "depression_results", ["user_id"])
    op.create_index("ix_depression_results_depression_test_id", "depression_results", ["depression_test_id"])


def downgrade() -> None:
    """Drop the depression_results table."""
    op.drop_index("ix_depression_results_depression_test_id", table_name="depression_results")
    op.drop_index("ix_depression_results_user_id", table_name="depression_results")
    op.drop_index("ix_depression_results_result_id", table_name="depression_results")
    op.drop_table("depression_results")
