"""empty message

Revision ID: 366d0a29e904
Revises: bc4e75e4e7ac
Create Date: 2019-02-04 10:58:03.540874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '366d0a29e904'
down_revision = 'bc4e75e4e7ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prijava',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('izlet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['izlet_id'], ['izlet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prijava')
    # ### end Alembic commands ###
