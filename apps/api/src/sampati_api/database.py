# SPDX-License-Identifier: Apache-2.0
"""Database configuration and session management."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import get_settings
from sampati_core_domain.models import Base


_engine = None
_session_factory = None


async def init_db() -> None:
    """Initialize database engine and create tables."""
    global _engine, _session_factory
    settings = get_settings()

    if not settings.database_url:
        raise ValueError("SAMPATI_DATABASE_URL not configured")

    _engine = create_async_engine(
        settings.database_url,
        echo=settings.env == "dev",
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )

    _session_factory = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Create tables (in production, use Alembic migrations)
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    global _engine
    if _engine:
        await _engine.dispose()
        _engine = None


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get the session factory."""
    if _session_factory is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _session_factory


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session."""
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_tenant_session(organisation_id: str) -> AsyncGenerator[AsyncSession, None]:
    """
    Get a database session with tenant context set.

    This sets the PostgreSQL row-level security context for the organisation.
    """
    async with get_session() as session:
        # Set the tenant context for RLS
        await session.execute(
            "SELECT set_config('app.current_organisation_id', :org_id, true)",
            {"org_id": organisation_id},
        )
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
