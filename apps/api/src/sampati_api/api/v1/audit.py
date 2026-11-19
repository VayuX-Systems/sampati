# SPDX-License-Identifier: Apache-2.0
"""Audit API routes."""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement audit routes for MVP

@router.get("")
async def list_audit():
    """List audit."""
    return {"message": "audit endpoint - implementation in progress"}
