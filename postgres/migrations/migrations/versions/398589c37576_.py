"""empty message

Revision ID: 398589c37576
Revises: 05df5e3a41f3
Create Date: 2019-08-30 16:41:18.575497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '398589c37576'
down_revision = '05df5e3a41f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('neurovault_file_upload',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nv_collection_id', sa.Integer(), nullable=False),
    sa.Column('path', sa.Text(), nullable=False),
    sa.Column('task_id', sa.Text(), nullable=True),
    sa.Column('level', sa.Text(), nullable=False),
    sa.Column('exception', sa.Text(), nullable=True),
    sa.Column('traceback', sa.Text(), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.CheckConstraint("level IN ('GROUP', 'SUBJECT')"),
    sa.CheckConstraint("status IN ('OK', 'FAILED', 'PENDING')"),
    sa.ForeignKeyConstraint(['nv_collection_id'], ['neurovault_collection.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'neurovault_collection', ['collection_id'])
    op.drop_column('neurovault_collection', 'status')
    op.drop_column('neurovault_collection', 'traceback')
    op.drop_column('neurovault_collection', 'task_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('neurovault_collection', sa.Column('task_id', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('neurovault_collection', sa.Column('traceback', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('neurovault_collection', sa.Column('status', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'neurovault_collection', type_='unique')
    op.drop_table('neurovault_file_upload')
    # ### end Alembic commands ###