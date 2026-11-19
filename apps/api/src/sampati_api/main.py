# SPDX-License-Identifier: Apache-2.0
"""Sampati API main entry point."""

from __future__ import annotations

import logging
import sys
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings
from .database import init_db, close_db
from .logging import setup_logging
from .middleware import RequestIDMiddleware, TenantMiddleware
from .errors import APIError, api_error_handler
from .api.v1 import router as v1_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    setup_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        await init_db()
        structlog.get_logger().info("application_started", env=settings.env)
        yield
        # Shutdown
        await close_db()
        structlog.get_logger().info("application_stopped")

    app = FastAPI(
        title="Sampati API",
        description="Open-source compliance automation platform API",
        version="0.1.0-dev",
        lifespan=lifespan,
        docs_url="/docs" if settings.env != "prod" else None,
        redoc_url="/redoc" if settings.env != "prod" else None,
    )

    # Middleware
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(TenantMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.env == "dev" else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    app.add_exception_handler(APIError, api_error_handler)

    # Routes
    app.include_router(v1_router, prefix="/api/v1")

    @app.get("/health")
    async def health_check(request: Request) -> dict[str, str]:
        return {"status": "healthy", "version": "0.1.0-dev"}

    @app.get("/")
    async def root(request: Request) -> dict[str, str]:
        return {"name": "Sampati by VayuX", "version": "0.1.0-dev", "docs": "/docs"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "sampati_api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.env == "dev",
        log_level=settings.log_level.lower(),
    )
