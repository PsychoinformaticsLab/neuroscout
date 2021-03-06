"""empty message

Revision ID: 1328ab9aae1e
Revises: 0a774092a8ae
Create Date: 2020-12-18 01:39:04.927554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1328ab9aae1e'
down_revision = '0a774092a8ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('neurovault_collection', sa.Column('estimator', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('neurovault_collection', 'estimator')
    # ### end Alembic commands ###
