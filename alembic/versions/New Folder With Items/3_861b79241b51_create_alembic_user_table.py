"""
create alembic_user table

Revision ID: 3_861b79241b51
Revises: 2_62b52c86a6bf
Create Date: 2021-11-22 14:16:22.782222

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = '3_861b79241b51'
down_revision = '2_62b52c86a6bf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'alembic_users', 
        sa.Column('id'   , sa.Integer(), nullable=False                  ),
        sa.Column('name' , sa.String(), nullable=False                  ),
        sa.Column('email', sa.String(), nullable=False                  ),
        sa.Column('password', sa.String(), nullable=False               ),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),

        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        )


def downgrade():
    op.drop_table('alembic_users')
