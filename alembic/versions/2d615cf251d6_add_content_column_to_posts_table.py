"""add content column to posts table

Revision ID: 2d615cf251d6
Revises: 12e73c935133
Create Date: 2023-12-31 17:21:13.765946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d615cf251d6'
down_revision: Union[str, None] = '12e73c935133'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
