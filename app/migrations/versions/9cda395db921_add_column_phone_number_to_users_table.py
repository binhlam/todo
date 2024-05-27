"""add column phone_number to users table

Revision ID: 9cda395db921
Revises: 0f628e86410a
Create Date: 2024-05-27 22:57:38.779533

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9cda395db921'
down_revision: Union[str, None] = '0f628e86410a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',  # Table name
                  sa.Column('phone_number', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
