"""add homepage and contract fields


Revision ID: 5b9fd9ddfe43
Revises: a7c43f3fbc76
Create Date: 2023-12-11 00:46:36.971286

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = "5b9fd9ddfe43"
down_revision = "a7c43f3fbc76"
branch_labels = None
depends_on = None

CONTRACT_TYPES = [
    ("open-ended", "Open-ended"),
    ("fixed-term", "Fixed-term"),
    ("short-term", "Short-term"),
    ("freelance", "Freelance"),
    ("apprentice", "Apprentice"),
    ("internship", "Internship"),
]


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("person", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "contract_type",
                sqlalchemy_utils.types.choice.ChoiceType(CONTRACT_TYPES),
                nullable=True,
            )
        )

    with op.batch_alter_table("project", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("homepage", sa.String(length=80), nullable=True)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table("project", schema=None) as batch_op:
        batch_op.drop_column("homepage")

    with op.batch_alter_table("person", schema=None) as batch_op:
        batch_op.drop_column("contract_type")

    # ### end Alembic commands ###
