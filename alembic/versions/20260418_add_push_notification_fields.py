"""Add push notification fields to users

Revision ID: 20260418_push_fields
Revises: 20260220_add_notifications
Create Date: 2026-04-18
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260418_push_fields"
down_revision: Union[str, None] = "20260220_add_notifications"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_push_reminder_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.add_column("users", sa.Column("fcm_token", sa.String(length=512), nullable=True))
    op.add_column("users", sa.Column("last_push_reminder_date", sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "last_push_reminder_date")
    op.drop_column("users", "fcm_token")
    op.drop_column("users", "is_push_reminder_enabled")
