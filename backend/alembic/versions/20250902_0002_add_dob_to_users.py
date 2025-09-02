"""
add dob to users

Revision ID: 20250902_0002
Revises: 20250902_0001
Create Date: 2025-09-02 00:02:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250902_0002'
down_revision = '20250902_0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('dob', sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'dob')

