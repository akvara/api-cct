"""empty message

Revision ID: 83cd15c6d432
Revises: 71cc59b5051f
Create Date: 2017-07-01 22:12:00.878126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83cd15c6d432'
down_revision = '71cc59b5051f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menus', sa.Column('restaurant_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'menus_restaurant_fkey', 'menus', type_='foreignkey')
    op.create_foreign_key(None, 'menus', 'restaurants', ['restaurant_id'], ['id'])
    op.drop_column('menus', 'restaurant')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menus', sa.Column('restaurant', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'menus', type_='foreignkey')
    op.create_foreign_key(u'menus_restaurant_fkey', 'menus', 'restaurants', ['restaurant'], ['id'])
    op.drop_column('menus', 'restaurant_id')
    # ### end Alembic commands ###