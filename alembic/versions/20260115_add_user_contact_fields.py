"""update users table with emergency contact and notification settings

Revision ID: 20260115a1b2
Revises: c0f30aa8f467
Create Date: 2026-01-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260115a1b2"
down_revision: Union[str, Sequence[str], None] = "c0f30aa8f467"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply schema changes."""
    op.add_column("users", sa.Column("emergency_contact_name", sa.String(length=255), nullable=True))
    op.add_column("users", sa.Column("emergency_contact_relationship", sa.String(length=255), nullable=True))
    op.add_column("users", sa.Column("emergency_contact_email", sa.String(length=255), nullable=True))
    op.add_column(
        "users",
        sa.Column(
            "is_notify_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column("users", sa.Column("daily_reminder_time", sa.Time(), nullable=True))
    op.add_column(
        "users",
        sa.Column(
            "is_risk_alert_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.drop_column("users", "is_active")
    op.drop_column("users", "updated_at")


def downgrade() -> None:
    """Revert schema changes."""
    op.add_column("users", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=True))
    op.drop_column("users", "is_risk_alert_enabled")
    op.drop_column("users", "daily_reminder_time")
    op.drop_column("users", "is_notify_enabled")
    op.drop_column("users", "emergency_contact_email")
    op.drop_column("users", "emergency_contact_relationship")
    op.drop_column("users", "emergency_contact_name")
