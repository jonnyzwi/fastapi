"""
create posts table

Revision ID: ec9299c66024
Revises: 
Create Date: 2021-11-22 14:00:30.233313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1_ec9299c66024'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'alembic_posts', 
        sa.Column('id'   , sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String() , nullable=False)
        ) 
    


def downgrade():
    op.drop_table('alembic_posts')
