"""
add Foreign Key to alembic_posts table

Revision ID: f6fab6389dd9
Revises: 3_861b79241b51
Create Date: 2021-11-22 14:25:23.118680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6fab6389dd9'
down_revision = '3_861b79241b51'
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
