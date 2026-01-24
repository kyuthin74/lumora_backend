"""add emergency contacts and link to users

Revision ID: 20260124ec01
Revises: 20260115a1b2
Create Date: 2026-01-24 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260124ec01"
down_revision: Union[str, Sequence[str], None] = "20260115a1b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to introduce emergency contacts table."""
    op.create_table(
        "emergency_contacts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("contact_name", sa.String(length=255), nullable=True),
        sa.Column("contact_email", sa.String(length=255), nullable=True),
        sa.Column("relationship", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.UniqueConstraint("user_id", name="uq_emergency_contacts_user_id"),
    )

    # Cast time -> timestamptz via explicit construction to avoid coercion errors
    op.execute(
        sa.text(
            """
            ALTER TABLE users
            ALTER COLUMN daily_reminder_time
            TYPE TIMESTAMP WITH TIME ZONE
            USING
              CASE
                WHEN daily_reminder_time IS NULL THEN NULL
                ELSE (DATE '1970-01-01' + daily_reminder_time)::timestamptz
              END
            """
        )
    )

    bind = op.get_bind()

    emergency_contacts = sa.table(
        "emergency_contacts",
        sa.column("id", sa.Integer()),
        sa.column("user_id", sa.Integer()),
        sa.column("contact_name", sa.String()),
        sa.column("contact_email", sa.String()),
        sa.column("relationship", sa.String()),
    )

    users_table = sa.table(
        "users",
        sa.column("id", sa.Integer()),
        sa.column("emergency_contact_name", sa.String()),
        sa.column("emergency_contact_relationship", sa.String()),
        sa.column("emergency_contact_email", sa.String()),
    )

    user_rows = bind.execute(
        sa.select(
            users_table.c.id,
            users_table.c.emergency_contact_name,
            users_table.c.emergency_contact_relationship,
            users_table.c.emergency_contact_email,
        )
    ).mappings().all()

    for row in user_rows:
        if row["emergency_contact_name"] or row["emergency_contact_relationship"] or row["emergency_contact_email"]:
            bind.execute(
                sa.text(
                    """
                    INSERT INTO emergency_contacts (user_id, contact_name, contact_email, relationship)
                    VALUES (:user_id, :contact_name, :contact_email, :relationship)
                    """
                ),
                {
                    "user_id": row["id"],
                    "contact_name": row["emergency_contact_name"],
                    "contact_email": row["emergency_contact_email"],
                    "relationship": row["emergency_contact_relationship"],
                },
            )

    op.drop_column("users", "emergency_contact_name")
    op.drop_column("users", "emergency_contact_relationship")
    op.drop_column("users", "emergency_contact_email")


def downgrade() -> None:
    """Revert emergency contacts schema changes."""
    op.add_column(
        "users",
        sa.Column("emergency_contact_email", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("emergency_contact_relationship", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("emergency_contact_name", sa.String(length=255), nullable=True),
    )

    bind = op.get_bind()

    emergency_contacts = sa.table(
        "emergency_contacts",
        sa.column("id", sa.Integer()),
        sa.column("user_id", sa.Integer()),
        sa.column("contact_name", sa.String()),
        sa.column("contact_email", sa.String()),
        sa.column("relationship", sa.String()),
    )

    user_rows = bind.execute(
        sa.select(
            emergency_contacts.c.user_id,
            emergency_contacts.c.contact_name,
            emergency_contacts.c.contact_email,
            emergency_contacts.c.relationship,
        )
    ).mappings().all()

    for row in user_rows:
        bind.execute(
            sa.text(
                """
                UPDATE users
                   SET emergency_contact_name = :contact_name,
                       emergency_contact_email = :contact_email,
                       emergency_contact_relationship = :relationship
                 WHERE id = :user_id
                """
            ),
            {
                "contact_name": row["contact_name"],
                "contact_email": row["contact_email"],
                "relationship": row["relationship"],
                "user_id": row["user_id"],
            },
        )

    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "daily_reminder_time",
            existing_type=sa.DateTime(timezone=True),
            type_=sa.Time(),
            existing_nullable=True,
        )

    op.drop_table("emergency_contacts")
