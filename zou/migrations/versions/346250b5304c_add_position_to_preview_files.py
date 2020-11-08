"""add position to preview files

Revision ID: 346250b5304c
Revises: 82e7f7a95e84
Create Date: 2020-10-26 18:34:47.936827

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '346250b5304c'
down_revision = '82e7f7a95e84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('preview_file', sa.Column('position', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('preview_file', 'position')
    # ### end Alembic commands ###
