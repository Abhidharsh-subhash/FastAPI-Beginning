"""add content to posts

Revision ID: 760d7efe2ebc
Revises: b1d9699b99a2
Create Date: 2024-02-19 18:54:43.110721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '760d7efe2ebc'
down_revision: Union[str, None] = 'b1d9699b99a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
