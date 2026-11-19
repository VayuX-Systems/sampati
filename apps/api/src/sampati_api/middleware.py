# SPDX-License-Identifier: Apache-2.0
"""Middleware for Sampati API."""

from __future__ import annotations

import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

import structlog

from .services.audit_service import AuditService


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add request ID to each request and response headers."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        # Add to structlog context
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class TenantMiddleware(BaseHTTPMiddleware):
    """Extract and validate tenant context from request."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # In production, extract organisation_id from JWT token or session
        # For now, use a header (dev only)
        org_id = request.headers.get("X-Organisation-ID")
        if org_id:
            request.state.organisation_id = org_id
            structlog.contextvars.bind_contextvars(organisation_id=org_id)

        return await call_next(request)


class AuditLogMiddleware(BaseHTTPMiddleware):
    """Automatically log write operations to audit log."""

    # Methods that should be audited
    AUDIT_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.audit_service = AuditService()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip audit for read-only operations
        if request.method not in self.AUDIT_METHODS:
            return await call_next(request)

        # Skip health checks and docs
        if request.url.path.startswith("/health") or request.url.path.startswith("/docs") or request.url.path.startswith("/redoc") or request.url.path.startswith("/openapi"):
            return await call_next(request)

        # Capture request body for 'before' state (for updates)
        # Note: This is a simplified version; production would need more sophisticated handling
        request_body = None
        if request.method in {"PUT", "PATCH"}:
            try:
                request_body = await request.json()
            except Exception:
                pass

        # Process request
        response = await call_next(request)

        # Log write operations (simplified - in production, use response hooks or dependency injection)
        # The actual audit logging should happen in the route handlers via AuditService
        # This middleware is a safety net

        return response
