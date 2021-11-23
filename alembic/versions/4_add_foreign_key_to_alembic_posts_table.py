"""add Foreign Key to alembic_posts table

Revision ID: 4
Revises: 3
Create Date: 2021-11-23 02:17:55.104443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4'
down_revision = '3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('alembic_posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'alembic_posts_FK', source_table='alembic_posts', referent_table='alembic_users', 
        local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

def downgrade():
    op.drop_constraint('alembic_posts_FK', table_name='alembic_posts')
    op.drop_column('alembic_posts', 'owner_id')