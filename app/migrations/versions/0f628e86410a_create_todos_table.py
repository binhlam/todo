"""create todos table

Revision ID: 0f628e86410a
Revises: 90480bd653ac
Create Date: 2024-05-27 22:56:30.645926

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0f628e86410a'
down_revision: Union[str, None] = '90480bd653ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'todos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('priority', sa.Integer, nullable=True),
        sa.Column('complete', sa.Integer, nullable=True),
        sa.Column('owner_id', sa.Integer, nullable=False)
    )

    # Create the foreign key constraint
    op.create_foreign_key(
        'fk_owner_id_to_users_id',
        'todos',
        'users',
        ['owner_id'],
        ['id']
    )

def downgrade() -> None:
    op.drop_constraint('fk_owner_id_to_users_id', 'todos', type_='foreignkey')
    op.drop_table('todos')
