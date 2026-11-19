# SPDX-License-Identifier: Apache-2.0
"""Initial schema with RLS policies.

Revision ID: 20261119_000000
Revises: 
Create Date: 2026-11-19 00:00:00.000000

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20261119_000000"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable UUID extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    # Create organisations table
    op.create_table(
        "organisations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(64), nullable=False),
        sa.Column("region", sa.String(2), nullable=False, server_default="IN"),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column("settings", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug", name="uq_organisations_slug"),
    )
    op.create_index("ix_organisations_slug", "organisations", ["slug"], unique=True)

    # Create entities table
    op.create_table(
        "entities",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organisation_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("type", sa.String(32), nullable=False, server_default="legal_entity"),
        sa.Column("parent_entity_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_entity_id"], ["entities.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organisation_id", "name", name="uq_entity_org_name"),
    )
    op.create_index("ix_entities_organisation_id", "entities", ["organisation_id"])

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("avatar_url", sa.String(512), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # Create memberships table
    op.create_table(
        "memberships",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("organisation_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "organisation_id", name="uq_membership_user_org"),
    )
    op.create_index("ix_memberships_user_id", "memberships", ["user_id"])
    op.create_index("ix_memberships_organisation_id", "memberships", ["organisation_id"])

    # Create roles table
    op.create_table(
        "roles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organisation_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("description", sa.String(512), nullable=True),
        sa.Column("permissions", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("is_system", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organisation_id", "name", name="uq_role_org_name"),
    )

    # Create sessions table
    op.create_table(
        "sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("organisation_id", sa.Uuid(), nullable=False),
        sa.Column("session_token_hash", sa.String(128), nullable=False),
        sa.Column("mfa_verified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("mfa_method", sa.String(32), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"])
    op.create_index("ix_sessions_organisation_id", "sessions", ["organisation_id"])
    op.create_index("ix_sessions_token_hash", "sessions", ["session_token_hash"])
    op.create_index("ix_sessions_expires_at", "sessions", ["expires_at"])

    # Create api_tokens table
    op.create_table(
        "api_tokens",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organisation_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("token_hash", sa.String(128), nullable=False),
        sa.Column("scopes", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_api_tokens_organisation_id", "api_tokens", ["organisation_id"])
    op.create_index("ix_api_tokens_token_hash", "api_tokens", ["token_hash"])

    # Create audit_logs table
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organisation_id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=True),
        sa.Column("action", sa.String(64), nullable=False),
        sa.Column("resource_type", sa.String(64), nullable=False),
        sa.Column("resource_id", sa.Uuid(), nullable=True),
        sa.Column("before", sa.JSON(), nullable=True),
        sa.Column("after", sa.JSON(), nullable=True),
        sa.Column("request_id", sa.Uuid(), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["actor_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_audit_logs_organisation_id_created_at", "audit_logs", ["organisation_id", "created_at"])
    op.create_index("ix_audit_logs_actor_id", "audit_logs", ["actor_id"])
    op.create_index("ix_audit_logs_resource", "audit_logs", ["resource_type", "resource_id"])
    op.create_index("ix_audit_logs_request_id", "audit_logs", ["request_id"])

    # --- Row-Level Security Setup ---
    
    # Create function to get current organisation ID from session variable
    op.execute("""
        CREATE OR REPLACE FUNCTION current_organisation_id() RETURNS uuid AS $$
        BEGIN
            RETURN current_setting('app.current_organisation_id', true)::uuid;
        EXCEPTION WHEN OTHERS THEN
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql SECURITY DEFINER;
    """)
    op.execute("GRANT EXECUTE ON FUNCTION current_organisation_id() TO PUBLIC;")

    # Enable RLS on all tenant tables
    tenant_tables = [
        "entities", "memberships", "roles", "sessions", "api_tokens", "audit_logs"
    ]
    for table in tenant_tables:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;")

    # Create RLS policies
    # entities
    op.execute("""
        CREATE POLICY entities_tenant_isolation ON entities
        USING (organisation_id = current_organisation_id())
        WITH CHECK (organisation_id = current_organisation_id());
    """)

    # memberships
    op.execute("""
        CREATE POLICY memberships_tenant_isolation ON memberships
        USING (organisation_id = current_organisation_id())
        WITH CHECK (organisation_id = current_organisation_id());
    """)

    # roles
    op.execute("""
        CREATE POLICY roles_tenant_isolation ON roles
        USING (organisation_id = current_organisation_id())
        WITH CHECK (organisation_id = current_organisation_id());
    """)

    # sessions
    op.execute("""
        CREATE POLICY sessions_tenant_isolation ON sessions
        USING (organisation_id = current_organisation_id())
        WITH CHECK (organisation_id = current_organisation_id());
    """)

    # api_tokens
    op.execute("""
        CREATE POLICY api_tokens_tenant_isolation ON api_tokens
        USING (organisation_id = current_organisation_id())
        WITH CHECK (organisation_id = current_organisation_id());
    """)

    # audit_logs
    op.execute("""
        CREATE POLICY audit_logs_tenant_isolation ON audit_logs
        USING (organisation_id = current_organisation_id())
        WITH CHECK (organisation_id = current_organisation_id());
    """)

    # organisations table - special case: users can only see their own organisation
    op.execute("""
        CREATE POLICY organisations_tenant_isolation ON organisations
        USING (id = current_organisation_id())
        WITH CHECK (id = current_organisation_id());
    """)

    # Set default for the session variable
    op.execute("ALTER DATABASE sampati SET app.current_organisation_id = '00000000-0000-0000-0000-000000000000';")


def downgrade() -> None:
    # Drop RLS policies
    tables = ["organisations", "entities", "memberships", "roles", "sessions", "api_tokens", "audit_logs"]
    for table in tables:
        op.execute(f"DROP POLICY IF EXISTS {table}_tenant_isolation ON {table};")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;")

    # Drop function
    op.execute("DROP FUNCTION IF EXISTS current_organisation_id();")

    # Drop tables in reverse order
    op.drop_table("audit_logs")
    op.drop_table("api_tokens")
    op.drop_table("sessions")
    op.drop_table("roles")
    op.drop_table("memberships")
    op.drop_table("users")
    op.drop_table("entities")
    op.drop_table("organisations")

    op.execute('DROP EXTENSION IF EXISTS "pgcrypto"')
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
