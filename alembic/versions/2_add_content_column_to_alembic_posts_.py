"""add CONTENT  column to alembic_posts table

Revision ID: 2
Revises: 1
Create Date: 2021-11-23 02:17:11.479055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2'
down_revision = '1'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('alembic_posts', sa.Column('content', sa.String(), nullable=False))

def downgrade():
    op.drop_column('alembic_posts', 'content')