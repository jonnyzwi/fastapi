"""auto-alembic_votes

Revision ID: 6
Revises: 5
Create Date: 2021-11-23 02:24:47.478373

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6'
down_revision = '5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'alembic_votes',
        sa.Column('voter_id', sa.Integer(), nullable=False),
        sa.Column('post_id' , sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id' ] , ['posts.id' ] , ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['voter_id'] , ['users.id'] , ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('voter_id', 'post_id')
    )

def downgrade():
   op.drop_table('alembic_votes')