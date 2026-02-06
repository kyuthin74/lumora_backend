"""Replace PHQ labels with mood and future_hope columns

Revision ID: 20260206_update_dt_cols
Revises: 20260206_cascade
Create Date: 2026-02-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260206_update_dt_cols'
down_revision: Union[str, None] = '20260206_cascade'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop PHQ columns
    op.drop_column('depression_tests', 'PHQ_label_one')
    op.drop_column('depression_tests', 'PHQ_label_two')
    
    # Add new columns
    op.add_column('depression_tests', sa.Column('mood', sa.String(), nullable=True))
    op.add_column('depression_tests', sa.Column('future_hope', sa.String(), nullable=True))
    
    # Change screen_time and socialize from Boolean to String
    op.alter_column('depression_tests', 'screen_time',
                    existing_type=sa.Boolean(),
                    type_=sa.String(),
                    existing_nullable=True,
                    postgresql_using='screen_time::text')
    op.alter_column('depression_tests', 'socialize',
                    existing_type=sa.Boolean(),
                    type_=sa.String(),
                    existing_nullable=True,
                    postgresql_using='socialize::text')


def downgrade() -> None:
    # Change screen_time and socialize back to Boolean
    op.alter_column('depression_tests', 'screen_time',
                    existing_type=sa.String(),
                    type_=sa.Boolean(),
                    existing_nullable=True,
                    postgresql_using='screen_time::boolean')
    op.alter_column('depression_tests', 'socialize',
                    existing_type=sa.String(),
                    type_=sa.Boolean(),
                    existing_nullable=True,
                    postgresql_using='socialize::boolean')
    
    # Drop new columns
    op.drop_column('depression_tests', 'mood')
    op.drop_column('depression_tests', 'future_hope')
    
    # Add PHQ columns back
    op.add_column('depression_tests', sa.Column('PHQ_label_one', sa.String(), nullable=True))
    op.add_column('depression_tests', sa.Column('PHQ_label_two', sa.String(), nullable=True))
