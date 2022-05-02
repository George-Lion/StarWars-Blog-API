"""empty message

Revision ID: bb50bb20d556
Revises: f84a1b44369d
Create Date: 2022-05-02 11:25:12.289990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb50bb20d556'
down_revision = 'f84a1b44369d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('characters', sa.Column('favorites_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'characters', 'favorites', ['favorites_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'characters', type_='foreignkey')
    op.drop_column('characters', 'favorites_id')
    # ### end Alembic commands ###
