"""empty message

Revision ID: c7098847c162
Revises: 319e666e4406
Create Date: 2019-06-02 15:09:15.795921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7098847c162'
down_revision = '319e666e4406'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brands',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.companies.id'], ),
    sa.PrimaryKeyConstraint('id', 'company_id'),
    schema='companies'
    )
    op.alter_column('companies', 'plan_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               schema='companies')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('companies', 'plan_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               schema='companies')
    op.drop_table('brands', schema='companies')
    # ### end Alembic commands ###
