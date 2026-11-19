# SPDX-License-Identifier: Apache-2.0
"""Add evidence_records and evidence_requests tables.

Revision ID: 20261119_000001
Revises: 20261119_000000
Create Date: 2026-11-19 00:00:00.000000

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20261119_000001"
down_revision = "20261119_000000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # evidence_records table
    op.create_table(
        "evidence_records",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organisation_id", sa.Uuid(), nullable=False),
        sa.Column("source_plugin", sa.String(128), nullable=False),
        sa.Column("plugin_version", sa.String(32), nullable=False),
        sa.Column("collector", sa.String(32), nullable=False),
        sa.Column("check", sa.String(128), nullable=False),
        sa.Column("subject", sa.String(512), nullable=False),
        sa.Column("result", sa.String(32), nullable=False),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("data", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("hash", sa.String(128), nullable=False),
        sa.Column("prev_hash", sa.String(128), nullable=True),
        sa.Column("linked_controls", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_evidence_records_organisation_id", "evidence_records", ["organisation_id"])
    op.create_index("ix_evidence_records_check", "evidence_records", ["check"])
    op.create_index("ix_evidence_records_result", "evidence_records", ["result"])
    op.create_index("ix_evidence_records_collected_at", "evidence_records", ["collected_at"])
    op.create_index("ix_evidence_records_valid_until", "evidence_records", ["valid_until"])
    op.create_index("ix_evidence_records_hash", "evidence_records", ["hash"])

    # RLS policy for evidence_records
    op.execute("ALTER TABLE evidence_records ENABLE ROW LEVEL SECURITY;")
    op.execute("""
        CREATE POLICY evidence_records_tenant_isolation ON evidence_records
        USING (organisation_id = current_organisation_id())
        WITH CHECK (organisation_id = current_organisation_id());
    """)

    # evidence_requests table
    op.create_table(
        "evidence_requests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organisation_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("requested_by_id", sa.Uuid(), nullable=False),
        sa.Column("assignee_id", sa.Uuid(), nullable=False),
        sa.Column("control_implementation_id", sa.Uuid(), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("priority", sa.String(32), nullable=False, server_default="medium"),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("evidence_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["requested_by_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["assignee_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["control_implementation_id"], ["control_implementations.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["evidence_id"], ["evidence_records.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_evidence_requests_organisation_id", "evidence_requests", ["organisation_id"])
    op.create_index("ix_evidence_requests_assignee_id", "evidence_requests", ["assignee_id"])
    op.create_index("ix_evidence_requests_requested_by_id", "evidence_requests", ["requested_by_id"])
    op.create_index("ix_evidence_requests_status", "evidence_requests", ["status"])
    op.create_index("ix_evidence_requests_due_date", "evidence_requests", ["due_date"])
    op.create_index("ix_evidence_requests_control_implementation_id", "evidence_requests", ["control_implementation_id"])
    op.create_index("ix_evidence_requests_evidence_id", "evidence_requests", ["evidence_id"])

    # RLS policy for evidence_requests
    op.execute("ALTER TABLE evidence_requests ENABLE ROW LEVEL SECURITY;")
    op.execute("""
        CREATE POLICY evidence_requests_tenant_isolation ON evidence_requests
        USING (organisation_id = current_organisation_id())
        WITH CHECK (organisation_id = current_organisation_id());
    """)


def downgrade() -> None:
    op.drop_table("evidence_requests")
    op.drop_table("evidence_records")
