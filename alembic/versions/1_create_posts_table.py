"""create posts table

Revision ID: 1
Revises: 
Create Date: 2021-11-23 02:15:53.181500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1'
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
