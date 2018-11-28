"""empty message

Revision ID: 61fa7d5009cb
Revises: fe95bd505740
Create Date: 2018-11-28 19:42:29.156161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61fa7d5009cb'
down_revision = 'fe95bd505740'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('created', sa.DateTime(), nullable=False), schema='companies')
    op.add_column('companies', sa.Column('created_by', sa.Integer(), nullable=False), schema='companies')
    op.add_column('companies', sa.Column('updated', sa.DateTime(), nullable=True), schema='companies')
    op.add_column('companies', sa.Column('updated_by', sa.Integer(), nullable=True), schema='companies')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('companies', 'updated_by', schema='companies')
    op.drop_column('companies', 'updated', schema='companies')
    op.drop_column('companies', 'created_by', schema='companies')
    op.drop_column('companies', 'created', schema='companies')
    # ### end Alembic commands ###
