"""empty message

Revision ID: 516f1b356dd4
Revises: 83cd15c6d432
Create Date: 2017-07-02 09:02:39.158235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '516f1b356dd4'
down_revision = '83cd15c6d432'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('for_menu', sa.Integer(), nullable=True),
    sa.Column('for_date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], [u'users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
