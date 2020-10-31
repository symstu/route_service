"""user routes table

Revision ID: 67883f189e58
Revises: 
Create Date: 2020-10-31 15:50:06.109245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67883f189e58'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_routes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('route_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_routes')
    # ### end Alembic commands ###
