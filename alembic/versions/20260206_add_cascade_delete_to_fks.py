"""Add CASCADE delete to foreign keys

Revision ID: 20260206_cascade
Revises: 20260130dr01
Create Date: 2026-02-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260206_cascade'
down_revision: Union[str, None] = '20260130dr01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop existing foreign keys and recreate with CASCADE
    
    # depression_risk_results - user_id
    op.drop_constraint('depression_risk_results_user_id_fkey', 'depression_risk_results', type_='foreignkey')
    op.create_foreign_key(
        'depression_risk_results_user_id_fkey',
        'depression_risk_results', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )
    
    # depression_risk_results - depression_test_id
    op.drop_constraint('depression_risk_results_depression_test_id_fkey', 'depression_risk_results', type_='foreignkey')
    op.create_foreign_key(
        'depression_risk_results_depression_test_id_fkey',
        'depression_risk_results', 'depression_tests',
        ['depression_test_id'], ['depression_test_id'],
        ondelete='CASCADE'
    )
    
    # emergency_contacts - user_id
    op.drop_constraint('emergency_contacts_user_id_fkey', 'emergency_contacts', type_='foreignkey')
    op.create_foreign_key(
        'emergency_contacts_user_id_fkey',
        'emergency_contacts', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )
    
    # depression_tests - user_id
    op.drop_constraint('depression_tests_user_id_fkey', 'depression_tests', type_='foreignkey')
    op.create_foreign_key(
        'depression_tests_user_id_fkey',
        'depression_tests', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    # Revert to foreign keys without CASCADE
    
    # depression_risk_results - user_id
    op.drop_constraint('depression_risk_results_user_id_fkey', 'depression_risk_results', type_='foreignkey')
    op.create_foreign_key(
        'depression_risk_results_user_id_fkey',
        'depression_risk_results', 'users',
        ['user_id'], ['id']
    )
    
    # depression_risk_results - depression_test_id
    op.drop_constraint('depression_risk_results_depression_test_id_fkey', 'depression_risk_results', type_='foreignkey')
    op.create_foreign_key(
        'depression_risk_results_depression_test_id_fkey',
        'depression_risk_results', 'depression_tests',
        ['depression_test_id'], ['depression_test_id']
    )
    
    # emergency_contacts - user_id
    op.drop_constraint('emergency_contacts_user_id_fkey', 'emergency_contacts', type_='foreignkey')
    op.create_foreign_key(
        'emergency_contacts_user_id_fkey',
        'emergency_contacts', 'users',
        ['user_id'], ['id']
    )
    
    # depression_tests - user_id
    op.drop_constraint('depression_tests_user_id_fkey', 'depression_tests', type_='foreignkey')
    op.create_foreign_key(
        'depression_tests_user_id_fkey',
        'depression_tests', 'users',
        ['user_id'], ['id']
    )
