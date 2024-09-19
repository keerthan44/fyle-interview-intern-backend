"""Initial migration.

Revision ID: ccd786798d2b
Revises: 52a401750a76
Create Date: 2024-09-19 13:31:06.740117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccd786798d2b'
down_revision = '52a401750a76'
branch_labels = None
depends_on = None


def upgrade():
    # Create a new table with the updated schema
    op.create_table(
        'assignments_new',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('student_id', sa.Integer, nullable=False),
        sa.Column('teacher_id', sa.Integer),
        sa.Column('content', sa.Text),
        sa.Column('grade', sa.String(length=1)),
        sa.Column('state', sa.String(length=9), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['students.id']),
        sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'])
    )

    # Copy data from the old table to the new table
    op.execute(
        """
        INSERT INTO assignments_new (id, student_id, teacher_id, content, grade, state, created_at, updated_at)
        SELECT id, student_id, teacher_id, content, grade, state, created_at, updated_at FROM assignments
        """
    )

    # Drop the old table
    op.drop_table('assignments')

    # Rename the new table to the original table name
    op.rename_table('assignments_new', 'assignments')


def downgrade():
    # Create a new table with the original schema
    op.create_table(
        'assignments_new',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('student_id', sa.Integer, nullable=False),
        sa.Column('teacher_id', sa.Integer),
        sa.Column('content', sa.Text),
        sa.Column('grade', sa.String(length=1)),
        sa.Column('state', sa.String(length=9), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['students.id']),
        sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'])
    )

    # Copy data from the old table to the new table
    op.execute(
        """
        INSERT INTO assignments_new (id, student_id, teacher_id, content, grade, state, created_at, updated_at)
        SELECT id, student_id, teacher_id, content, grade, state, created_at, updated_at FROM assignments
        """
    )

    # Drop the old table
    op.drop_table('assignments')

    # Rename the new table to the original table name
    op.rename_table('assignments_new', 'assignments')