"""Initial schema - consolidated migration

Revision ID: 20260211_initial
Revises: 
Create Date: 2026-02-11

This migration creates all tables for the Lumora backend:
- users
- emergency_contacts
- mood_journaling
- depression_tests
- depression_risk_results
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '20260211_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ==================== USERS TABLE ====================
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_notify_enabled', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('is_risk_alert_enabled', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # ==================== EMERGENCY CONTACTS TABLE ====================
    op.create_table(
        'emergency_contacts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('contact_name', sa.String(length=255), nullable=True),
        sa.Column('contact_email', sa.String(length=255), nullable=True),
        sa.Column('relationship', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', name='uq_emergency_contacts_user_id')
    )

    # ==================== MOOD JOURNALING TABLE ====================
    op.create_table(
        'mood_journaling',
        sa.Column('mood_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('mood_type', sa.String(length=50), nullable=False),
        sa.Column('activities', postgresql.ARRAY(sa.String(length=100)), nullable=False),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('mood_id')
    )
    op.create_index('ix_mood_journaling_user_id', 'mood_journaling', ['user_id'])

    # ==================== DEPRESSION TESTS TABLE ====================
    op.create_table(
        'depression_tests',
        sa.Column('depression_test_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('mood', sa.String(), nullable=True),
        sa.Column('sleep_hour', sa.String(), nullable=True),
        sa.Column('appetite', sa.String(), nullable=True),
        sa.Column('exercise', sa.String(), nullable=True),
        sa.Column('screen_time', sa.String(), nullable=True),
        sa.Column('academic_work', sa.String(), nullable=True),
        sa.Column('socialize', sa.String(), nullable=True),
        sa.Column('energy_level', sa.Integer(), nullable=True),
        sa.Column('trouble_concentrating', sa.String(), nullable=True),
        sa.Column('negative_thoughts', sa.String(), nullable=True),
        sa.Column('decision_making', sa.String(), nullable=True),
        sa.Column('bothered_things', sa.String(), nullable=True),
        sa.Column('stressful_events', sa.String(), nullable=True),
        sa.Column('future_hope', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('depression_test_id')
    )
    op.create_index('ix_depression_tests_depression_test_id', 'depression_tests', ['depression_test_id'])
    op.create_index('ix_depression_tests_user_id', 'depression_tests', ['user_id'])

    # ==================== DEPRESSION RISK RESULTS TABLE ====================
    op.create_table(
        'depression_risk_results',
        sa.Column('result_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('depression_test_id', sa.Integer(), nullable=True),
        sa.Column('risk_level', sa.String(), nullable=False),
        sa.Column('risk_score', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['depression_test_id'], ['depression_tests.depression_test_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('result_id')
    )
    op.create_index('ix_depression_risk_results_result_id', 'depression_risk_results', ['result_id'])
    op.create_index('ix_depression_risk_results_user_id', 'depression_risk_results', ['user_id'])
    op.create_index('ix_depression_risk_results_depression_test_id', 'depression_risk_results', ['depression_test_id'])
    op.create_index('ix_depression_risk_results_created_at', 'depression_risk_results', ['created_at'])


def downgrade() -> None:
    # Drop tables in reverse order (respecting foreign key dependencies)
    op.drop_index('ix_depression_risk_results_created_at', table_name='depression_risk_results')
    op.drop_index('ix_depression_risk_results_depression_test_id', table_name='depression_risk_results')
    op.drop_index('ix_depression_risk_results_user_id', table_name='depression_risk_results')
    op.drop_index('ix_depression_risk_results_result_id', table_name='depression_risk_results')
    op.drop_table('depression_risk_results')

    op.drop_index('ix_depression_tests_user_id', table_name='depression_tests')
    op.drop_index('ix_depression_tests_depression_test_id', table_name='depression_tests')
    op.drop_table('depression_tests')

    op.drop_index('ix_mood_journaling_user_id', table_name='mood_journaling')
    op.drop_table('mood_journaling')

    op.drop_table('emergency_contacts')

    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
