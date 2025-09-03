"""
add dob to users

Revision ID: 003
Revises: 002
Create Date: 2025-09-02 00:02:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('dob', sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'dob')

