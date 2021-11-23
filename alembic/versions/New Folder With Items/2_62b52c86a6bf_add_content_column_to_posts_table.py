"""
add 'content' column to alembic_posts table

Revision ID: 2_62b52c86a6bf
Revises: 1_ec9299c66024
Create Date: 2021-11-22 14:10:38.530169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2_62b52c86a6bf'
down_revision = '1_ec9299c66024'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('alembic_posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('alembic_posts', 'content')
