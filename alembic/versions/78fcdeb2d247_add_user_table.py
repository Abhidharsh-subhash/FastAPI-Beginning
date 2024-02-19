"""add user table

Revision ID: 78fcdeb2d247
Revises: 760d7efe2ebc
Create Date: 2024-02-19 21:30:29.718225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78fcdeb2d247'
down_revision: Union[str, None] = '760d7efe2ebc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer,
                              primary_key=True, nullable=False),
                    sa.Column('email', sa.String, unique=True, nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
