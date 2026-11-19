# SPDX-License-Identifier: Apache-2.0
"""Tasks API routes."""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement tasks routes for MVP

@router.get("")
async def list_tasks():
    """List tasks."""
    return {"message": "tasks endpoint - implementation in progress"}
