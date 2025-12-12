"""add webhook events table

Revision ID: 4d9fa49d2a36
Revises: 
Create Date: 2025-12-11 13:22:18.078349

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4d9fa49d2a36'
down_revision = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "webhook_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("processed", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index(
        "ix_webhook_events_processed",
        "webhook_events",
        ["processed"],
    )
    op.create_index(
        "ix_webhook_events_created_at",
        "webhook_events",
        ["created_at"],
    )


def downgrade() -> None:
    op.drop_table("webhook_events")
