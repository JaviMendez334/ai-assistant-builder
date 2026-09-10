"""crear tabla asistentes

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-07-24
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d4e5f6a7b8c9"
down_revision: Union[str, Sequence[str], None] = "c3d4e5f6a7b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assistants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("instrucciones", sa.Text(), nullable=False),
        sa.Column(
            "modelo",
            sa.String(length=100),
            server_default="gpt-4.1-mini",
            nullable=False,
        ),
        sa.Column("activo", sa.Integer(), server_default="1", nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_assistants_id", "assistants", ["id"], unique=False)
    op.create_index("ix_assistants_project_id", "assistants", ["project_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_assistants_project_id", table_name="assistants")
    op.drop_index("ix_assistants_id", table_name="assistants")
    op.drop_table("assistants")
