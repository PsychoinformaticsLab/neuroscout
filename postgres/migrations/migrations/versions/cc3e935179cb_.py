"""empty message

Revision ID: cc3e935179cb
Revises: ad787307f461
Create Date: 2019-07-04 21:20:47.633341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc3e935179cb'
down_revision = 'ad787307f461'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('predictor_collection',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('uploaded_at', sa.DateTime(), nullable=True),
    sa.Column('collection_name', sa.Text(), nullable=False),
    sa.Column('task_id', sa.Text(), nullable=True),
    sa.Column('traceback', sa.Text(), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.CheckConstraint("status IN ('OK', 'FAILED', 'PENDING')"),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collection_predictor',
    sa.Column('pc_id', sa.Integer(), nullable=True),
    sa.Column('predictor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pc_id'], ['predictor_collection.id'], ),
    sa.ForeignKeyConstraint(['predictor_id'], ['predictor.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('collection_predictor')
    op.drop_table('predictor_collection')
    # ### end Alembic commands ###