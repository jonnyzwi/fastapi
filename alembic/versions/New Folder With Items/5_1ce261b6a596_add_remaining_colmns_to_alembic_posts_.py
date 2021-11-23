"""
add remaining colmns to alembic_posts table 

Revision ID: 1ce261b6a596
Revises: f6fab6389dd9
Create Date: 2021-11-22 14:45:13.219593
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1ce261b6a596'
down_revision = 'f6fab6389dd9'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('alembic_posts', sa.Column('published' ,sa.Boolean()               , nullable=False, server_default='TRUE'), )
    op.add_column('alembic_posts', sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), ))

def downgrade():
    op.drop_column('alembic_posts', 'published')
    op.drop_column('alembic_posts', 'created_at')