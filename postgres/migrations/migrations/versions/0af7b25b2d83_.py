"""empty message

Revision ID: 0af7b25b2d83
Revises: fa02cc560c61
Create Date: 2020-06-03 22:31:41.647391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0af7b25b2d83'
down_revision = 'fa02cc560c61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('stim_run', 'run_stimulus', ['stimulus_id', 'run_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('stim_run', table_name='run_stimulus')
    # ### end Alembic commands ###
