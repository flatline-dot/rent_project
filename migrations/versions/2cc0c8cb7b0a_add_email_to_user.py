"""add email to user

Revision ID: 2cc0c8cb7b0a
Revises: 9a2a9313a1ac
Create Date: 2021-09-12 18:17:45.919794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cc0c8cb7b0a'
down_revision = '9a2a9313a1ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'email')
    # ### end Alembic commands ###
