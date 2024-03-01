"""Add some indexes

Revision ID: 16df47d76c64
Revises: 0596674df51d
Create Date: 2023-07-24 22:44:26.233788

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "16df47d76c64"
down_revision = "0596674df51d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("comment", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_comment_person_id"), ["person_id"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_comment_task_status_id"),
            ["task_status_id"],
            unique=False,
        )

    with op.batch_alter_table("department_link", schema=None) as batch_op:
        batch_op.alter_column(
            "person_id", existing_type=sa.UUID(), nullable=False
        )
        batch_op.alter_column(
            "department_id", existing_type=sa.UUID(), nullable=False
        )

    with op.batch_alter_table("output_file", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_output_file_entity_id"), ["entity_id"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_output_file_file_status_id"),
            ["file_status_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_output_file_person_id"), ["person_id"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_output_file_source_file_id"),
            ["source_file_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_output_file_temporal_entity_id"),
            ["temporal_entity_id"],
            unique=False,
        )

    with op.batch_alter_table("search_filter", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_search_filter_person_id"),
            ["person_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_search_filter_project_id"),
            ["project_id"],
            unique=False,
        )

    with op.batch_alter_table("task_type", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_task_type_department_id"),
            ["department_id"],
            unique=False,
        )

    with op.batch_alter_table("working_file", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_working_file_person_id"),
            ["person_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_working_file_software_id"),
            ["software_id"],
            unique=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("working_file", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_working_file_software_id"))
        batch_op.drop_index(batch_op.f("ix_working_file_person_id"))

    with op.batch_alter_table("task_type", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_task_type_department_id"))

    with op.batch_alter_table("search_filter", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_search_filter_project_id"))
        batch_op.drop_index(batch_op.f("ix_search_filter_person_id"))

    with op.batch_alter_table("output_file", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_output_file_temporal_entity_id"))
        batch_op.drop_index(batch_op.f("ix_output_file_source_file_id"))
        batch_op.drop_index(batch_op.f("ix_output_file_person_id"))
        batch_op.drop_index(batch_op.f("ix_output_file_file_status_id"))
        batch_op.drop_index(batch_op.f("ix_output_file_entity_id"))

    with op.batch_alter_table("department_link", schema=None) as batch_op:
        batch_op.alter_column(
            "department_id", existing_type=sa.UUID(), nullable=True
        )
        batch_op.alter_column(
            "person_id", existing_type=sa.UUID(), nullable=True
        )

    with op.batch_alter_table("comment", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_comment_task_status_id"))
        batch_op.drop_index(batch_op.f("ix_comment_person_id"))

    # ### end Alembic commands ###
