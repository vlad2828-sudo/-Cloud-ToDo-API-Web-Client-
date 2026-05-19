"""create tasks table

Revision ID: 202604260001
Revises:
Create Date: 2026-04-26 00:01:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202604260001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

status_enum = sa.Enum("NEW", "IN_PROGRESS", "DONE", name="task_status", native_enum=False)
priority_enum = sa.Enum("LOW", "MEDIUM", "HIGH", name="task_priority", native_enum=False)


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("status", status_enum, nullable=False, server_default="NEW"),
        sa.Column("priority", priority_enum, nullable=False, server_default="MEDIUM"),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_tasks_status", "tasks", ["status"])
    op.create_index("idx_tasks_priority", "tasks", ["priority"])
    op.create_index("idx_tasks_status_priority", "tasks", ["status", "priority"])


def downgrade() -> None:
    op.drop_index("idx_tasks_status_priority", table_name="tasks")
    op.drop_index("idx_tasks_priority", table_name="tasks")
    op.drop_index("idx_tasks_status", table_name="tasks")
    op.drop_table("tasks")
