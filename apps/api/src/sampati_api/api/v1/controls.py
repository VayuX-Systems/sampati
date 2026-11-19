# SPDX-License-Identifier: Apache-2.0
"""Controls API routes."""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement controls routes for MVP

@router.get("")
async def list_controls():
    """List controls."""
    return {"message": "controls endpoint - implementation in progress"}
