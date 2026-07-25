"""agregar rol a usuarios

Revision ID: a1b2c3d4e5f6
Revises: f07855239967
Create Date: 2026-07-24
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "f07855239967"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("role", sa.String(), server_default="user", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("users", "role")
