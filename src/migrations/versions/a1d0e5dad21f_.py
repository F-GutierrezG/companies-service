"""empty message

Revision ID: a1d0e5dad21f
Revises: 61fa7d5009cb
Create Date: 2018-12-31 21:42:24.022928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1d0e5dad21f'
down_revision = '61fa7d5009cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classification',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='companies'
    )
    op.add_column('companies', sa.Column('classification_id', sa.Integer(), nullable=False), schema='companies')
    op.add_column('companies', sa.Column('expiration', sa.DateTime(), nullable=True), schema='companies')
    op.create_foreign_key(None, 'companies', 'classification', ['classification_id'], ['id'], source_schema='companies', referent_schema='companies')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'companies', schema='companies', type_='foreignkey')
    op.drop_column('companies', 'expiration', schema='companies')
    op.drop_column('companies', 'classification_id', schema='companies')
    op.drop_table('classification', schema='companies')
    # ### end Alembic commands ###