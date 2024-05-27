"""create users table

Revision ID: 90480bd653ac
Revises: 
Create Date: 2024-05-27 22:41:58.215982

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '90480bd653ac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('first_name', sa.String, nullable=False),
        sa.Column('last_name', sa.String, nullable=False),
        sa.Column('role', sa.String, nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True)
    )

def downgrade() -> None:
    op.drop_table('users')
