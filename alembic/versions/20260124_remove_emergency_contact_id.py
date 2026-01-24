"""remove emergency_contact_id from users table

Revision ID: 20260124ec02
Revises: 20260124ec01
Create Date: 2026-01-24 10:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260124ec02"
down_revision: Union[str, Sequence[str], None] = "20260124ec01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove FK constraint from users.emergency_contact_id if it exists."""
    bind = op.get_bind()
    
    # Check if constraint exists before dropping
    result = bind.execute(
        sa.text(
            """
            SELECT 1 FROM information_schema.table_constraints 
            WHERE constraint_name = 'fk_users_emergency_contact' 
            AND table_name = 'users'
            """
        )
    ).fetchone()
    
    if result:
        op.drop_constraint("fk_users_emergency_contact", "users", type_="foreignkey")


def downgrade() -> None:
    """Re-add FK constraint to users.emergency_contact_id."""
    # Only create if column exists
    bind = op.get_bind()
    result = bind.execute(
        sa.text(
            """
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'emergency_contact_id'
            """
        )
    ).fetchone()
    
    if result:
        op.create_foreign_key(
            "fk_users_emergency_contact",
            source_table="users",
            referent_table="emergency_contacts",
            local_cols=["emergency_contact_id"],
            remote_cols=["id"],
        )
