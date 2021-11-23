"""add remaining colmns to alembic_posts table

Revision ID: 5
Revises: 4
Create Date: 2021-11-23 02:18:23.864564

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5'
down_revision = '4'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('alembic_posts', sa.Column('published' ,sa.Boolean()               , nullable=False, server_default='TRUE'), )
    op.add_column('alembic_posts', sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), ))

def downgrade():
    op.drop_column('alembic_posts', 'published')
    op.drop_column('alembic_posts', 'created_at')