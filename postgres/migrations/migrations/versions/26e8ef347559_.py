"""empty message

Revision ID: 26e8ef347559
Revises: 411caa1af7db
Create Date: 2018-10-16 21:50:59.804037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26e8ef347559'
down_revision = '411caa1af7db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('picture', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'picture')
    # ### end Alembic commands ###
