"""Merge chat history and push fields heads

Revision ID: 20260424_merge_heads
Revises: 20260418_push_fields, c44bdeec5875
Create Date: 2026-04-24
"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "20260424_merge_heads"
down_revision: Union[str, Sequence[str], None] = ("20260418_push_fields", "c44bdeec5875")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Merge heads - no schema changes."""
    pass


def downgrade() -> None:
    """Unmerge heads - no schema changes."""
    pass
